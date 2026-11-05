## XRD / SEM / UV-VIS-NIR

### 1. XRD (Slide 4): Rietveld Terms, Space Groups, Fit Metrics & Unequivocal Spinel Signal

#### A. What are *"pseudo-Voigt, doblete $\text{K}\alpha_1/\text{K}\alpha_2$, fondo polinomial"*?
In Rietveld refinement, instead of just looking up peak positions like a barcode, the software (**HighScore Plus 3.0**) simulates the **entire continuous diffractogram** ($Y_{\text{calc}}$) point-by-point and adjusts crystal/instrument parameters to match your raw detector counts ($Y_{\text{obs}}$):

1. **Perfil pseudo-Voigt (Peak shape):**
   - A diffraction peak has a finite width and tail shape caused by two things: the **instrument + microstrain** (which produces a bell-shaped **Gaussian** curve, $G$) and the **finite size of nanocrystallites + X-ray spectral width** (which produces a **Lorentzian/Cauchy** curve with wide tails, $L$).
   - Mathematically combining (convolving) a Gaussian and a Lorentzian gives a *Voigt* function, which is computationally slow to integrate thousands of times. A **pseudo-Voigt** is a fast, exact-enough approximation that takes a weighted sum of both:
     $$\text{pV}(2\theta) = \eta\,L(2\theta) + (1 - \eta)\,G(2\theta), \qquad 0 \le \eta \le 1$$
2. **Doblete $\text{K}\alpha_1 / \text{K}\alpha_2$ (X-ray source doublet):**
   - The copper X-ray tube does not emit a single pure wavelength. Due to spin-orbit splitting of copper's $2p \to 1s$ electron transition, it emits a **doublet** of two nearly identical wavelengths:
     - $\text{Cu K}\alpha_1 = 1.54060\text{ \AA}$
     - $\text{Cu K}\alpha_2 = 1.54443\text{ \AA}$ (always at half the intensity of $\text{K}\alpha_1$, ratio $= 0.5$)
   - Because of Bragg's law ($\lambda = 2d\sin\theta$), every single crystal plane $(hkl)$ actually produces **two** peaks right next to each other (more separated at higher $2\theta$). Modeling the $\text{K}\alpha_1/\text{K}\alpha_2$ doublet tells HighScore Plus not to mistake the $\text{K}\alpha_2$ echo for a second phase or extra peak broadening.
3. **Fondo polinomial (Polynomial background):**
   - Look at the vertical axis of [`xrd_highscore.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/xrd_highscore.png): the flat baseline sits around **$\sim 3000\text{--}3400\text{ counts}$**, not zero!
   - Why is the background so high? Because copper X-rays ($\text{Cu K}\alpha \approx 8.04\text{ keV}$) have slightly more energy than the iron K-shell absorption edge ($7.11\text{ keV}$). When $\text{Cu K}\alpha$ hits an iron-rich sample, the iron atoms absorb the X-rays and re-emit **X-ray fluorescence** in all directions, creating a huge, gently curving baseline.
   - Instead of subtracting the background beforehand (which ruins Poisson counting statistics), Rietveld fits a smooth polynomial curve to the baseline simultaneously with the Bragg peaks.

#### B. What are *"Espacio $R\bar{3}c$ (N.º 167)"* and *"Espacio $Fd\bar{3}m$ (N.º 227)"*?
In 3D crystallography, there are **230 possible Space Groups (Grupos Espaciales)** listed in the *International Tables for Crystallography* (numbered 1 to 230). A space group describes the unit cell's Bravais lattice plus all internal rotational, mirror, glide-plane, and screw-axis symmetries.
- **Why does the space group matter in XRD?** Symmetries cause destructive interference (cancellation) for certain $(hkl)$ planes (**systematic absences / reglas de extinción**). A peak can *only* appear if its $(hkl)$ indices obey the space group's rules:
  - **Hematite $\alpha\text{-Fe}_2\text{O}_3$ $\to$ $R\bar{3}c$ (No. 167):** A rhombohedral ($R$) crystal with a 3-fold rotoinversion axis ($\bar{3}$) and axial $c$-glide planes ($c$). In hexagonal axes ($a = b \neq c$, $\alpha=\beta=90^\circ, \gamma=120^\circ$), a reflection $(hkl)$ is **forbidden** unless $-h + k + l = 3n$.
  - **Magnesioferrite $\text{MgFe}_2\text{O}_4$ $\to$ $Fd\bar{3}m$ (No. 227):** The classic cubic spinel structure ($a=b=c$, $\alpha=\beta=\gamma=90^\circ$), which is Face-Centered Cubic ($F$) with diamond glide planes ($d$). A reflection $(hkl)$ is **forbidden** unless $h, k, l$ are Either **all even** (like $220, 400, 422, 440$) or **all odd** (like $111, 311, 511$).

#### C. What are $R_{wp}$, GOF, and $\lambda$?
- **$\lambda = 1.5406\text{ \AA}$:** The X-ray wavelength ($\text{Cu K}\alpha_1$) used to convert diffraction angles $2\theta$ into interplanar distances $d_{hkl}$ via Bragg's Law ($n\lambda = 2d\sin\theta$).
- **$R_{wp}$ (Weighted Profile R-factor $= 1.46\%$ at $400\,^\circ\text{C}$, $1.54\%$ at $600\,^\circ\text{C}$):** The weighted percentage error between the experimental curve $Y_{\text{obs}}$ and the Rietveld model $Y_{\text{calc}}$:
  $$R_{wp} = \sqrt{\frac{\sum_i w_i \left(Y_{\text{obs},i} - Y_{\text{calc},i}\right)^2}{\sum_i w_i\,Y_{\text{obs},i}^2}}, \qquad w_i = \frac{1}{Y_{\text{obs},i}}$$
  *(Tip if a professor asks why $R_{wp} \approx 1.5\%$ is so small: because the denominator sums the raw counts including the $\sim 3000$-count iron fluorescence background, which makes the relative percentage error numerically small.)*
- **GOF (Goodness of Fit $= 0.72$):** Defined in HighScore Plus as $\text{GOF} = \chi^2 = (R_{wp} / R_{\text{exp}})^2$, where $R_{\text{exp}}$ is the theoretical minimum $R_{wp}$ achievable given pure random photon shot noise ($\sqrt{N}$). An ideal refinement has $\text{GOF} \approx 1.0$. A value of $0.72$ means the model fits the data down to the random detector noise floor.

#### D. Explain the *"Señal inequívoca de la espinela"* (Unequivocal Spinel Signal)
Since spinel is only $3.7\text{--}4.7\text{ wt\%}$ of the powder, a skeptical reviewer might ask: *"How do you know $\text{MgFe}_2\text{O}_4$ is really there and not just noise or hematite?"* You have **two bulletproof pieces of evidence** (shown in the inset of [`xrd_highscore.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/xrd_highscore.png)):
1. **The isolated $(220)$ peak at $2\theta = 30.12^\circ\text{--}30.24^\circ$:** By space group $R\bar{3}c$ rules, hematite has **zero allowed reflections** between $(012)$ at $24.13^\circ$ and $(104)$ at $33.14^\circ$. Therefore, the peak at $\sim 30.1^\circ$ is a $100\%$ isolated fingerprint of the cubic spinel phase.
2. **The $(311)$ low-angle shoulder at $35.48^\circ$ in XRD2 ($600\,^\circ\text{C}$):** The strongest peak of any spinel is $(311)$. At $400\,^\circ\text{C}$, spinel $(311)$ sits at $35.62^\circ$, completely buried on top of hematite $(110)$ at $35.61^\circ$. At $600\,^\circ\text{C}$, the spinel unit cell expands, shifting $(311)$ left to **$35.48^\circ$** while hematite $(110)$ stays at **$35.61^\circ$**, resolving $(311)$ as a distinct shoulder on the left flank of $(110)$!

---

### 2. XRD (Slide 5): Scorecard Data Provenance & Lattice Expansion

#### A. Item-by-Item Provenance of the Scorecard (traced via GLM-5.3 subagent)
The scorecard table on Slide 5 ([`generate_deck_v2.py`](file:///Users/rifusaki/localRepos/uni/tcb/generate_deck_v2.py#L607-L617)) and Table 1 in [`article/main.tex`](file:///Users/rifusaki/localRepos/uni/tcb/article/main.tex#L196-L216) combines **two upstream sources**:
1. **HighScore Plus 3.0 Rietveld exports** in [`analysis/highscore/400/`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400.CIF) and [`analysis/highscore/600/`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF) (for phase quantification, $R_{wp}/\text{GOF}$, and unit cell parameters).
2. **In-house Python peak analysis** in [`analysis/notebooks/xrd_rietveld_analysis.ipynb`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/notebooks/xrd_rietveld_analysis.ipynb) (for whole-pattern FWHM, Scherrer $D$, and Williamson–Hall $D$ & $\varepsilon$).

| Scorecard Metric | $400\,^\circ\text{C}$ (XRD1) | $600\,^\circ\text{C}$ (XRD2) | Exact Source & How It Was Calculated |
| :--- | :---: | :---: | :--- |
| **Hematita $\alpha\text{-Fe}_2\text{O}_3$ (% peso)** | $96.3$ | $95.3$ | **HighScore Plus 3.0** ([`400.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400.CIF#L93), [`600.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF#L84)). Computed from the refined phase scale factors $S_p$ using the **Hill–Howard equation**: $$W_p = \frac{S_p Z_p M_p V_p}{\sum_k S_k Z_k M_k V_k}$$ where $Z_p M_p$ is the unit-cell mass ($958.15\text{ u}$ for $\text{Fe}_{12}\text{O}_{18}$; $1599.97\text{ u}$ for $\text{Mg}_8\text{Fe}_{16}\text{O}_{32}$) and $V_p$ is the refined cell volume ($302.40\text{ \AA}^3$ / $582.28\text{ \AA}^3$ at $400\,^\circ\text{C}$; $301.90\text{ \AA}^3$ / $588.73\text{ \AA}^3$ at $600\,^\circ\text{C}$). Exact unrounded output: $96.33\%$ and $95.31\%$. |
| **Espinela $\text{MgFe}_2\text{O}_4$ (% peso)** | $3.7$ | $4.7$ | Complement of the Hill–Howard equation above from [`400.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400.CIF#L384) ($S = 2.9(4)\times 10^{-6} \to 3.67\%$) and [`600.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF#L375) ($S = 3.9(6)\times 10^{-6} \to 4.69\%$). |
| **$R_{wp}$ / GOF** | $1.46\%$ / $0.72$ | $1.54\%$ / $0.72$ | [`400Structures.rtf`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400Structures.rtf) ($R_{wp}=1.46072\%$, $\text{GOF}=0.71542$) and [`600Structures.rtf`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600Structures.rtf) ($R_{wp}=1.54008\%$, $\text{GOF}=0.71894$). |
| **$a$ hematita (\AA)** | $5.0378(8)$ | $5.0358(4)$ | [`400.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400.CIF#L102) & [`600.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF#L93). Note the parentheses notation: $5.0378(8)$ means $5.0378 \pm 0.0008\text{ \AA}$ (uncertainty in the last digit). |
| **$c$ hematita (\AA)** | $13.759(3)$ | $13.746(1)$ | [`400.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400.CIF#L104) & [`600.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF#L95) ($13.759 \pm 0.003\text{ \AA}$ and $13.746 \pm 0.001\text{ \AA}$). |
| **$a$ espinela (\AA)** | $8.350(3)$ | **$8.381(5)$** | [`400.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400.CIF#L393) ($8.350 \pm 0.003\text{ \AA}$) & [`600.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF#L384) ($8.381 \pm 0.005\text{ \AA}$). Since spinel is cubic, $a = b = c$. |
| **FWHM global ($^\circ$)** | $0.474$ | $0.275$ | [`xrd_rietveld_analysis.ipynb`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/notebooks/xrd_rietveld_analysis.ipynb) **Cell 5**: whole-pattern Full Width at Half Maximum from the in-house pseudo-Voigt fit. It drops by $42\%$ ($0.474^\circ \to 0.275^\circ$), meaning peaks become $1.72\times$ sharper at $600\,^\circ\text{C}$. |
| **$D_{\text{Scherrer}}$ (nm)** | $18.2 \pm 0.9$ | $28.7 \pm 1.6$ | [`xrd_rietveld_analysis.ipynb`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/notebooks/xrd_rietveld_analysis.ipynb) **Cell 11**: mean $\pm$ standard error of the mean across 10 individual Gaussian peak fits of hematite reflections, corrected for instrumental broadening ($\beta_{\text{inst}} = 0.05^\circ$). |
| **W–H: $D$ (nm) / $\varepsilon$** | $21 \pm 5$ / $0.0006$ | $76 \pm 30$ / $0.0019$ | [`xrd_rietveld_analysis.ipynb`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/notebooks/xrd_rietveld_analysis.ipynb) **Cell 11 & Cell 13**: linear regression of $\beta\cos\theta$ vs $4\sin\theta/\lambda$ across the same 10 reflections. |

#### B. Explain the Spinel Lattice Expansion (*Expansión de Red*: $a = 8.350 \to 8.381\text{ \AA}$)
1. **Why does the crystal lattice expand chemically?**
   - In an iron-oxide spinel, the octahedral ionic radius of **$\text{Mg}^{2+}$ ($0.72\text{ \AA}$)** is significantly larger than that of **$\text{Fe}^{3+}$ ($0.645\text{ \AA}$)**.
   - At $400\,^\circ\text{C}$ (just above the decomposition temperature of the hydroxides), the spinel lattice is poorly ordered and **$\text{Mg}^{2+}$-deficient** (close to $\gamma\text{-Fe}_2\text{O}_3$ maghemite, which has $a \approx 8.34\text{ \AA}$).
   - When recalcined at $600\,^\circ\text{C}$ for 2 hours, thermal diffusion allows the larger $\text{Mg}^{2+}$ cations to fully incorporate and order into the spinel lattice sites, expanding the cubic cell edge by $\Delta a = +0.031\text{ \AA}$ ($+0.37\%$) to **$a = 8.381\text{ \AA}$** — matching the stoichiometric reference value for $\text{MgFe}_2\text{O}_4$ ($8.38\text{--}8.39\text{ \AA}$).
2. **Why does lattice expansion shift peaks to *smaller* $2\theta$, and what does "anti-correlated" mean?**
   - Look at Bragg's law for a cubic crystal:
     $$\sin\theta = \frac{\lambda}{2\,d_{hkl}} = \frac{\lambda\sqrt{h^2+k^2+l^2}}{2\,a}$$
     Because $a$ is in the **denominator**, when $a$ gets **bigger** ($8.350 \to 8.381\text{ \AA}$), $\sin\theta$ and $2\theta$ must get **smaller** (peaks shift to the left).
   - **Why is this proof against an instrument error ("corrimiento de cero")?** If you accidentally packed the powder $0.1\text{ mm}$ higher or lower in the sample holder during XRD2, *every* peak in the pattern (both hematite and spinel) would shift in the same direction by the same amount. Instead:
     - At $\sim 35.5^\circ$: Spinel $(311)$ shifts left ($35.62^\circ \to 35.48^\circ$), moving **away** from hematite $(110)$ ($35.61^\circ$) to create a left shoulder. *(Note: in `main.tex` line 190, $\Delta 2\theta = 0.13^\circ$ refers to the $35.61^\circ - 35.48^\circ = 0.134^\circ$ separation between the two peaks at $600\,^\circ\text{C}$; the shift of $(311)$ itself is $35.624^\circ - 35.476^\circ = 0.148^\circ \approx 0.15^\circ$.)*
     - At $\sim 62.5^\circ$: Spinel $(440)$ sits to the right of hematite $(214)$ ($62.42^\circ$). When spinel expands, $(440)$ shifts left ($62.90^\circ \to 62.63^\circ$), moving **closer** to hematite $(214)$.
     - One spinel peak moves *away* from its hematite neighbor while another moves *toward* its hematite neighbor. That geometric opposition makes it $100\%$ certain that the spinel lattice physically expanded.

---

### 3. XRD (Slide 6): Crystallite Size Methods — Scherrer vs. Williamson–Hall

#### A. How the Two Methods Work
When X-rays hit a huge, perfect crystal, constructive interference happens *only* at the exact Bragg angle $\theta$, and any slight deviation $\theta \pm \delta\theta$ is immediately canceled out by destructive interference from thousands of deep atomic planes — producing a razor-thin peak.
In a real nanopowder, peaks broaden ($\beta = \sqrt{\text{FWHM}^2 - \beta_{\text{inst}}^2}$, in radians) for **two different physical reasons**:

1. **Finite Crystallite Size ($D$):** If the crystal is only $\sim 20\text{ nm}$ thick, there aren't enough atomic planes to completely cancel out rays slightly off the Bragg angle. This broadening varies as $1/\cos\theta$:
   $$\beta_{\text{size}} = \frac{K\lambda}{D\cos\theta} \quad \Longrightarrow \quad \text{\textbf{Scherrer Equation: }} D = \frac{K\lambda}{\beta\cos\theta} \quad (K \approx 0.9)$$
   *Limitation:* Scherrer assumes microstrain is zero ($\varepsilon = 0$). If the crystal also has internal strain, $\beta$ is larger, so Scherrer **underestimates** $D$.
2. **Microstrain ($\varepsilon = \Delta d / d$):** If crystal defects, dislocations, or thermal stresses stretch and compress $d_{hkl}$ locally inside the nanoparticle, a single plane spacing $d$ becomes a spread $d \pm \Delta d$. Differentiating Bragg's law shows this broadening grows steeper with angle, as $\tan\theta$:
   $$\beta_{\text{strain}} = 4\,\varepsilon\tan\theta$$
3. **Williamson–Hall (W–H) Method:** Combines both effects additively ($\beta_{\text{total}} = \beta_{\text{size}} + \beta_{\text{strain}}$) and multiplies both sides by $\cos\theta$ to get a straight line $y = b + m x$:
   $$\underbrace{\beta\cos\theta}_{y} = \underbrace{\frac{K\lambda}{D}}_{\text{intercept } b} + \underbrace{(\varepsilon\lambda)}_{\text{slope } m}\,\underbrace{\left(\frac{4\sin\theta}{\lambda}\right)}_{x}$$
   - Plotting $\beta\cos\theta$ vs. $4\sin\theta/\lambda$ (right panel of [`xrd_size.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/xrd_size.png)): the **slope** gives the microstrain $\varepsilon$, and the **$y$-intercept** gives the size $D = K\lambda / b$.

#### B. Why Calculate Williamson–Hall if We Primarily Present Scherrer for Crystallite Size?
There are three scientific reasons why you need both, and why **Scherrer** ($18.2 \to 28.7\text{ nm}$) is the headline size number while **W–H** is used to report $\varepsilon$:
1. **W–H validates Scherrer at $400\,^\circ\text{C}$:** At $400\,^\circ\text{C}$ (blue line in [`xrd_size.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/xrd_size.png)), the W–H slope is flat within error ($\varepsilon = 0.0006 \pm 0.0010 \approx 0$). That *proves* microstrain is negligible at $400\,^\circ\text{C}$, which is why $D_{\text{Scherrer}} = 18.2 \pm 0.9\text{ nm}$ and $D_{\text{W--H}} = 21 \pm 5\text{ nm}$ agree!
2. **W–H detects new lattice strain at $600\,^\circ\text{C}$:** At $600\,^\circ\text{C}$ (red line), the W–H plot tilts upward with a statistically significant slope ($\varepsilon = 0.0019 \pm 0.0004$), proving that thermal sintering and cation rearrangement at $600\,^\circ\text{C}$ introduce internal lattice strain.
3. **Why W–H's size $D = 76 \pm 30\text{ nm}$ is noisy whereas Scherrer's $D = 28.7 \pm 1.6\text{ nm}$ is precise:** In W–H, $D = K\lambda / b$ is inversely proportional to the $y$-intercept $b$. As crystals grow larger and peaks sharpen at $600\,^\circ\text{C}$, the $y$-intercept $b$ gets very close to zero ($b \approx 0.0018\text{ rad}$). When you divide by a number near zero, even tiny scatter in the 10 data points causes a huge propagated error ($\pm 30\text{ nm}$, or $40\%$ uncertainty!). Scherrer averages $\beta\cos\theta$ directly without extrapolating to $x=0$, giving a tight $\pm 1.6\text{ nm}$ error bar (representing the *effective/apparent* coherent diffraction domain size).

---

### 4. SEM-EDS (Slide 7): Is Mg Underestimated or Genuinely Low? & Polycrystalline Clusters

#### A. Are we underestimating Mg, or is there genuinely that little Mg in the powder?
**Both are happening simultaneously**, and doing a quick mass balance between XRD and EDS makes the whole story click together:

1. **There is genuinely very little Mg left in the solid powder (lost during synthesis):**
   - You weighed the precursors in the exact $1:2$ molar ratio for $\text{MgFe}_2\text{O}_4$, which theoretically has **$55.85\text{ wt\% Fe}$**, **$12.15\text{ wt\% Mg}$**, and **$32.00\text{ wt\% O}$** (a stoichiometric mass ratio of **$\text{Fe:Mg} = 4.60 : 1$**).
   - However, during co-precipitation with $\text{NH}_4\text{OH}$ at $\text{pH } 10\text{--}11$, $\text{Fe}^{3+}$ precipitates completely ($K_{\text{sp}} \approx 10^{-38}$, insoluble above $\text{pH } 3$), whereas $\text{Mg}(\text{OH})_2$ ($K_{\text{sp}} \approx 5.6 \times 10^{-12}$) is much more soluble. Worse, the $\text{NH}_4^+$ ions produced in the reaction buffer the solution and form soluble $\text{Mg}^{2+}$–ammonium complexes, and the 3 centrifugation washes with distilled water dissolve even more $\text{Mg}(\text{OH})_2$ into the decanted supernatant!
   - **Check the XRD mass balance:** Rietveld XRD shows your final powder is only **$3.7\text{--}4.7\text{ wt\%}$ $\text{MgFe}_2\text{O}_4$** and $95.3\text{--}96.3\text{ wt\%}$ $\alpha\text{-Fe}_2\text{O}_3$ (with no $\text{MgO}$). Since $\text{Mg}$ is $12.15\text{ wt\%}$ of $\text{MgFe}_2\text{O}_4$, a powder containing $3.7\text{--}4.7\text{ wt\%}$ spinel actually contains only:
     $$w_{\text{Mg, real}} = (3.7\% \text{ to } 4.7\%) \times 0.1215 = \mathbf{0.45\text{ to }0.57\text{ wt\% Mg}}$$
     So ~95% of the initial $\text{Mg}^{2+}$ really was lost in the liquid supernatant during precipitation/washing, leaving a true bulk $\text{Fe:Mg}$ ratio of $\sim 120:1$ to $150:1$!
2. **Why we also say EDS underestimates / struggles to detect Mg:**
   - Look at the EDS uncertainty in [`main.tex`](file:///Users/rifusaki/localRepos/uni/tcb/article/main.tex#L259): **$\text{Mg} = 0.9 \pm 1.1\text{ wt\%}$** ($\text{Fe:Mg} \approx 69:1$). The uncertainty ($\pm 1.1\%$) is larger than the measured number ($0.9\%$)!
   - Why? In EDS at $30\text{ kV}$, the low-energy **$\text{Mg K}\alpha$ X-ray line ($1.253\text{ keV}$)** is heavily absorbed by the surrounding heavy iron matrix (ZAF matrix absorption effect) and sits right on the noisy Bremsstrahlung background tail next to the huge $\text{O K}\alpha$ ($0.525\text{ keV}$) and $\text{Fe L}\alpha$ ($0.705\text{ keV}$) peaks (see [`sem_eds.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/sem_eds.png)).
   - **Takeaway for your presentation:** Most of the $\text{Mg}^{2+}$ was genuinely lost in the aqueous supernatant (which is *why* hematite is the $95\text{--}96\%$ majority phase in XRD!), and the remaining $< 1\text{ wt\%}$ $\text{Mg}$ in the spinel sits right at the physical detection limit of EDS ($\text{Mg K}\alpha$ at $1.253\text{ keV}$), which is why Slide 10 proposes **ICP-OES/AAS** to close the exact mass balance.

#### B. How did we identify "Polycrystalline Clusters" (*Cúmulos Policristalinos*)?
You didn't need high-resolution TEM to prove the grains are polycrystalline clusters — you proved it by comparing **SEM** against **XRD**:
- **XRD Scherrer ($D_{\text{XRD}} = 18.2\text{--}28.7\text{ nm}$)** measures the size of a **single coherent crystal domain (cristalito)** — a region where the atomic planes are uninterrupted and point in the exact same direction. XRD cannot "see" the outer boundary of a particle if several nanocrystals are fused together at different angles.
- **SEM segmentation ($d_{50} = 161\text{ nm}$, mean $163\text{--}171\text{ nm}$)** measures the outer physical diameter of the **visible grains (granos/partículas)** using secondary electrons.
- Since each SEM grain ($\approx 161\text{ nm}$) is **$6\text{ to }9\times$ wider** in linear diameter than an individual XRD crystallite ($161 / 28.7 \approx 5.6$ and $161 / 18.2 \approx 8.8$), a $161\text{ nm}$ SEM grain **cannot** be a single crystal. Each SEM grain is a **polycrystalline cluster (aglomerado policristalino)** formed by $\sim 6\text{--}9$ crystallites across its diameter (hundreds in 3D volume) that nucleated and sintered together during co-precipitation and calcination.

---

### 5. UV-Vis-NIR (Slide 8): Regime A vs. Band Gap, Direct vs. Indirect Tauc & Regime B Slope Check

#### A. How do we know Regime A ($1.10\text{--}1.45\text{ eV}$) is NOT our band gap?
Contrasting with literature values ($\alpha\text{-Fe}_2\text{O}_3 \approx 2.0\text{--}2.2\text{ eV}$, $\text{MgFe}_2\text{O}_4 \approx 1.6\text{--}1.9\text{ eV}$) is one check, but you can actually tell **directly from the physics of your spectrum** in Panel (a) of [`uvvis_tauc.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/uvvis_tauc.png) in **three independent ways**:

1. **Peak shape vs. Step/Plateau shape (The #1 giveaway):**
   - Look at the green shaded region (Regime A, $1.10\text{--}1.45\text{ eV}$) in Panel (a): $F(R_\infty)$ rises from $0.8$ to a small **hill/peak** of $\sim 2.4$ around $1.38\text{ eV}$ ($\sim 900\text{ nm}$) and **then goes back down** at $1.45\text{--}1.55\text{ eV}$!
   - A true semiconductor **band gap (interband transition)** promotes electrons from the valence band into a continuous conduction band: once photon energy exceeds $E_g$, absorption shoots up like a **wall/step** and **stays high** for all higher energies (like Regime B, which shoots up to $F(R_\infty) \approx 13\text{--}15$ and stays there from $2.3$ to $3.5\text{ eV}$).
   - Anything that goes up and comes back down is a **localized transition between discrete energy levels**, specifically the internal **$d\text{--}d$ crystal-field (ligand-field) transition** ${}^6A_{1g} \to {}^4T_{1g}$ of octahedral $\text{Fe}^{3+}$ ions!
2. **Absorption intensity ($F(R_\infty)$ magnitude):**
   - Regime A reaches only $F(R_\infty) \approx 2.4$, whereas Regime B reaches $F(R_\infty) \approx 14\text{--}15$. That is because $\text{Fe}^{3+}$ ($3d^5$) $d\text{--}d$ transitions are quantum-mechanically **spin-forbidden and parity-forbidden** (Laporte rule), making them much weaker than the allowed $\text{O }2p \to \text{Fe }3d$ charge-transfer band gap in Regime B.
3. **Visual color of your powder:**
   - Visible light spans $1.77\text{ eV}$ ($700\text{ nm}$, red) to $3.10\text{ eV}$ ($400\text{ nm}$, violet). If your powder had a true band gap of $0.80\text{--}1.12\text{ eV}$ (in the near-infrared), it would strongly absorb *all* visible light and look **pitch black** (like silicon, $E_g = 1.12\text{ eV}$). Because your powder is **reddish-brown** (reflecting red/orange below $\sim 2.0\text{ eV}$ and absorbing green/blue above $2.0\text{ eV}$), the true interband edge *must* be around $1.6\text{--}2.0\text{ eV}$ (Regime B).

#### B. Difference Between Direct ($n=2$) and Indirect ($n=1/2$) Tauc — and Why Include Both?
In the Kubelka–Munk Tauc equation, $(F(R_\infty)\,h\nu)^n = A(h\nu - E_g)$:
- **Direct Tauc ($n = 2$, Panel b):** Assumes the highest valence-band state and lowest conduction-band state have the **same crystal momentum ($\mathbf{k}$)**. The electron jumps straight across the gap by absorbing **only a photon**. Absorption turns on very abruptly ($\alpha h\nu \propto (h\nu - E_g)^{1/2}$, so squaring both sides with $n=2$ makes it a straight line).
- **Indirect Tauc ($n = 1/2$, Panel c):** Assumes the valence-band maximum and conduction-band minimum are at **different crystal momenta ($\mathbf{k}$)**. To conserve momentum, the electron must simultaneously absorb **a photon AND a phonon (lattice vibration)**. This two-particle process turns on more gradually ($\alpha h\nu \propto (h\nu - E_g)^2$, so taking the square root $n=1/2$ makes it a straight line).

**Why include both?**
1. **Electronic nature of iron oxides:** Hematite ($\alpha\text{-Fe}_2\text{O}_3$) and magnesioferrite ($\text{MgFe}_2\text{O}_4$) are famous for having **both** an indirect phonon-assisted onset ($\sim 1.9\text{--}2.0\text{ eV}$ in hematite) and a slightly higher direct charge-transfer onset ($\sim 2.0\text{--}2.2\text{ eV}$), and literature papers report both.
2. **Each exponent visually highlights one of your two phases:**
   - Squaring the data ($n=2$) blows up large values ($13^2 \to 1000$) and squashes small values, so the majority **hematite** edge ($2.00\text{ eV}$) dominates the main plot, while the minority **spinel** foot ($1.70\text{ eV}$) requires the zoomed inset to be seen.
   - Taking the square root ($n=1/2$) compresses the vertical scale ($0$ to $6$), making the lower absorption baseline ($1.78\text{--}2.00\text{ eV}$) and the main edge clearly visible on the same axes so you can apply **Makuła's baseline-intersection method** (where the $y=0$ intercept gives the minority spinel onset at $1.61\text{ eV}$ and the baseline intersection gives the majority hematite onset at $1.96\text{ eV}$). Showing that **both** $n=2$ and $n=1/2$ yield the exact same two band gaps ($1.61\text{--}1.70\text{ eV}$ and $1.96\text{--}2.03\text{ eV}$) makes your two-phase conclusion rock-solid.

### 6. Can We Illustrate a Biphasic Structure in VESTA?

**Yes — and you already have the exact `.CIF` files in your repo to do it!**

#### A. First: What does "Biphasic" mean at the atomic scale?
A very common point of confusion is thinking that a "biphasic crystal structure" means a single hybrid unit cell where $\alpha\text{-Fe}_2\text{O}_3$ and $\text{MgFe}_2\text{O}_4$ are merged into one lattice. **It does not!**
- At the unit-cell scale ($\sim 0.5\text{--}1.4\text{ nm}$), the two crystal structures are completely separate:
  1. One set of nanocrystallites has the **trigonal/hexagonal Hematite lattice** ($R\bar{3}c$, No. 167).
  2. The other set of nanocrystallites has the **cubic Spinel lattice** ($Fd\bar{3}m$, No. 227).
- Inside your $\sim 161\text{ nm}$ polycrystalline SEM clusters, individual $18\text{--}29\text{ nm}$ nanocrystals of Hematite and Spinel are sintered side-by-side sharing grain boundaries. Because X-ray wavelengths ($\lambda = 1.5406\text{ \AA}$) are tiny compared to the nanocrystals, the X-ray beam diffracts from millions of crystallites of both phases at the same time, superimposing both patterns on your detector.

---

### 7. Can HighScore Plus Calculate FWHM, Scherrer, and Williamson–Hall?

**Yes, HighScore Plus *is* capable of all three — and checking your [`400Structures.rtf`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400Structures.rtf) and [`600Structures.rtf`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600Structures.rtf) files reveals why your project used the Python notebook for Scherrer/W–H instead.**

#### A. How HighScore Plus Models Peak Width (The Caglioti Equation)
In a full Rietveld refinement, HighScore Plus does not fit every peak's width independently. Instead, it models how $\text{FWHM}$ changes across the diffractogram angle $2\theta$ using the **Caglioti formula**:
$$\text{FWHM}^2(2\theta) = U\tan^2\theta + V\tan\theta + W$$
where:
- **$W$** sets the baseline peak width (angle-independent).
- **$U$ and $V$** control how much the peaks widen as $2\theta$ increases (which is what captures **crystallite size** $\propto 1/\cos\theta$ and **microstrain** $\propto \tan\theta$!).

#### B. What Happened in Your HighScore Plus Refinement (`400.CIF` & `600.CIF`)
If you look at lines 85–87 of [`600.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF#L85-L87) (and [`400Structures.rtf`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/400/400Structures.rtf)), when HighScore Plus was run:
- **$W$ was refined**, giving:
  - Hematite ($400\,^\circ\text{C}$): $W = 0.189(5)$
  - Hematite ($600\,^\circ\text{C}$): $W = 0.046(1)$
- **However, $U$ and $V$ were left turned off (fixed at `0.000000`)!**

Look at the mathematical consequence of setting $U = 0$ and $V = 0$ in $\text{FWHM}^2 = U\tan^2\theta + V\tan\theta + W$:
1. **HighScore's FWHM became a constant ($\text{FWHM} = \sqrt{W}$) for every peak of a phase:**
   - At $400\,^\circ\text{C}$: $\text{FWHM}_{\text{HSP}} = \sqrt{0.189} = \mathbf{0.435^\circ}$ for every single Hematite peak.
   - At $600\,^\circ\text{C}$: $\text{FWHM}_{\text{HSP}} = \sqrt{0.046} = \mathbf{0.215^\circ}$ for every single Hematite peak (see [`600.CIF`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/highscore/600/600.CIF#L443-L472) where every `PH00` peak lists `0.2152`!).
   - Compare that to your Python notebook's whole-pattern FWHM (**$0.474^\circ \to 0.275^\circ$**): they tell the exact same physical story (peaks sharpen by $\sim 42\text{--}50\%$ after recalcination at $600\,^\circ\text{C}$).
2. **What if we calculate Scherrer from HighScore's $\text{FWHM} = \sqrt{W}$ at the main $(104)$ peak ($2\theta = 33.14^\circ$)?**
   - At $400\,^\circ\text{C}$ ($\text{FWHM} = 0.4352^\circ$): **$D_{\text{HSP}} = 19.2\text{ nm}$** (almost identical to your Python notebook's **$18.2 \pm 0.9\text{ nm}$**!).
   - At $600\,^\circ\text{C}$ ($\text{FWHM} = 0.2152^\circ$): **$D_{\text{HSP}} = 39.5\text{ nm}$** (slightly larger than the notebook's $28.7 \pm 1.6\text{ nm}$ because high-angle peaks in XRD2 are wider than $0.215^\circ$ due to strain).
3. **Why you *cannot* get Williamson–Hall from those current HighScore exports:**
   - Williamson–Hall ($\beta\cos\theta = \frac{K\lambda}{D} + 4\varepsilon\sin\theta$) requires measuring how $\beta$ **increases with angle $\theta$** across individual reflections.
   - Because $U=0$ and $V=0$ in the saved HighScore run, HighScore forced $\beta$ to be constant across all angles! If you plot a constant $\beta$ times $\cos\theta$ vs. $4\sin\theta/\lambda$, $\beta\cos\theta$ automatically slopes *downward* (giving an impossible negative microstrain $\varepsilon < 0$) simply because $\cos\theta$ decreases with $\theta$.
   - That is why your Python notebook ([`xrd_rietveld_analysis.ipynb`](file:///Users/rifusaki/localRepos/uni/tcb/analysis/notebooks/xrd_rietveld_analysis.ipynb) Cell 11) had to fit the 10 Hematite peaks **individually** without the $U=V=0$ constraint so each peak $(hkl)$ could have its true experimental width, making the Williamson–Hall plot possible!
   - *(Fun fact: Look at the last bullet of your article [`main.tex` line 291](file:///Users/rifusaki/localRepos/uni/tcb/article/main.tex#L291) under "Próximos pasos": **"Refinar con HighScore Plus añadiendo orientación preferida (March–Dollase) y parámetros de tamaño/deformación."** That bullet is referring to turning on Caglioti $U, V$ / Size-Strain analysis inside HighScore Plus!)*

---

### 8. The Rietveld "Parameter Correlation" Trap (Why it crashes or gives garbage)
Rietveld refinement is a non-linear least-squares minimization of dozens of coupled variables at the same time.

In the Caglioti formula:
$$\text{FWHM}^2(2\theta) = U\tan^2\theta + V\tan\theta + W$$

$U$, $V$, and $W$ are **heavily mathematically correlated**. 
- If you check `Refine U`, `Refine V`, and `Refine W` all at once—especially in a **biphasic sample** where one phase is only $\approx 4\%$ (Spinel)—the least-squares matrix almost always **diverges, produces negative widths, or crashes**. 
- The software might make $U$ huge and $V$ negative to compensate, resulting in unphysical parameters that have zero physical meaning.

Because of this, every standard Rietveld protocol teaches you a strict **hierarchy of refinement**:
1. Zero shift + Scale factor + Background polynomial.
2. Unit cell parameters ($a, c$).
3. Peak shape / basic width ($W$).
4. **Stop here** unless you have a dedicated calibration to do more.

---

### 9. The Big Requirement: An Instrumental Standard ($\text{LaB}_6$ or $\text{Si}$)
To do real crystallite size and microstrain modeling directly inside HighScore Plus, the software needs to know:
$$\text{Broadening}_{\text{measured}} = \text{Broadening}_{\text{instrument}} + \text{Broadening}_{\text{sample}}$$

If you tell HighScore to refine size and strain from $U, V, W$:
- **How does HighScore know how much of the peak width came from your $20\text{ nm}$ nanocrystals, versus the diffractometer's optics (slits, detector resolution, beam divergence)?**
- It **can't**, unless you first run a certified coarse-grained microcrystalline reference standard (like **$\text{LaB}_6$ NIST SRM 660** or **Si NIST SRM 640**, which have zero microstrain and crystal size $> 2\text{ }\mu\text{m}$) on that exact Bruker D8 machine with the exact same slits, and load that instrument calibration file into HighScore.

Without an instrumental calibration file loaded into HighScore, letting it refine $U$ and $V$ would just be guessing.

---

### 10. Why Doing It in Python Was Actually the Better Move
Instead of dealing with HighScore's black-box multi-parameter matrix, your project did what most research groups do:

1. **HighScore was used for what it does best:** 
   - Unit cell parameters ($a, c$) and quantitative phase fraction (Hill–Howard $S \cdot Z \cdot M \cdot V$), which are rock-solid.
2. **The Python notebook was used for Size and Strain:**
   - It fitted the 10 Hematite peaks individually, cleanly subtracted the instrument width ($\beta_{\text{inst}} = 0.05^\circ$ for the LynxEye detector), and plotted **Scherrer** and **Williamson–Hall** transparently.
   - Any reviewer or professor can inspect the line, slope, and intercept directly in [`xrd_size.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/xrd_size.png), rather than having to trust a black-box parameter buried in HighScore.

---

### Summary: How to Frame This in Your Defense / Presentation
If a professor asks: *"Why didn't you refine size-strain directly in HighScore Plus?"*

You have the perfect answer:
> *"We kept $U$ and $V$ fixed and refined $W$ in HighScore Plus to avoid parameter correlation and ensure numerical stability in our two-phase refinement. To determine crystallite size and strain without coupling artifacts, we conducted an independent Williamson–Hall and Scherrer analysis across the 10 main reflections in Python, leaving full instrumental-deconvoluted size-strain tensor modeling in HighScore as future work."*

---

### 11. What is Strain, Exactly?

In solid-state physics and XRD, you have to distinguish between **macro-deformación** and **micro-deformación**:

```
Ideal Crystal Lattice:          Uniform Macro-strain:           Non-uniform Micro-strain (ε):
d  d  d  d  d                   d'   d'   d'   d'   d'          d-Δd   d+Δd   d    d+Δd  d-Δd
|  |  |  |  |                   |    |    |    |    |           |      |      |    |     |
●──●──●──●──●                   ●────●────●────●────●           ●──────●──●───●────●─────●
(All d identical -> sharp peak) (All d shifted -> peak moves)   (Spread of d -> peak broadens)
```

1. **Macro-strain (Deformación macroscópica):**
   - The entire sample is uniformly stretched or compressed (e.g., thermal expansion or external bending).
   - *XRD effect:* Every plane spacing $d$ expands or contracts by the exact same amount ($d \to d'$). The diffraction peak does **not** broaden; it simply **shifts** position to a new angle $2\theta$.

2. **Micro-strain ($\varepsilon = \Delta d / d$, Deformación microscópica / interna):**
   - This is what Williamson–Hall measures. It is the **local, sub-nanometer fluctuation of interplanar spacing** from one unit cell to the next inside the nanocrystallite.
   - *Where does it come from?*
     - Point defects (missing atoms / vacancies).
     - Cation size mismatch ($\text{Mg}^{2+}$ is larger than $\text{Fe}^{3+}$, so inserting it stretches nearby bonds while compressing others).
     - Nanograin boundaries and surface tension/surface relaxation in tiny crystals.
   - *XRD effect:* In region 1, the planes have spacing $d + \Delta d$; in region 2, they have $d - \Delta d$. Because Bragg's law is $\lambda = 2d\sin\theta$, taking the derivative gives:
     $$\Delta(2\theta) = 4\left(\frac{\Delta d}{d}\right)\tan\theta = 4\,\varepsilon\tan\theta$$
   - Since different parts of the same crystallite diffract at slightly different angles $\theta \pm \Delta\theta$, the peak **broadens symmetrically**. That spread is microstrain $\varepsilon$.

---

### 12. Manually (Numerically and Physically), What is Done to the Data in Scherrer and W–H?

Here is the step-by-step recipe that was executed on your raw counts:

#### Step 0: The Instrumental Correction (Deconvolución)
- **Physical reality:** The machine's optical slit widths, beam divergence, and detector pixel size widen peaks even if you put a perfect, infinite diamond in the holder. For your Bruker D8 / LynxEye, that machine width is $\beta_{\text{inst}} \approx 0.05^\circ$.
- **Numerical step:** For each of the 10 hematite peaks, HighScore/Python fits the peak with a bell curve and finds its observed width $\text{FWHM}_{\text{obs}}$ (in degrees). The sample's genuine broadening $\beta$ is obtained by Pythagorean subtraction and converted to radians:
  $$\beta = \sqrt{\text{FWHM}_{\text{obs}}^2 - \beta_{\text{inst}}^2} \quad \left[\text{converted to radians: } \beta_{\text{rad}} = \beta \times \frac{\pi}{180}\right]$$

---

#### Step 1: Scherrer Method
- **Physical premise:** It assumes internal microstrain is zero ($\varepsilon = 0$). Peak width is assumed to be $100\%$ caused by finite crystallite size $D$.
- **Numerical calculation:** For each of the 10 peaks at position $\theta$ (half of $2\theta$):
  $$D = \frac{K\,\lambda}{\beta_{\text{rad}}\,\cos\theta}$$
  where $K = 0.9$ (crystallite shape factor) and $\lambda = 1.5406\text{ \AA} = 0.15406\text{ nm}$.
- **Final result:** You calculate $D$ for all 10 peaks and compute the mean and standard error:
  - $400\,^\circ\text{C}$: **$D = 18.2 \pm 0.9\text{ nm}$**
  - $600\,^\circ\text{C}$: **$D = 28.7 \pm 1.6\text{ nm}$**

---

#### Step 2: Williamson–Hall (W–H) Method
- **Physical premise:** Broadening comes from *both* finite size ($1/\cos\theta$) and microstrain ($\tan\theta$) simultaneously:
  $$\beta_{\text{total}} = \beta_{\text{size}} + \beta_{\text{strain}} = \frac{K\lambda}{D\cos\theta} + 4\varepsilon\tan\theta$$
- **Linearization:** Multiply the whole equation by $\cos\theta$ ($\text{since } \tan\theta\cos\theta = \sin\theta$):
  $$\underbrace{\beta\cos\theta}_{y} = \underbrace{\frac{K\lambda}{D}}_{\text{intercept } b} + \underbrace{(\varepsilon\lambda)}_{\text{slope } m}\,\underbrace{\left(\frac{4\sin\theta}{\lambda}\right)}_{x}$$
- **Numerical calculation (Linear Regression $y = mx + b$):**
  - For each of your 10 peaks, compute:
    $$y_i = \beta_i\cos\theta_i \qquad x_i = \frac{4\sin\theta_i}{\lambda}$$
  - Fit a straight line through the 10 $(x_i, y_i)$ points (as shown in the right panel of [`xrd_size.png`](file:///Users/rifusaki/localRepos/uni/tcb/article/figs/xrd_size.png)):
    - **Microstrain $\varepsilon$:** comes from the **slope** $m$: $\varepsilon = m / \lambda$.
    - **Crystallite size $D$:** comes from the **$y$-intercept** $b$: $D = K\lambda / b$.
  - At $400\,^\circ\text{C}$, the slope is flat ($m \approx 0 \implies \varepsilon = 0.0006 \pm 0.0010$, negligible). At $600\,^\circ\text{C}$, the line visibly tilts upward ($m > 0 \implies \varepsilon = 0.0019 \pm 0.0004$, real strain).

---

### 13. What Does Network Parameter Expansion Mean, Physically?

The **parámetro de red** ($a$) is the physical edge length of the unit cell (the repeating microscopic "brick" of the crystal).

```
Spinel unit cell at 400 °C:               Spinel unit cell at 600 °C:
a = 8.350 Å                               a = 8.381 Å (+0.37% linear expansion)
┌─────────────┐                           ┌───────────────┐
│  Fe3+       │                           │  Fe3+   Mg2+  │
│  (0.645 Å)  │  + 600 °C thermal energy  │  (0.720 Å)    │  Volume swells by +1.1%
│             │  ======================>  │  (swells cage)│
└─────────────┘                           └───────────────┘
Deficient, disordered                     Equilibrium stoichiometric ordering
```

1. **Volume swelling:**
   Because spinel is cubic ($V = a^3$), an increase from $a = 8.350\text{ \AA}$ to $a = 8.381\text{ \AA}$ means the unit-cell volume expands from $582.3\text{ \AA}^3 \to 588.7\text{ \AA}^3$ (**$+1.1\%$ volume expansion**).
2. **The atomic mechanism:**
   - At $400\,^\circ\text{C}$, the spinel phase has just crystallized from the amorphous hydroxide precursor. It is **cation-deficient** and disordered, with many empty vacancies and dominated by smaller $\text{Fe}^{3+}$ ions ($r_{\text{ionic}} = 0.645\text{ \AA}$). Its cell ($a \approx 8.35\text{ \AA}$) is contracted, resembling maghemite ($\gamma\text{-Fe}_2\text{O}_3$, $a \approx 8.34\text{ \AA}$).
   - At $600\,^\circ\text{C}$, high temperature provides the thermal activation energy needed for the larger $\text{Mg}^{2+}$ cations ($r_{\text{ionic}} = 0.720\text{ \AA}$) to diffuse into their equilibrium tetrahedral and octahedral interstitial cages.
   - Forcing larger $\text{Mg}^{2+}$ ions into the coordination polyhedra pushes the surrounding $\text{O}^{2-}$ anions outward, stretching all bond lengths and expanding the whole crystal lattice to its true bulk equilibrium value ($a = 8.381\text{ \AA}$).

---

### 14. What Does FWHM Decrease Mean, Physically?

$\text{FWHM}$ is **Full Width at Half Maximum** (ancho a media altura del pico). In your scorecard, FWHM dropped from **$0.474^\circ$ at $400\,^\circ\text{C}$ to $0.275^\circ$ at $600\,^\circ\text{C}$** (a $42\%$ drop; peaks became $1.7\times$ sharper).

- **Physical mechanism:**
  - Diffraction peaks are created by **constructive wave interference** of X-rays bouncing off parallel crystal planes.
  - In a crystal with infinite planes, constructive interference occurs *only* at the exact Bragg angle $\theta_B$. If you move just $0.001^\circ$ away from $\theta_B$, the 10,000th plane deep inside cancels out the 1st plane by perfect destructive interference, making the peak razor-sharp.
  - In an $18\text{ nm}$ nanocrystal ($400\,^\circ\text{C}$), there are only $\sim 50\text{--}70$ atomic planes. There are simply **not enough planes** to completely destroy the waves slightly off $\theta_B$, so the peak stays broad and fat.
  - When you heat to $600\,^\circ\text{C}$, smaller particles sinter together into larger crystallites ($29\text{ nm}$), increasing the number of coherent planes. Destructive interference becomes much stricter.
- **Takeaway:** **FWHM decrease = nanocrystals grew larger (crystallite growth) and internal atomic ordering improved (higher crystallinity).**

---

### 15. Why $\alpha\text{-Fe}_2\text{O}_3$?

There are two reasons to explain:

#### A. Why the Greek letter "$\alpha$"? (Polymorphism of Iron Oxide)
Iron(III) oxide ($\text{Fe}_2\text{O}_3$) can crystallize into four distinct geometric arrangements (polymorphs):
1. **$\alpha\text{-Fe}_2\text{O}_3$ (Hematite):** Hexagonal/rhombohedral ($R\bar{3}c$). It is the **thermodynamic champion**—the most stable form of iron oxide in the universe at standard temperature and pressure.
2. **$\gamma\text{-Fe}_2\text{O}_3$ (Maghemite):** Cubic defect spinel ($Fd\bar{3}m$). It is metastable. If you heat it above $\sim 400\,^\circ\text{C}$, it converts irreversibly into $\alpha\text{-Fe}_2\text{O}_3$.
3. **$\beta\text{-Fe}_2\text{O}_3$ and $\varepsilon\text{-Fe}_2\text{O}_3$:** Rare laboratory polymorphs.

#### B. Why did $\alpha\text{-Fe}_2\text{O}_3$ form in your sample instead of pure spinel?
- In your reaction, you dissolved $1\text{ Mg} : 2\text{ Fe}$. But because $\text{Mg(OH)}_2$ is soluble while $\text{Fe(OH)}_3$ is totally insoluble, **$\sim 95\%$ of the $\text{Mg}^{2+}$ was lost in the water wash**.
- This left you with an overwhelming excess of $\text{Fe(OH)}_3$ precipitate.
- During calcination at $400\,^\circ\text{C}$ and $600\,^\circ\text{C}$, the iron hydroxide dehydrates:
  $$2\,\text{Fe(OH)}_3 \xrightarrow{\Delta} \alpha\text{-Fe}_2\text{O}_3 + 3\,\text{H}_2\text{O}$$
- Because $400\text{--}600\,^\circ\text{C}$ is well above the activation barrier, the pure iron oxide automatically crystallizes into its lowest-energy thermodynamic ground state: **$\alpha\text{-Fe}_2\text{O}_3$ (Hematite)**.

---

### 16. What are "Transiciones de Campo Ligando" (Ligand Field Transitions) for the Non-Band-Gap Transition?

This is one of the most elegant chemistry questions you might get asked about Slide 8.

```
Free Fe3+ ion in vacuum:            Fe3+ inside Hematite/Spinel Octahedron:
(All 5 d-orbitals equal energy)     (O2- electron clouds repel d-orbitals unequally)

                                                 ┌───┐ ┌───┐  eg (dx2-y2, dz2)  [point at ligands]
                                                   ↑     ↑
───────── 5 d-orbitals ─────────    =======>     ────────────────  Δo (Ligand field splitting ~1.2 eV)
                                                   ↑     ↑     ↑
                                                 ┌───┐ ┌───┐ ┌───┐  t2g (dxy, dyz, dxz) [point between]
```

#### A. Where Does the "Field" Come From?
- In an isolated $\text{Fe}^{3+}$ atom floating in space, all five of its $3d$ electron orbitals have the exact same energy (they are degenerate).
- In hematite or spinel, each $\text{Fe}^{3+}$ is trapped in an octahedron surrounded by **six negative $\text{O}^{2-}$ ions (ligands)**.
- The negative electron clouds of the oxygen atoms push against the iron's $3d$ electrons (**campo ligando** / ligand field).
- Because two orbitals ($d_{x^2-y^2}, d_{z^2} \to e_g$) point directly at the oxygens, they feel high repulsion and rise in energy. The other three orbitals ($d_{xy}, d_{yz}, d_{xz} \to t_{2g}$) point between the oxygens, so they sit at lower energy.
- The energy gap between them is the **ligand field splitting energy $\Delta_o \approx 1.2\text{ eV}$**.

#### B. The Transition (${}^6A_{1g} \to {}^4T_{1g}$)
- In high-spin $\text{Fe}^{3+}$ ($3d^5$), there is one electron in each orbital: $(t_{2g})^3 (e_g)^2$, ground state notation **${}^6A_{1g}$**.
- When you shine **near-infrared light ($1.10\text{--}1.45\text{ eV}$)** on the powder, an electron absorbs that photon and flips/rearranges between these split $d$-orbitals into the excited state **${}^4T_{1g}$**.

#### C. Why is this NOT a Band Gap?
| Property | Ligand Field Transition (Regime A: $1.1\text{--}1.4\text{ eV}$) | True Band Gap (Regime B: $1.8\text{--}2.4\text{ eV}$) |
| :--- | :--- | :--- |
| **What happens?** | **Intra-atomic hop:** An electron hops between split $d$-orbitals *within the same iron atom*. | **Interband charge transfer:** An electron is completely torn from an oxygen valence band ($\text{O } 2p$) and sent to the iron conduction band ($\text{Fe } 3d$). |
| **Electron mobility** | The electron is **bound** to the atom. It cannot move through the crystal to conduct electricity. | The electron is **free**. It creates electrical conductivity and photocatalytic electron-hole pairs. |
| **Spectral shape** | Rises and **falls** back down like a hump/peak ($F(R)$ peaks at $\sim 2.4$ and drops). | Rises like a **step/wall** ($F(R) \approx 14$) and stays elevated for all higher energies. |