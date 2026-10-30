#!/usr/bin/env python3
"""Synthesize a Bruker RAW4.00 file from a .brml scan.

HighScore Plus reads Bruker .raw natively, so this route skips XRDML entirely.
There is no public RAW4.00 writer; instead this script clones the 885-byte
header of a known-good RAW4.00 file produced by Bruker's BrmlToV4Converter and
patches the fields that identify the scan (start, step, point count, drives,
wavelengths, tube settings, timestamp) plus the intensity array.

Usage:
    pixi run python analysis/brml2raw.py data/XRD/XRD1/MgFe2O4.brml \\
        --template data/XRD/XRD2/MgFe2O4.raw

The .raw is written next to the .brml file. Existing files are kept unless
--force is given, so the Bruker-generated template itself is never clobbered.
"""

from __future__ import annotations

import argparse
import struct
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from brml2xrdml import BrmlError, Scan, parse_scan

RAW4_MAGIC = b"RAW4.00\0"
RAW4_HEADER_BYTES = 885
RAW4_RECORD_BYTES = 4
CU_K_BETA_ANGSTROM = 1.39222
K_ALPHA2_TO_K_ALPHA1_RATIO = 0.5
FLOAT32_EXACT_INTEGER_LIMIT = 2**24

# All offsets below are inside the fixed part of the RAW4.00 file, verified
# against the BrmlToV4Converter output in data/XRD/XRD2/MgFe2O4.raw.
DATE_OFFSET = 0x0C
TIME_OFFSET = 0x18
K_ALPHA_AVERAGE_OFFSET = 400
K_ALPHA1_OFFSET = 408
K_ALPHA2_OFFSET = 416
K_BETA_OFFSET = 424
K_ALPHA2_RATIO_OFFSET = 432
POINTS_OFFSET_A = 468
POINTS_OFFSET_B = 472
RANGE_START_OFFSET = 536
RANGE_STEP_OFFSET = 544
RANGE_POINTS_OFFSET = 552
RANGE_KV_OFFSET = 564
RANGE_MA_OFFSET = 568
RANGE_K_ALPHA_AVERAGE_OFFSET = 576
TWO_THETA_DRIVE_OFFSET = 757
THETA_DRIVE_OFFSET = 849

TEMPLATE_EXPECTED = {
    K_ALPHA_AVERAGE_OFFSET: ("<d", 1.5418),
    K_ALPHA1_OFFSET: ("<d", 1.5406),
    K_ALPHA2_OFFSET: ("<d", 1.54439),
    K_BETA_OFFSET: ("<d", 1.39222),
    K_ALPHA2_RATIO_OFFSET: ("<d", 0.5),
    RANGE_K_ALPHA_AVERAGE_OFFSET: ("<d", 1.5418),
    RANGE_KV_OFFSET: ("<f", 40.0),
    RANGE_MA_OFFSET: ("<f", 25.0),
}


@dataclass(frozen=True)
class RawTemplate:
    """Validated RAW4.00 header, ready to be patched."""

    header: bytes
    points: int
    start_two_theta: float
    step_degrees: float


def checked(condition: bool, message: str) -> None:
    if not condition:
        raise BrmlError(message)


def template_double(blob: bytes, offset: int, name: str) -> float:
    checked(offset + 8 <= len(blob), f"template is too short for {name}")
    return struct.unpack_from("<d", blob, offset)[0]


def template_uint32(blob: bytes, offset: int, name: str) -> int:
    checked(offset + 4 <= len(blob), f"template is too short for {name}")
    return struct.unpack_from("<I", blob, offset)[0]


def load_template(path: Path) -> RawTemplate:
    if not path.is_file():
        raise BrmlError(f"template {path} does not exist")
    blob = path.read_bytes()

    checked(blob.startswith(RAW4_MAGIC), f"{path} is not a RAW4.00 file")
    points = template_uint32(blob, RANGE_POINTS_OFFSET, "point count")
    data_offset = len(blob) - RAW4_RECORD_BYTES * points
    checked(
        data_offset == RAW4_HEADER_BYTES,
        f"{path} is not a recognised RAW4.00 template: data starts at "
        f"{data_offset}, expected {RAW4_HEADER_BYTES}",
    )
    checked(
        template_uint32(blob, POINTS_OFFSET_A, "point count copy A") == points
        and template_uint32(blob, POINTS_OFFSET_B, "point count copy B") == points,
        f"{path} has inconsistent point counts in its range header",
    )

    start = template_double(blob, RANGE_START_OFFSET, "scan start")
    step = template_double(blob, RANGE_STEP_OFFSET, "scan step")
    checked(
        abs(template_double(blob, TWO_THETA_DRIVE_OFFSET, "2Theta drive") - start) < 1e-6
        and abs(template_double(blob, THETA_DRIVE_OFFSET, "Theta drive") - start / 2) < 1e-6,
        f"{path} does not have the expected coupled scan drive layout",
    )
    checked(0 < step < 1, f"{path} has an implausible step of {step} deg")

    for offset, (format_code, expected) in TEMPLATE_EXPECTED.items():
        width = struct.calcsize(format_code)
        checked(
            offset + width <= len(blob),
            f"{path} is too short for the field at {offset}",
        )
        actual = struct.unpack_from(format_code, blob, offset)[0]
        checked(
            abs(actual - expected) < 1e-4,
            f"{path} has {actual} at offset {offset}, expected {expected}",
        )

    return RawTemplate(
        header=blob[:RAW4_HEADER_BYTES],
        points=points,
        start_two_theta=start,
        step_degrees=step,
    )


def uniform_step(scan: Scan) -> float:
    angles = [float(value) for value in scan.two_theta]
    checked(len(angles) >= 2, "a RAW4.00 scan needs at least two points")
    checked(scan.is_uniform_scan, "RAW4.00 cannot express a non-uniform step")
    steps = [later - earlier for earlier, later in zip(angles, angles[1:])]
    median_step = sorted(steps)[len(steps) // 2]
    checked(abs(median_step) > 0, "scan step must be non-zero")
    return median_step


def scan_timestamp(scan: Scan) -> tuple[bytes, bytes] | None:
    if not scan.started:
        return None
    try:
        started = datetime.fromisoformat(scan.started)
    except ValueError:
        return None
    date = started.strftime("%m/%d/%Y").encode("ascii").ljust(12, b"\0")
    time = started.strftime("%H:%M:%S").encode("ascii").ljust(12, b"\0")
    return date, time


def render_raw(scan: Scan, template: RawTemplate) -> bytes:
    points = len(scan.counts)
    intensities = [int(value) for value in scan.counts]
    checked(
        all(abs(value) < FLOAT32_EXACT_INTEGER_LIMIT for value in intensities),
        "intensities exceed the exact integer range of float32",
    )

    step = uniform_step(scan)
    start = float(scan.two_theta[0])
    k_alpha1 = float(scan.wavelength_alpha1_angstrom)
    k_alpha2 = float(scan.wavelength_alpha2_angstrom)

    header = bytearray(template.header)
    struct.pack_into("<d", header, RANGE_START_OFFSET, start)
    struct.pack_into("<d", header, RANGE_STEP_OFFSET, step)
    for offset in (POINTS_OFFSET_A, POINTS_OFFSET_B, RANGE_POINTS_OFFSET):
        struct.pack_into("<I", header, offset, points)
    struct.pack_into("<d", header, TWO_THETA_DRIVE_OFFSET, start)
    struct.pack_into("<d", header, THETA_DRIVE_OFFSET, start / 2)
    struct.pack_into("<d", header, K_ALPHA1_OFFSET, k_alpha1)
    struct.pack_into("<d", header, K_ALPHA2_OFFSET, k_alpha2)
    struct.pack_into("<d", header, K_BETA_OFFSET, CU_K_BETA_ANGSTROM)
    struct.pack_into("<d", header, K_ALPHA2_RATIO_OFFSET, K_ALPHA2_TO_K_ALPHA1_RATIO)
    average = (2 * k_alpha1 + k_alpha2) / 3
    struct.pack_into("<d", header, K_ALPHA_AVERAGE_OFFSET, average)
    struct.pack_into("<d", header, RANGE_K_ALPHA_AVERAGE_OFFSET, average)
    struct.pack_into("<f", header, RANGE_KV_OFFSET, float(scan.tube_tension_kv))
    struct.pack_into("<f", header, RANGE_MA_OFFSET, float(scan.tube_current_ma))

    timestamp = scan_timestamp(scan)
    if timestamp is not None:
        date, time = timestamp
        header[DATE_OFFSET : DATE_OFFSET + 12] = date
        header[TIME_OFFSET : TIME_OFFSET + 12] = time

    intensities_bytes = struct.pack(f"<{points}f", *intensities)
    return bytes(header) + intensities_bytes


def verify_raw(blob: bytes, scan: Scan) -> None:
    points = len(scan.counts)
    checked(
        len(blob) == RAW4_HEADER_BYTES + RAW4_RECORD_BYTES * points,
        "written RAW4.00 file has an inconsistent size",
    )
    checked(blob.startswith(RAW4_MAGIC), "written file lost its RAW4.00 magic")
    for offset in (POINTS_OFFSET_A, POINTS_OFFSET_B, RANGE_POINTS_OFFSET):
        checked(
            struct.unpack_from("<I", blob, offset)[0] == points,
            "written RAW4.00 point count does not round-trip",
        )
    expected_start = float(scan.two_theta[0])
    checked(
        abs(struct.unpack_from("<d", blob, RANGE_START_OFFSET)[0] - expected_start) < 1e-9,
        "written RAW4.00 start position does not round-trip",
    )
    stored = struct.unpack_from(f"<{points}f", blob, RAW4_HEADER_BYTES)
    checked(
        [int(value) for value in stored] == [int(value) for value in scan.counts],
        "written RAW4.00 intensities do not round-trip",
    )


def convert(brml_path: Path, template_path: Path, force: bool) -> Path:
    raw_path = brml_path.with_suffix(".raw")
    if raw_path.exists() and not force:
        raise BrmlError(f"{raw_path} already exists; pass --force to replace it")
    template = load_template(template_path)
    scan = parse_scan(brml_path)
    blob = render_raw(scan, template)
    verify_raw(blob, scan)
    raw_path.write_bytes(blob)
    return raw_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brml", type=Path, nargs="+", help="Bruker .brml file(s)")
    parser.add_argument("--template", type=Path, required=True, help="known-good RAW4.00 file")
    parser.add_argument("--force", action="store_true", help="replace an existing .raw")
    arguments = parser.parse_args(argv)

    for brml_path in arguments.brml:
        try:
            raw_path = convert(brml_path, arguments.template, arguments.force)
        except (BrmlError, OSError) as error:
            print(f"{brml_path}: {error}", file=sys.stderr)
            return 1
        print(f"{brml_path} -> {raw_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
