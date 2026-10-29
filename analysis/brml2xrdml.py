#!/usr/bin/env python3
"""Convert Bruker .brml powder scans to PANalytical .xrdml for HighScore Plus.

A .brml file is a ZIP archive of Bruker "Experiment" XML documents. HighScore
Plus cannot read .brml, but it reads .xrdml natively and takes the instrument
metadata (wavelength, goniometer radius, tube settings, timestamps) from it.

Usage:
    pixi run python analysis/brml2xrdml.py data/XRD/XRD1/MgFe2O4.brml
    pixi run python analysis/brml2xrdml.py data/XRD/XRD*/*.brml --xy

The .xrdml (and optional .xy) is written next to each .brml file.
"""

from __future__ import annotations

import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

XRDML_NAMESPACE = "http://www.xrdml.com/XRDMeasurement/1.3"

# Bruker reports the Cu K-beta line nowhere in these files; the constant below
# is the standard Cu K-beta value used by every .xrdml producer.
CU_K_BETA_ANGSTROM = "1.3922500"
K_ALPHA2_TO_K_ALPHA1_RATIO = "0.5000"


class BrmlError(Exception):
    """Raised when a .brml archive does not contain the expected scan data."""


@dataclass(frozen=True)
class Scan:
    """Trusted, fully parsed scan ready for serialisation."""

    two_theta: tuple[str, ...]
    counts: tuple[str, ...]
    counting_time_seconds: str
    scan_mode: str
    wavelength_alpha1_angstrom: str
    wavelength_alpha2_angstrom: str
    tube_tension_kv: str
    tube_current_ma: str
    goniometer_radius_mm: str
    operator: str
    sample_id: str
    started: str
    finished: str


def archive_member(archive: zipfile.ZipFile, suffix: str) -> bytes:
    """Return the bytes of the first member whose path ends with `suffix`."""
    for name in archive.namelist():
        if name.endswith(suffix):
            return archive.read(name)
    raise BrmlError(f"archive has no member ending with {suffix!r}")


def parse_xml(archive: zipfile.ZipFile, suffix: str) -> ElementTree.Element:
    return ElementTree.fromstring(archive_member(archive, suffix))


def require(element: ElementTree.Element | None, what: str) -> ElementTree.Element:
    if element is None:
        raise BrmlError(f"missing {what}")
    return element


def text_of(root: ElementTree.Element, tag: str) -> str:
    element = require(next(root.iter(tag), None), f"<{tag}>")
    return require(element.text, f"text in <{tag}>").strip()


def value_of(root: ElementTree.Element, tag: str) -> str:
    element = require(next(root.iter(tag), None), f"<{tag}>")
    return require(element.get("Value"), f"Value attribute on <{tag}>")


def optional_text(root: ElementTree.Element, tag: str) -> str:
    element = next(root.iter(tag), None)
    return (element.text or "").strip() if element is not None else ""


def parse_scan(brml_path: Path) -> Scan:
    if not brml_path.is_file():
        raise BrmlError(f"{brml_path} does not exist")

    archive = zipfile.ZipFile(brml_path)
    raw = parse_xml(archive, "RawData0.xml")
    measurement = parse_xml(archive, "MeasurementContainer.xml")
    instruction = parse_xml(archive, "InstructionContainer.xml")

    points = [d.text for d in raw.iter("Datum") if d.text]
    if not points:
        raise BrmlError("RawData0.xml contains no <Datum> rows")

    columns = [row.split(",") for row in points]
    two_theta = tuple(column[2] for column in columns)
    counts = tuple(column[4] for column in columns)
    if len(two_theta) != len(counts):
        raise BrmlError("two-theta and intensity columns differ in length")

    scan_info = require(next(raw.iter("ScanInformation"), None), "<ScanInformation>")
    radius = next(
        (e.get("Value") for e in instruction.iter("Radius") if e.get("Value") not in (None, "0")),
        None,
    )
    identifier = require(next(measurement.iter("Identifier"), None), "<Identifier>")

    return Scan(
        two_theta=two_theta,
        counts=counts,
        counting_time_seconds=text_of(raw, "TimePerStep"),
        scan_mode=text_of(scan_info, "ScanModeVisibleName"),
        wavelength_alpha1_angstrom=value_of(instruction, "WaveLengthAlpha1"),
        wavelength_alpha2_angstrom=value_of(instruction, "WaveLengthAlpha2"),
        tube_tension_kv=value_of(instruction, "Voltage"),
        tube_current_ma=value_of(instruction, "Current"),
        goniometer_radius_mm=require(radius, "goniometer radius in InstructionContainer.xml"),
        operator=identifier.get("UserName") or "",
        sample_id=next((e.get("Value") for e in measurement.iter("SampleId")), "") or "",
        started=optional_text(raw, "TimeStampStarted"),
        finished=optional_text(raw, "TimeStampFinished"),
    )


def render_xrdml(scan: Scan) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<xrdMeasurements xmlns="{XRDML_NAMESPACE}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="{XRDML_NAMESPACE} {XRDML_NAMESPACE}/XRDMeasurement.xsd" status="Completed" sampleMode="Reflection">
\t<comment>
\t\t<entry>Converted from Bruker .brml; scan mode={scan.scan_mode}</entry>
\t\t<entry>Operator={scan.operator}</entry>
\t</comment>
\t<sample type="To be analyzed">
\t\t<id>{scan.sample_id}</id>
\t\t<name>{scan.sample_id}</name>
\t</sample>
\t<xrdMeasurement measurementType="Scan" status="Completed" sampleMode="Reflection">
\t\t<usedWavelength intended="K-Alpha 1">
\t\t\t<kAlpha1 unit="Angstrom">{scan.wavelength_alpha1_angstrom}</kAlpha1>
\t\t\t<kAlpha2 unit="Angstrom">{scan.wavelength_alpha2_angstrom}</kAlpha2>
\t\t\t<kBeta unit="Angstrom">{CU_K_BETA_ANGSTROM}</kBeta>
\t\t\t<ratioKAlpha2KAlpha1>{K_ALPHA2_TO_K_ALPHA1_RATIO}</ratioKAlpha2KAlpha1>
\t\t</usedWavelength>
\t\t<incidentBeamPath>
\t\t\t<radius unit="mm">{scan.goniometer_radius_mm}</radius>
\t\t\t<xRayTube name="Bruker D8 sealed tube">
\t\t\t\t<tension unit="kV">{scan.tube_tension_kv}</tension>
\t\t\t\t<current unit="mA">{scan.tube_current_ma}</current>
\t\t\t\t<anodeMaterial>Cu</anodeMaterial>
\t\t\t</xRayTube>
\t\t</incidentBeamPath>
\t\t<scan appendNumber="0" mode="Continuous" scanAxis="TwoTheta" status="Completed">
\t\t\t<header>
\t\t\t\t<startTimeStamp>{scan.started}</startTimeStamp>
\t\t\t\t<endTimeStamp>{scan.finished}</endTimeStamp>
\t\t\t\t<author>
\t\t\t\t\t<name>{scan.operator}</name>
\t\t\t\t</author>
\t\t\t\t<source>
\t\t\t\t\t<applicationSoftware version="6.5.0.0">Bruker Data Collector</applicationSoftware>
\t\t\t\t\t<instrumentControlSoftware version="6.5.0.0">Bruker Data Collector</instrumentControlSoftware>
\t\t\t\t</source>
\t\t\t</header>
\t\t\t<dataPoints>
\t\t\t\t<positions axis="2Theta" unit="deg">{" ".join(scan.two_theta)}</positions>
\t\t\t\t<commonCountingTime unit="seconds">{scan.counting_time_seconds}</commonCountingTime>
\t\t\t\t<intensities unit="counts">{" ".join(scan.counts)}</intensities>
\t\t\t</dataPoints>
\t\t</scan>
\t</xrdMeasurement>
</xrdMeasurements>
"""


def render_xy(scan: Scan) -> str:
    rows = zip(scan.two_theta, scan.counts, strict=True)
    return "".join(f"{angle} {count}\n" for angle, count in rows)


def convert(brml_path: Path, also_xy: bool) -> tuple[Scan, tuple[Path, ...]]:
    scan = parse_scan(brml_path)
    xrdml_path = brml_path.with_suffix(".xrdml")
    xrdml_path.write_text(render_xrdml(scan), encoding="utf-8")
    written = [xrdml_path]
    if also_xy:
        xy_path = brml_path.with_suffix(".xy")
        xy_path.write_text(render_xy(scan), encoding="utf-8")
        written.append(xy_path)
    return scan, tuple(written)


def main(argv: list[str]) -> int:
    also_xy = "--xy" in argv
    sources = [Path(arg) for arg in argv if not arg.startswith("-")]
    if not sources:
        print(__doc__, file=sys.stderr)
        return 2

    for source in sources:
        try:
            scan, written = convert(source, also_xy)
        except (BrmlError, zipfile.BadZipFile) as error:
            print(f"{source}: {error}", file=sys.stderr)
            return 1
        print(
            f"{source} -> {', '.join(str(path) for path in written)} "
            f"({len(scan.counts)} points, Ka1={scan.wavelength_alpha1_angstrom} A, "
            f"{scan.counting_time_seconds} s/step)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
