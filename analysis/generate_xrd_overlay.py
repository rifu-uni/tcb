import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import re
from pathlib import Path

# Publication-grade typography and style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['xtick.minor.size'] = 3.5
plt.rcParams['ytick.minor.size'] = 3.5

ROOT = Path('.').resolve()
CIF_400 = ROOT / 'analysis/highscore/400/400.CIF'
CIF_600 = ROOT / 'analysis/highscore/600/600.CIF'
OUT_PNG = ROOT / 'article/figs/xrd_highscore.png'
OUT_DECK = ROOT / 'article/figs/deck/xrd_highscore.png'

def parse_cif(cif_path):
    with open(cif_path) as f:
        text = f.read()

    loop_match = re.search(r'loop_\s+_pd_meas_intensity_total\s+_pd_proc_intensity_bgk_calc\s+_pd_calc_intensity_total([\s\S]*?)(?:loop_|#|\Z)', text)
    lines = loop_match.group(1).strip().splitlines()
    data = []
    for l in lines:
        parts = l.split()
        if len(parts) >= 3:
            data.append([float(x) for x in parts[:3]])
    arr = np.array(data)

    tt_min_m = re.search(r'_pd_proc_2theta_range_min\s+([\d\.]+)', text)
    tt_inc_m = re.search(r'_pd_proc_2theta_range_inc\s+([\d\.]+)', text)
    tt_min = float(tt_min_m.group(1)) if tt_min_m else 20.0
    tt_inc = float(tt_inc_m.group(1)) if tt_inc_m else 0.03
    tt = tt_min + np.arange(len(arr)) * tt_inc

    # Reflections
    refln_match = re.search(r'loop_\s+_refln_index_h\s+_refln_index_k\s+_refln_index_l\s+_pd_refln_phase_id\s+_refln_observed_status\s+_refln_F_squared_calc\s+_refln_F_squared_meas\s+_refln_phase_calc\s+_pd_refln_i100_meas\s+_pd_refln_peak_id([\s\S]*?)(?:loop_|#|\Z)', text)
    reflections = []
    if refln_match:
        for line in refln_match.group(1).strip().splitlines():
            line = line.strip()
            if not line or line.startswith('_') or line.startswith('#'): continue
            parts = line.split()
            if len(parts) >= 10:
                h, k, l = int(parts[0]), int(parts[1]), int(parts[2])
                phase_id = parts[3]
                i100 = float(parts[8])
                pk_id = parts[9]
                reflections.append({
                    'h': h, 'k': k, 'l': l,
                    'phase_id': phase_id,
                    'i100': i100,
                    'pk_id': pk_id
                })

    # Peaks
    peak_match = re.search(r'loop_\s+_pd_peak_id\s+_pd_peak_2theta_centroid\s+_pd_peak_d_spacing\s+_pd_peak_pk_height\s+_pd_peak_width_2theta([\s\S]*?)loop_', text)
    peaks = {}
    if peak_match:
        for line in peak_match.group(1).strip().splitlines():
            line = line.strip()
            if not line or line.startswith('_') or line.startswith('#'): continue
            parts = line.split()
            if len(parts) >= 5:
                pk_id = parts[0]
                peaks[pk_id] = {
                    '2theta': float(parts[1]),
                    'd': float(parts[2]),
                    'height': float(parts[3]),
                    'fwhm': float(parts[4])
                }

    for r in reflections:
        if r['pk_id'] in peaks:
            r.update(peaks[r['pk_id']])

    return {
        'tt': tt,
        'y_obs': arr[:, 0],
        'y_bkg': arr[:, 1],
        'y_calc': arr[:, 2],
        'y_diff': arr[:, 0] - arr[:, 2],
        'reflections': reflections
    }

d400 = parse_cif(CIF_400)
d600 = parse_cif(CIF_600)

# Colors
C_OBS = '#222222'
C_CALC = '#E53935'    # crisp red
C_DIFF = '#455A64'    # slate blue
C_HEM = '#B71C1C'     # dark crimson
C_SPINEL = '#0D47A1'  # vibrant royal blue

fig, axes = plt.subplots(2, 1, figsize=(12, 11), sharex=False, gridspec_kw={'hspace': 0.28})

# Custom staggered annotations for zero-collision layout
ANNOTATION_CONFIG_400 = {
    (24.13, 'PH00'): (0, 160, '(012)'),
    (30.24, 'PH01'): (0, 220, '(220)'),
    (33.13, 'PH00'): (0, 180, '(104)'),
    (35.61, 'PH00'): (0.5, 180, '(110)'),
    (35.62, 'PH01'): (-0.5, 360, '(311)*'),
    (40.83, 'PH00'): (0, 160, '(113)'),
    (43.30, 'PH01'): (-0.35, 260, '(400)'),
    (43.48, 'PH00'): (0.35, 160, '(202)'),
    (49.43, 'PH00'): (0, 160, '(024)'),
    (54.03, 'PH00'): (0, 160, '(116)'),
    (57.55, 'PH00'): (0, 180, '(018)'),
    (62.40, 'PH00'): (-0.5, 170, '(214)'),
    (62.90, 'PH01'): (0.1, 320, '(440)'),
    (63.96, 'PH00'): (0.5, 170, '(300)'),
    (71.89, 'PH00'): (0, 160, '(1 0 10)'),
    (75.41, 'PH00'): (0, 160, '(220)'),
}

ANNOTATION_CONFIG_600 = {
    (18.30, 'PH01'): (0, 220, '(111)'),
    (24.13, 'PH00'): (0, 180, '(012)'),
    (30.12, 'PH01'): (0, 240, '(220)'),
    (33.14, 'PH00'): (0, 200, '(104)'),
    (35.48, 'PH01'): (-0.6, 380, '(311)'),
    (35.61, 'PH00'): (0.6, 180, '(110)'),
    (40.84, 'PH00'): (0, 180, '(113)'),
    (43.12, 'PH01'): (-0.35, 260, '(400)'),
    (43.49, 'PH00'): (0.35, 180, '(202)'),
    (49.45, 'PH00'): (0, 180, '(024)'),
    (53.50, 'PH01'): (-0.35, 260, '(422)'),
    (54.06, 'PH00'): (0.35, 180, '(116)'),
    (57.03, 'PH01'): (-0.35, 280, '(511)'),
    (57.59, 'PH00'): (0.35, 180, '(018)'),
    (62.42, 'PH00'): (-0.5, 180, '(214)'),
    (62.63, 'PH01'): (0.0, 340, '(440)'),
    (63.98, 'PH00'): (0.5, 180, '(300)'),
    (71.95, 'PH00'): (0, 180, '(1 0 10)'),
}

def plot_panel(ax, d, title, wt_hem, wt_spinel, rwp, gof, ann_config, is_600=False):
    tt = d['tt']
    y_obs = d['y_obs']
    y_calc = d['y_calc']
    y_diff = d['y_diff']
    
    diff_offset = 2400
    y_diff_plot = y_diff + diff_offset
    
    # Profiles
    ax.plot(tt, y_obs, '.', color=C_OBS, ms=2.4, alpha=0.55, label=r'Observado ($Y_{\mathrm{obs}}$)')
    ax.plot(tt, y_calc, '-', color=C_CALC, lw=1.3, label=r'Rietveld ($Y_{\mathrm{calc}}$)')
    ax.plot(tt, y_diff_plot, '-', color=C_DIFF, lw=0.75, label=r'Diferencia ($Y_{\mathrm{obs}} - Y_{\mathrm{calc}}$)')
    ax.axhline(diff_offset, color=C_DIFF, lw=0.5, ls='--', alpha=0.6)

    # Bragg ticks
    hem_ticks = [r['2theta'] for r in d['reflections'] if r['phase_id'] == 'PH00' and '2theta' in r]
    spinel_ticks = [r['2theta'] for r in d['reflections'] if r['phase_id'] == 'PH01' and '2theta' in r]
    
    tick_y_hem = diff_offset + 250
    tick_y_spin = diff_offset + 120
    
    ax.plot(hem_ticks, [tick_y_hem]*len(hem_ticks), '|', color=C_HEM, ms=7.5, markeredgewidth=1.3, label=r'Bragg $\alpha$-Fe$_2$O$_3$ (Hexagonal)')
    ax.plot(spinel_ticks, [tick_y_spin]*len(spinel_ticks), '|', color=C_SPINEL, ms=7.5, markeredgewidth=1.3, label=r'Bragg MgFe$_2$O$_4$ (Espinela)')

    # Labels
    for (t_ref, phase), (dx, dy, lbl) in ann_config.items():
        matches = [r for r in d['reflections'] if r['phase_id'] == phase and '2theta' in r and abs(r['2theta'] - t_ref) < 0.2]
        t = matches[0]['2theta'] if matches else t_ref
        y_pos = np.interp(t, tt, y_calc)
        col = C_SPINEL if phase == 'PH01' else C_HEM
        
        ax.annotate(lbl,
                    xy=(t, y_pos),
                    xytext=(t + dx, y_pos + dy),
                    ha='center', va='bottom',
                    fontsize=8.5, fontweight='bold', color=col,
                    arrowprops=dict(arrowstyle='-', color=col, lw=0.7, alpha=0.75))

    # Generous limits so all peak labels have ample headroom without hitting borders
    ax.set_xlim(17.5 if is_600 else 19.5, 80)
    ax.set_ylim(2100, 7000 if is_600 else 5600)
    ax.set_ylabel('Intensidad (cuentas)', fontsize=12, fontweight='bold')
    
    # Place panel information as an elegant title outside the data area (NO collision with peaks!)
    chi2_val = f"{float(gof)**2:.2f}"
    panel_title = (f"$\\mathbf{{{title}}}$: "
                   f"● Hematita $\\mathbf{{{wt_hem}\\%}}$ peso ($R\\bar{{3}}c$)  |  "
                   f"◆ Magnesioferrita $\\mathbf{{{wt_spinel}\\%}}$ peso ($Fd\\bar{{3}}m$)  —  "
                   f"$R_{{wp}} = {rwp}\\%$, $\\chi^2 = {chi2_val}$")
    ax.set_title(panel_title, fontsize=11, fontweight='bold', loc='left', pad=10)

# Plot panels
plot_panel(axes[0], d400, "XRD1 (400 °C) — Calcinación", "96.3", "3.7", "1.46", "0.72", ANNOTATION_CONFIG_400, is_600=False)
axes[0].set_xlabel(r'Posición $2\theta$ ($^\circ$)', fontsize=11, fontweight='bold')

plot_panel(axes[1], d600, "XRD2 (600 °C) — Recalcinación", "95.3", "4.7", "1.54", "0.72", ANNOTATION_CONFIG_600, is_600=True)
axes[1].set_xlabel(r'Posición $2\theta$ ($^\circ$, radiación Cu K$\alpha$, $\lambda = 1.54060$ Å)', fontsize=12, fontweight='bold')

# Legend on top panel (placed at upper right where peaks are small baseline, completely unobstructed)
handles = [
    Line2D([0], [0], marker='.', color=C_OBS, lw=0, ms=6, label=r'Observado ($Y_{\mathrm{obs}}$)'),
    Line2D([0], [0], color=C_CALC, lw=1.5, label=r'Rietveld ($Y_{\mathrm{calc}}$)'),
    Line2D([0], [0], color=C_DIFF, lw=1.0, label=r'Diferencia ($Y_{\mathrm{obs}} - Y_{\mathrm{calc}}$)'),
    Line2D([0], [0], marker='|', color=C_HEM, lw=0, ms=10, markeredgewidth=1.5, label=r'Bragg $\alpha$-Fe$_2$O$_3$ (Hexagonal)'),
    Line2D([0], [0], marker='|', color=C_SPINEL, lw=0, ms=10, markeredgewidth=1.5, label=r'Bragg MgFe$_2$O$_4$ (Espinela)')
]
axes[0].legend(handles=handles, loc='upper right', fontsize=9.5, framealpha=0.95, edgecolor='#CFD8DC')

# Inset on 600 °C panel: Zoom on 29° to 37.2° region
# Placed in the upper right quadrant of the panel (x: 52% to 96%, y: 44% to 94%)
ax_ins = axes[1].inset_axes([0.52, 0.44, 0.45, 0.50])
tt600 = d600['tt']
y_obs600 = d600['y_obs']
y_calc600 = d600['y_calc']

m_ins = (tt600 >= 29.0) & (tt600 <= 37.2)
ax_ins.plot(tt600[m_ins], y_obs600[m_ins], '.', color=C_OBS, ms=3.5, alpha=0.65)
ax_ins.plot(tt600[m_ins], y_calc600[m_ins], '-', color=C_CALC, lw=1.5)

# Annotate peaks in inset with carefully placed leader lines
ax_ins.annotate("MgFe$_2$O$_4$ (220)\n30.12° (aislado diagnóstico)",
                xy=(30.12, 3050), xytext=(30.25, 4150),
                ha='left', fontsize=8, fontweight='bold', color=C_SPINEL,
                arrowprops=dict(arrowstyle='->', color=C_SPINEL, lw=1.0))

ax_ins.annotate("Hematita (104)\n33.14° (100%)",
                xy=(33.14, 5920), xytext=(32.5, 4900),
                ha='center', fontsize=8, fontweight='bold', color=C_HEM,
                arrowprops=dict(arrowstyle='->', color=C_HEM, lw=1.0))

ax_ins.annotate("MgFe$_2$O$_4$ (311)\n35.48° (convolucionado)",
                xy=(35.48, 4000), xytext=(34.5, 5600),
                ha='center', fontsize=8, fontweight='bold', color=C_SPINEL,
                arrowprops=dict(arrowstyle='->', color=C_SPINEL, lw=1.0))

ax_ins.annotate("Hematita (110)\n35.61°",
                xy=(35.61, 4600), xytext=(36.3, 5600),
                ha='center', fontsize=8, fontweight='bold', color=C_HEM,
                arrowprops=dict(arrowstyle='->', color=C_HEM, lw=1.0))

ax_ins.set_xlim(29.1, 37.1)
ax_ins.set_ylim(2750, 6400)
ax_ins.set_title("Detalle: Pico diagnóstico (220) de espinela y región (110)", fontsize=8.5, fontweight='bold', pad=4)
ax_ins.tick_params(labelsize=7.5)

# Inset indicator box with clean subtle styling
axes[1].indicate_inset_zoom(ax_ins, edgecolor='#37474F', alpha=0.4, lw=1.0)

fig.subplots_adjust(left=0.08, right=0.98, top=0.96, bottom=0.065, hspace=0.28)
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
OUT_DECK.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT_PNG, dpi=300)
fig.savefig(OUT_DECK, dpi=300)
print(f"Successfully generated {OUT_PNG} and {OUT_DECK}")

# --- Generate Individual Ultra-High-Resolution Deck Hero Plots ---
# 1. XRD1 400 °C Single Panel
fig400, ax400 = plt.subplots(figsize=(11.5, 5.8))
plot_panel(ax400, d400, "XRD1 (400 °C) — Calcinación", "96.3", "3.7", "1.46", "0.72", ANNOTATION_CONFIG_400, is_600=False)
ax400.set_xlabel(r'Posición $2\theta$ ($^\circ$, radiación Cu K$\alpha$, $\lambda = 1.54060$ Å)', fontsize=12, fontweight='bold')
ax400.legend(handles=handles, loc='upper right', fontsize=9.5, framealpha=0.95, edgecolor='#CFD8DC')
fig400.subplots_adjust(left=0.08, right=0.98, top=0.93, bottom=0.12)
out_400 = OUT_DECK.parent / 'xrd_highscore_400.png'
fig400.savefig(out_400, dpi=300)
print(f"Successfully generated {out_400}")

# 2. XRD2 600 °C Single Panel (with high-detail inset)
fig600, ax600 = plt.subplots(figsize=(11.5, 5.8))
plot_panel(ax600, d600, "XRD2 (600 °C) — Recalcinación", "95.3", "4.7", "1.54", "0.72", ANNOTATION_CONFIG_600, is_600=True)
ax600.set_xlabel(r'Posición $2\theta$ ($^\circ$, radiación Cu K$\alpha$, $\lambda = 1.54060$ Å)', fontsize=12, fontweight='bold')
ax600.set_ylim(2100, 7600)  # Extra headroom so inset does not touch peak annotations

# Inset on 600 °C placed high and wide
ax_ins600 = ax600.inset_axes([0.48, 0.50, 0.49, 0.46])
ax_ins600.plot(tt600[m_ins], y_obs600[m_ins], '.', color=C_OBS, ms=3.5, alpha=0.65)
ax_ins600.plot(tt600[m_ins], y_calc600[m_ins], '-', color=C_CALC, lw=1.5)

ax_ins600.annotate("MgFe$_2$O$_4$ (220)\n30.12° (aislado diagnóstico)",
                   xy=(30.12, 3050), xytext=(30.25, 4150),
                   ha='left', fontsize=8, fontweight='bold', color=C_SPINEL,
                   arrowprops=dict(arrowstyle='->', color=C_SPINEL, lw=1.0))

ax_ins600.annotate("Hematita (104)\n33.14° (100%)",
                   xy=(33.14, 5920), xytext=(32.5, 4900),
                   ha='center', fontsize=8, fontweight='bold', color=C_HEM,
                   arrowprops=dict(arrowstyle='->', color=C_HEM, lw=1.0))

ax_ins600.annotate("MgFe$_2$O$_4$ (311)\n35.48° (convolucionado)",
                   xy=(35.48, 4000), xytext=(34.5, 5600),
                   ha='center', fontsize=8, fontweight='bold', color=C_SPINEL,
                   arrowprops=dict(arrowstyle='->', color=C_SPINEL, lw=1.0))

ax_ins600.annotate("Hematita (110)\n35.61°",
                   xy=(35.61, 4600), xytext=(36.3, 5600),
                   ha='center', fontsize=8, fontweight='bold', color=C_HEM,
                   arrowprops=dict(arrowstyle='->', color=C_HEM, lw=1.0))

ax_ins600.set_xlim(29.1, 37.1)
ax_ins600.set_ylim(2750, 6400)
ax_ins600.set_title("Detalle: Pico diagnóstico (220) de espinela y región (110)", fontsize=8.5, fontweight='bold', pad=4)
ax_ins600.tick_params(labelsize=7.5)
ax600.indicate_inset_zoom(ax_ins600, edgecolor='#37474F', alpha=0.4, lw=1.0)

fig600.subplots_adjust(left=0.08, right=0.98, top=0.93, bottom=0.12)
out_600 = OUT_DECK.parent / 'xrd_highscore_600.png'
fig600.savefig(out_600, dpi=300)
print(f"Successfully generated {out_600}")
