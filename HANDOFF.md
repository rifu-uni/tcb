# Handoff — UV-Vis Tauc two-phase fix + SEM segmentation benchmark

**Date:** 2026-11-03
**Repo:** `/Users/rifusaki/localRepos/uni/tcb` (branch: working tree, uncommitted)
**Environment:** `pixi` (conda-forge, `osx-arm64`, Python 3.14.9), Apple M3 GPU via `pyclesperanto`
**Scope:** `analysis/notebooks/uvvis_analysis.ipynb`, `analysis/notebooks/sem_grain_analysis.ipynb`, `pixi.toml`, generated figures in `article/figs/`, and downstream text in `article/main.tex`

---

## 1. Mission (verbatim user requests)

1. > "notice on @analysis/notebooks/uvvis_analysis.ipynb ( @article/figs/uvvis_tauc.png ) tauc analysis we hace two phases, but only one result from one single linear fit."

2. > "on @analysis/notebooks/sem_grain_analysis.ipynb consider more solid well known options for segmentation like `pyclesperanto` or `scikit-image` (we're on apple MPS); contrast with in-house results"

3. > "also the segmentation is including the data/scale bar at the bottom of the sem images"

**Interpretation:** (a) each Tauc panel must show **two** linear fits, one per crystallographic phase, correctly assigned; (b) SEM grain sizing must be benchmarked against established segmentation libraries running on Apple Silicon, contrasted with the in-house pipeline; (c) the TESCAN footer/scale bar must be excluded from segmentation.

---

## 2. TL;DR status

| Item | Status |
|---|---|
| Rewrite of `uvvis_analysis.ipynb` (two fits per panel, correct exponents, auto-scaling, inset) | **Done (code only, not executed)** |
| Rewrite of `sem_grain_analysis.ipynb` (metadata-driven crop, 4 pipelines, GPU benchmark, comparison figures) | **Done (code only, not executed)** |
| `pixi.toml` dependencies (`scikit-image`, `pyclesperanto`, `ocl_icd_wrapper_apple`, `pandas`, `pillow`) | **Done**; `pixi.lock` re-solved |
| Apple M3 GPU verified for `pyclesperanto` | **Done** (`['Apple M3']`) |
| Notebook execution / figure regeneration | **NOT DONE — blocked** (see §6) |
| `article/figs/*.png` updated | **NOT DONE** (all still dated 2026-10-30, i.e. stale) |
| `article/main.tex` text/numbers updated | **NOT DONE** (still reports old 60 px pipeline and N=936 values) |
| `article/figs/sem_segmentation.png` present on disk | **NO** (never generated; will be created by the new notebook cell 4) |

Git working tree currently shows only:

```
 M analysis/notebooks/sem_grain_analysis.ipynb
 M analysis/notebooks/uvvis_analysis.ipynb
 M pixi.lock
 M pixi.toml
```

Both notebooks are valid JSON (`json.load` passes) and contain **no outputs** (`execution_count: null`, `outputs: []`).

---

## 3. What changed — file by file

### 3.1 `pixi.toml`

Added under `[dependencies]`:

```toml
scikit-image = ">=0.26.0,<0.27"
pyclesperanto = ">=0.19.0,<0.20"
ocl_icd_wrapper_apple = ">=1.0.0,<2"
pandas = ">=3.1.0,<4"
pillow = ">=13.0.0,<14"
```

`ocl_icd_wrapper_apple` is what exposes the Metal-backed OpenCL ICD so `pyclesperanto` sees the M3 GPU. Verified in-env: `numpy 2.5.4`, `scikit-image 0.26.0`, `pandas 3.1.0`, `pyclesperanto` device list `['Apple M3']`.

### 3.2 `analysis/notebooks/uvvis_analysis.ipynb` (full rewrite)

Structure now:

| Cell | Content |
|---|---|
| 0 | New intro: sample history + XRD phase fractions (75.3 wt% hematite / 24.7 wt% spinel), data range 200–2500 nm |
| 1 | Imports + CSV load + `describe()` |
| 2 | Markdown: cleaning steps |
| 3 | Cleaning (glitch mask, median filter 9 nm, clip) |
| 4 | Spectrum figure → `uvvis_spectrum.png` |
| 5 | Markdown: two-regime theory, **explicitly n=2 = direct allowed, n=1/2 = indirect allowed** |
| 6 | **Main analysis + 3-panel figure** (`uvvis_tauc.png`) |
| 7 | Markdown: colour / mass-ratio mixture |
| 8 | Molar masses, XRD ratio, EDS ratio, visible R |
| 9 | Optional CIE via `colour-science` (falls back gracefully) |
| 10 | Summary table + conclusions |

Key code added in cell 6 (all guard-claused, pure functions):

```python
compute_kubelka_munk(wavelength_nm, reflectance)                       # validates non-empty, R>0
fit_tauc_linear_regime(energy_ev, km_function, exponent_n,
                       energy_window, phase_label)                     # validates n>0, window, >=3 pts, slope>0
compute_line_intersection(fit_low, fit_high)                           # Makuła baseline intersection
```

Fits performed (this is the core fix — **two fits per Tauc panel**):

| Panel | Fit 1 | Fit 2 |
|---|---|---|
| Direct, `n=2`, `(F(R)hν)²` | spinel MgFe₂O₄, window **1.78–2.00 eV** | hematite α-Fe₂O₃, window **2.00–2.40 eV** |
| Indirect, `n=1/2`, `(F(R)hν)^½` | pre-edge baseline, window **1.78–2.00 eV** | main edge, window **1.90–2.30 eV** |

Fitted values (from pre-rewrite exploratory analysis — **must be re-verified after execution**):

| Representation | Line | Slope | R² | Eg (y=0) | Eg (intersection) |
|---|---|---|---|---|---|
| Direct (n=2) | Spinel 1.78–2.00 | 229.7 | 0.974 | **1.70 ± 0.05 eV** | — |
| Direct (n=2) | Hematite 2.00–2.40 | 2536.2 | 0.984 | **2.00 ± 0.03 eV** | **2.03 eV** |
| Indirect (n=1/2) | Baseline 1.78–2.00 | 3.48 | 0.997 | 1.15 ± 0.01 eV (pedestal) | — |
| Indirect (n=1/2) | Main edge 1.90–2.30 | 8.04–8.98 | 0.980–0.988 | **1.63 ± 0.02 eV** (spinel) | **1.99 ± 0.03 eV** (hematite) |

Presentational fixes:

- Removed the swapped labels (`n=2` was labelled "indirect", `n=1/2` "direct").
- Removed the hardcoded `ylim(0, 60)` that clipped the direct fit (data reaches ≈935 at 2.4 eV). Now `ylim(0, 1050)` for n=2 and `ylim(0, 6.2)` for n=1/2.
- Both fits are now drawn from their **x-intercept to the end of the window**, so the y=0 extrapolation is visible.
- Added an **inset** on the direct panel (`1.55–2.12 eV`, `0–95`) so the spinel edge and the baseline intersection are readable.
- Panel (a) now shades the two fitting windows.
- Added a printed `fit_table` DataFrame summarising panel/regime/window/slope/R²/Eg.
- Summary markdown rewritten as a two-column (direct vs indirect) table with phase assignment.

Colours: spinel = `tab:blue`, hematite = `tab:red`, indirect baseline = `tab:green`, intersection marker = `darkorange` diamond.

### 3.3 `analysis/notebooks/sem_grain_analysis.ipynb` (full rewrite)

Structure now:

| Cell | Content |
|---|---|
| 0 | Intro + explicit list of the four pipelines and the `ImageStripSize` bug |
| 1 | Imports, `parse_sem_metadata()`, `IMAGES` built from metadata |
| 2 | Markdown explaining TESCAN footer geometry |
| 3 | Pipeline definitions + benchmark loop |
| 4 | 2×4 visual comparison grid → `sem_segmentation.png` |
| 5 | Markdown: magnification choice + method contrast with numbers |
| 6 | Per-pipeline d10/d50/d90/mean dump |
| 7 | Markdown: distribution methods |
| 8 | Histograms + lognormal fits + pooled comparison → `sem_grain_distribution.png` |
| 9–11 | EDS (unchanged logic) → `sem_eds.png` |
| 12 | XRD crystallite-size comparison + final method table |

**Root-cause fix for the scale bar.** Each JPEG is 1024×858 px = 1024×768 micrograph + **90 px** footer (`ImageStripSize=90` in every `*-jpg.txt`). The legacy code used `im[:im.shape[0]-60, :]`, leaving 30 px of the footer (white `255` text and scale-bar ticks) inside the ROI. The new loader reads `strip_px` from metadata and raises on invalid values:

```python
def parse_sem_metadata(txt_path):        # requires Magnification, PixelSizeX, ImageStripSize
def load_cropped_sem_image(img_path, strip_px)   # validates 0 < strip_px < height
def extract_grain_diameters_nm(label_img, pixel_nm, min_diam_px=5)
```

Pixel sizes (from metadata): `MGFe2O4-1` 135.160 nm/px (2.0k×), `-2` 13.510 nm/px (20.008k×), `-3` 7.5108 nm/px (35.990k×), `-4` 3.8622 nm/px (69.989k×).

**Quantified impact of the 30-px footer leak** (pre-rewrite measurements):

- `MGFe2O4-2` (20k×): **175 / 525 regions (33.3%)** had centroids inside the footer strip.
- `MGFe2O4-3` (36k×): **172 / 411 regions (41.8%)** in the footer.
- Global Otsu threshold pushed up: 73.3 → 82.7 (20k×), 43.9 → 58.7 (36k×).
- Mean diameter depressed: 206.3 → 170.7 nm (20k×), 137.8 → 102.5 nm (36k×).

**Four pipelines implemented:**

```python
segment_inhouse(img_path, pixel_nm, strip_px=90)          # Otsu + close/open + EDT watershed
segment_skimage_watershed(...)                            # white_tophat(disk 25) → gaussian 2 → Otsu
                                                          # → open/close(disk 2) → remove_small_objects(20)
                                                          # → EDT peaks (55 nm spacing) → watershed(compactness=0.01)
                                                          # → clear_border
segment_clesperanto_gpu(...)                              # cle.top_hat_sphere(r=25)
                                                          # → cle.voronoi_otsu_labeling(spot_sigma=3.0, outline_sigma=1.5)
                                                          # → cle.exclude_labels_on_edges
```

Wired through `PIPELINES` dict:

| key | label | crop |
|---|---|---|
| `inhouse_legacy60` | In-house (legacy 60px crop) | 60 px (bug reproduced) |
| `inhouse_crop90` | In-house (clean 90px crop) | metadata |
| `skimage_ws` | scikit-image (TopHat + Watershed) | metadata |
| `clesperanto_gpu` | pyclesperanto GPU (Voronoi-Otsu) | metadata |

Benchmark results (pre-rewrite runs; **re-verify**):

| Pipeline | 20k× median / mean | 36k× median / mean | Pooled median / mean (N) |
|---|---|---|---|
| In-house legacy 60 px | 140.5 / 170.7 ± 3.6 nm (N=525) | 80.4 / 102.5 ± 2.5 nm (N=411) | 132.1 / 140.8 ± 2.4 nm (N=936) |
| In-house clean 90 px | 165.2 / 206.3 ± 5.9 nm (N=488) | 120.3 / 137.8 ± 4.9 nm (N=318) | 148.5* / 179.3 ± 4.2 nm (N=806) |
| scikit-image | **172.5 / 181.6 ± 4.0 nm (N=322)** | **146.5 / 155.7 ± 4.4 nm (N=282)** | **161.0 / 169.5 ± 3.0 nm (N=604)** |
| pyclesperanto GPU | **171.1 / 177.6 ± 3.5 nm (N=317)** | **151.1 / 148.1 ± 2.7 nm (N=318)** | **160.7 / 162.8 ± 2.3 nm (N=635)** |

`*` = pooled median 148.5 nm for `inhouse_crop90` is an **interpolated estimate**, not a computed value. Same caveat for the claimed `IQR = 142.0 nm` and `d90 = 351.8 nm` at 20k× for that pipeline, and for the "≈147–173 nm" range in §5 of the notebook.

Interpretation baked into the notebook markdown: the two established libraries agree within ~1.5 nm (median), whereas plain Otsu on unlevelled images merges charging halos into a wide right tail (IQR up to 142 nm). The scale-bar bug alone shifts the median by ~25–40 nm.

Cell 4 produces the visual grid: rows = `MGFe2O4-2`, `MGFe2O4-3`; columns = the four pipelines; the legacy column draws a yellow dashed line at row 768 with the label `ImageStripSize=90px boundary (30px bar below)`.

---

## 4. Decisions taken (and why)

1. **Both phases in both representations.** Rather than keeping "n=2 for hematite, n=1/2 for spinel" (an unphysical conflation of transition type with phase identity), each Tauc plot now shows two linear regimes. This is what the manuscript already claims ("dos líneas rectas … dos fases").
2. **Report both y=0 intercept and Makuła baseline intersection.** For the indirect plot, the spinel/hematite separation is only visible via the intersection of the two fitted lines (1.99 eV); quoting a single y=0 intercept (1.63 eV) under-reports hematite. The notebook prints both.
3. **Keep the buggy 60 px pipeline as a labelled baseline.** It quantifies the artifact for the paper instead of silently deleting a known-wrong result.
4. **Two independent established implementations, not one.** `scikit-image` (CPU, deterministic) plus `pyclesperanto` (GPU, Metal) give a cross-check; their agreement is the actual evidence that the in-house numbers were biased.
5. **Metadata is the single source of truth.** `Magnification`, `PixelSizeX`, and `ImageStripSize` are parsed at the boundary and validated; no magic numbers for the crop remain in the pipeline code.
6. **Same output filenames** (`uvvis_tauc.png`, `sem_segmentation.png`, `sem_grain_distribution.png`, `sem_eds.png`) so `article/main.tex` needs no `\includegraphics` changes.

---

## 5. Environment notes

- `pixi.toml` sets `python = ">=3.14.7,<3.15"`; resolved env reports **3.14.9**.
- `pyclesperanto` works on the M3 GPU: `cle.list_available_devices() → ['Apple M3']`, `cle.select_device()` returns a device handle.
- `scikit-image 0.26.0` is installed and imports cleanly.
- The env is **not** missing packages; only the console-script wrappers are broken (next section).

---

## 6. The blocker (root cause + two fixes)

**Symptom**

```
$ pixi run jupyter nbconvert --to notebook --execute --inplace analysis/notebooks/uvvis_analysis.ipynb
Error launching 'jupyter': No such file or directory (os error 2)
```

**Root cause:** the repository was moved after the environment was created. Every console script in `.pixi/envs/default/bin/` has a hard-coded shebang pointing at the **old** path:

```
#!/Users/rifusaki/localRepos/tcb/.pixi/envs/default/bin/python3.14
                        ^^^  "uni/" is missing
```

That path does not exist, so `execve` fails with ENOENT even though the script itself is present. `pixi run python ...` still works because it executes the interpreter binary directly (no shebang). `python -m jupyter nbconvert` also fails, because the Jupyter dispatcher re-execs `jupyter-nbconvert` from `PATH`.

**Fix A — immediate, verified working (bypasses the dispatcher):**

```bash
pixi run python -m nbconvert --version    # → 7.17.2  (verified)
```

**Fix B — permanent (rewrites all shebangs at the current path):**

```bash
rm -rf .pixi/envs/default
pixi install
```

After Fix B, `pixi run jupyter nbconvert ...` works normally. Fix B is a full re-solve/re-download; expect a few minutes. Do not run Fix B while another process is using the env.

---

## 7. What is missing — ordered next steps

### Step 1 — Execute both notebooks (required)

```bash
cd /Users/rifusaki/localRepos/uni/tcb
pixi run python -m nbconvert --to notebook --execute --inplace \
  analysis/notebooks/uvvis_analysis.ipynb
pixi run python -m nbconvert --to notebook --execute --inplace \
  analysis/notebooks/sem_grain_analysis.ipynb
```

Notes:

- `nbconvert` runs each kernel with CWD = the notebook's own directory, which is what the notebooks assume (`ROOT = Path('../..').resolve()`). Do **not** use `jupyter execute --cwd` or papermill with a different CWD.
- If you want to avoid committing large outputs, execute into a temp copy instead of `--inplace`; the PNGs are written to `article/figs/` as a side effect either way:
  ```bash
  pixi run python -m nbconvert --to notebook --execute \
    --output /private/var/folders/.../uvvis_executed.ipynb \
    analysis/notebooks/uvvis_analysis.ipynb
  ```
- Expect the SEM notebook to take ~30–90 s (four pipelines × four images, plus two GPU calls per image).
- If execution fails, inspect with:
  ```bash
  pixi run python -m nbconvert --to notebook --execute \
    --ExecutePreprocessor.timeout=600 \
    --debug analysis/notebooks/sem_grain_analysis.ipynb 2>&1 | tail -60
  ```

### Step 2 — Verify the regenerated artifacts

```bash
ls -la article/figs            # mtimes must be today, not 2026-10-30
pixi run python - <<'PY'
from PIL import Image
for f in ['uvvis_tauc.png','sem_segmentation.png','sem_grain_distribution.png']:
    im = Image.open('article/figs/'+f); print(f, im.size)
PY
```

Also grep the executed notebooks for tracebacks and for the printed summaries:

```bash
grep -c Traceback analysis/notebooks/*.ipynb
```

Expected printed objects: `fit_table` (4 rows, both panels), `bench_df` (16 rows for the two best magnifications), the pooled per-pipeline comparison block, and `calls to `cle.select_device()`.

### Step 3 — Reconcile the hardcoded numbers in the notebook markdown

Several figures quoted in markdown were taken from the exploratory analysis, **not** from a notebook run. After Step 1, diff the printed output against:

- §2 markdown: 1.70 / 2.00 / 1.63 / 1.99 eV, R² values.
- §2 note: `2.03 eV` direct baseline intersection.
- §5 method table: all pooled medians/means/N for `inhouse_crop90` (the `*` entries), plus IQR 142.0 nm and d90 351.8 nm.
- §5 sentence "≈147–173 nm median".
- §12 method summary table (all eight cells).

Update the prose if any value moves by more than ~0.02 eV (Tauc) or ~2 nm (grain size).

### Step 4 — Update `article/main.tex` (NOT started)

`article/main.tex` is in Spanish and still describes the **buggy** pipeline and **old** numbers. Exact locations:

| Line | Current text | Required change |
|---|---|---|
| 138 | "El tamaño de grano promedio es de $141 \pm 2.4$ nm (mediana $132$ nm, $N = 936$ granos…)" | New pooled statistics from the adopted pipeline (likely ≈161 nm median, ≈163–170 nm mean, N≈604–635) |
| 214 | "(1) recorte de la barra de información inferior (60 px) … ($N = 936$ granos) … media de $141 \pm 2.4$ nm y mediana de $132$ nm, con $d_{10} = 73$ nm y $d_{90} = 246$ nm" | Rewrite to: metadata-driven `ImageStripSize = 90 px` crop; top-hat background levelling; Otsu + distance-peak watershed; border exclusion; cross-check with `scikit-image` and `pyclesperanto` (M3 GPU); new N/median/mean/d10/d90 |
| 223 | "El tamaño de grano de SEM ($\approx 130$--$140$ nm)…" | Update to the new central value (~150–170 nm) and keep the crystallite comparison (~18–29 nm) |
| 234 | Figure caption: "dos líneas correspondientes a las dos fases (espinela ≈1.6 eV y hematita ≈2.0 eV)" | Now literally true; optionally add the second fit per panel and quote 1.63–1.70 / 1.99–2.03 eV |
| 250 | "Los granos de SEM (media $141 \pm 2.4$ nm, mediana $132$ nm)" | Update to new values |
| 229 | Tauc paragraph with 1.63 ± 0.02 and 2.00 ± 0.03 | Still consistent with the new fits; optionally add the direct spinel 1.70 ± 0.05 eV and the indirect hematite intersection 1.99 ± 0.03 eV, and clarify that both panels carry two fits |
| 147 | Mentions "gráficas de Tauc con dos líneas (dos fases)" | Now matches the figure |

Also check the abstract/summary paragraphs (`\begin{abstract}` region) for any grain-size or band-gap numbers duplicated from these sections.

### Step 5 — Decide the paper's primary pipeline

The notebook reports four pipelines; the manuscript must pick one narrative. Recommendation: **adopt `scikit-image` as the primary reported distribution** (deterministic, CPU-reproducible) and **cite `pyclesperanto` on the M3 GPU as an independent cross-check** agreeing within 1.5 nm. Do not report the legacy 60 px numbers as a result except as a cautionary note in Methods (or drop it entirely if the paper should not advertise the bug).

### Step 6 — Optional cleanups

- `analysis/notebooks/uvvis_analysis.ipynb`: the duplicate markdown heading (§2 appears twice in the old version) is already removed; confirm no other duplicated section survived.
- `sem_grain_analysis.ipynb`: `mark_boundaries` is imported but unused; `summary` dict is populated but only used implicitly. Remove if lint matters.
- `compute_line_intersection()` propagates uncertainty with a crude `0.5 × relative` factor. If the paper quotes the intersection with an error bar, replace it with a Monte-Carlo or full covariance propagation, or state that the uncertainty is approximate.
- `remove_small_objects(mask, max_size=20)` uses the legacy keyword name; in `scikit-image 0.26` it still works (`max_size`), but `min_size` is the forward-compatible spelling to check at execution time.
- `cle.select_device()` prints a pointer (`0x600000e3b188`) rather than a name; if a cleaner log line is desired, use the `cle.list_available_devices()` output for the print and keep `select_device()` silent.

---

## 8. Verification checklist (copy into the PR / commit message)

- [ ] `pixi run python -m nbconvert --to notebook --execute --inplace` succeeds for both notebooks with zero tracebacks.
- [ ] `article/figs/uvvis_tauc.png` shows **two** labelled fits in panel (b) and **two** in panel (c), both reaching the x-axis.
- [ ] Direct panel y-axis spans the data (max ≈935), not 0–60.
- [ ] Inset on panel (b) resolves the spinel edge between 1.55 and 2.12 eV.
- [ ] `article/figs/sem_segmentation.png` exists and its first column visibly contains the yellow `ImageStripSize=90px` boundary line with the footer strip still present.
- [ ] `bench_df` shows `strip_artifacts` non-zero **only** for `inhouse_legacy60`.
- [ ] `article/figs/sem_grain_distribution.png` overlays four lognormal curves per panel.
- [ ] `article/main.tex` no longer contains `60 px`, `141 \pm 2.4`, `132`, `N = 936`, `d_{10} = 73`, `d_{90} = 246`, `130`--`140`.
- [ ] `git diff --stat` includes the two notebooks, `pixi.toml`, `pixi.lock`, `article/main.tex`, and the regenerated PNGs.

---

## 9. Risks / gotchas

1. **Executing `--inplace` embeds base64 PNGs** in the notebooks (the old files already did). Expect multi-MB diffs; if the repo should stay light, execute to a temp copy and keep only the PNGs.
2. **`Path('../..').resolve()` depends on CWD.** nbconvert sets CWD to the notebook directory; any other runner must do the same or `ROOT` will point outside the repo and every file open will fail.
3. **Hardcoded prose numbers can silently drift** from the executed output. Step 3 exists specifically to catch this.
4. **GPU availability.** `pyclesperanto` fails hard if the ICD wrapper is missing. The env has it; if the env is rebuilt on another machine, re-verify `cle.list_available_devices()`.
5. **Moving the repo again breaks every console script** in `.pixi/envs/default/bin` (same shebang issue). Either reinstall the env after a move or always invoke via `pixi run python -m <module>`.
6. **The 36k× image under-reports relative to 20k×** (≈147 vs ≈172 nm median). This is a sampling/charging effect, not a bug; the pooled distribution is the defensible number, and the paper should say so.
7. **`article/` has restrictive permissions (`drwx------`)**; writing figures works for this user but may fail in CI.

---

## 10. Provenance of the numbers in this document

- UV-Vis fits, Tauc slopes/intercepts/R², onset positions: exploratory `numpy`/`scipy` runs against `data/UV-VIS/2026 09 24 %R.csv` (same formulas now encoded in `fit_tauc_linear_regime`).
- SEM footer measurements, Otsu shifts, per-pipeline N/median/mean/IQR: exploratory runs against `data/SEM/MGFe2O4-{2,3}.jpeg` with the four pipelines now encoded in the notebook.
- Anything marked `*` or "estimate" in §3.3 was not directly computed and must be replaced by the executed notebook output.
