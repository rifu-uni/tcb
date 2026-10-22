# TCB

Characterization data and analysis for the MgFe2O4 TCB experiment.

## Contents

| Path | Purpose |
|---|---|
| `UV-vis/` | UV-vis reflectance export (`.csv`) and instrument file (`.DSW`) |
| `XRay/` | Bruker D8 scan `MG_AS` (`.brml` + extracted XML) |
| `Xray2/` | Bruker D8 scan `MgFeO4` (`.brml` + extracted XML) |
| `SEM/` | SEM images, EDX spectrum and exports |
| `highscore/` | HighScore phase identification and refinement exports |
| `rietveld/` | Rietveld refinement script, reflection tables, fits |
| `uvvis_xrd_analysis.ipynb` | UV-vis and XRD comparison notebook |

## Environment

The pixi workspace provides Python, Jupyter, NumPy, SciPy and Matplotlib.

```bash
pixi install
pixi run jupyter lab uvvis_xrd_analysis.ipynb
```

Run notebooks and scripts from the repository root; paths are relative to it.

## Rietveld refinement

```bash
pixi run python rietveld/rietveld_tcb.py
```

The script refines both scans against the hematite and magnesioferrite
reflection tables in `rietveld/reflections.json` and overwrites
`rietveld/fit_MG_AS.png` and `rietveld/fit_MgFeO4.png`.
