# QPU Spatial Anisotropy & Lorentz Violation Characterization Suite

An open-access metrology protocol designed to execute high-density tomographic sweeps on quantum information processing substrates (QPUs). By systematically deactivating software-level Readout Error Mitigation (REM) layers, this suite isolates raw telemetry count matrices to search for orientation-dependent spatial anisotropy or local Lorentz Invariance Violation (LIV) within the framework of the Standard Model Extension (SME).

---

## 1. Overview of the Experimental Protocol

Standard device-independent verification metrics assume a continuous, perfectly isotropic spacetime background. This protocol introduces a targeted, 72-point symmetric co-rotating tomographic sweep ($5^\circ$ angular steps over a full $360^\circ$ spatial range) to map the unmitigated residual probability delta:

$$\Delta P(\phi) = P_{\text{quantum}} - P_{\text{raw}}$$

By evaluating raw coincidences across a physical spatial sweep, the toolkit provides statistical boundary criteria to differentiate stochastic hardware cross-talk from a phase-locked, quadrupolar harmonic modulation curve:

$$P_{\text{raw}}(\phi) \propto [1 - \theta_{\text{drag}} \cdot \sin^2(2\phi - \phi_0)]$$

---

## 2. Dependencies and Quickstart Installation

This package requires Python 3.9+ and standard scientific data manipulation stacks along with the current Qiskit ecosystem primitives.

```bash
# Clone the operational toolkit
git clone [https://github.com/yourusername/qpu-anisotropy-suite.git](https://github.com/yourusername/qpu-anisotropy-suite.git)
cd qpu-anisotropy-suite

# Install requisite packages
```
```
pip install -r requirements.txt
```

## 3. Usage Guidelines
3.1 Hardware DeploymentThe primary execution script, qpu_anisotropy_sweep.py, is configured for direct hardware interaction.
  Configure: Edit the TARGET_SYSTEM variable at the top of the script to match your specific QPU substrate (e.g., 'ibm_nairobi').Execute: Run the sweep directly via terminal:Bashpython qpu_anisotropy_sweep.py
  Hardware Mandate: Ensure all automated software readout error mitigation (REM) layers are explicitly bypassed in your environment, as these algorithms will systematically average out the geometric signal of interest.

## 4. Analytical OutputsUpon execution, the diagnostic engine generates two primary artifacts:
  hardware_anisotropy_sweep_data.csv: A raw, unweighted count ledger recording registration counts ($n_{00}, n_{11}, n_{01}, n_{10}$) alongside absolute laboratory orientation angles ($\phi$).
  spatial_anisotropy_residual_map.png: A comparative mapping plot displaying physical raw telemetry against the standard isotropic null hypothesis baseline and the anisotropic SME target model.

## 5. References
[1] L. Shalm, et al. "A strong loophole-free test of local realism." Physical Review Letters (2015). 
[2] R. D. Gill. "Optimal statistical analyses of Bell experiments." arXiv:2209.00702 [quant-ph] (2023).
[3] D. Kostelecký and N. Russell. "Data Tables for Lorentz and CPT Violation." Reviews of Modern Physics.
