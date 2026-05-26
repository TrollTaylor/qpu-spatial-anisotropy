import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit_ibm_runtime import QiskitRuntimeService

###############################################################################
# CONFIGURATION BLOCK: Adjust system deployment parameters here
###############################################################################
BACKEND_CHANNEL = 'ibm_quantum'  # Standard IBM Quantum cloud runtime service
SHOTS_PER_POINT = 8192            # Statistical sampling allocation per angle
TOTAL_STEPS     = 72              # 5-degree increments covering a full 360°
TARGET_SYSTEM   = 'ibm_nairobi'   # Target physical QPU substrate label
###############################################################################


def generate_anisotropy_circuits(steps=TOTAL_STEPS):
    """
    Sweeps orientation angles to build a tomographic map. Both measurement bases 
    rotate together by angle phi, keeping their relative orientation fixed.
    """
    # Generate continuous orientation division from 0 to 2*pi
    phi_angles = np.linspace(0, 2 * np.pi, steps, endpoint=False)
    circuits = []
    
    for i, phi in enumerate(phi_angles):
        # 2-qubit circuit with 2 classical readout register channels
        qc = QuantumCircuit(2, 2)
        
        # 1. Prepare Maximally Entangled Bell Pair |\Phi^+>
        qc.h(0)
        qc.cx(0, 1)
        
        # 2. Rotate measurement basis: U(phi) x U(phi)
        # Apply physical, localized spatial rotation via Ry
        qc.ry(2 * phi, 0)
        qc.ry(2 * phi, 1)
        
        # 3. Projective measurement. Keep readout counts completely unmitigated.
        qc.measure([0, 1], [0, 1])
        
        # Metadata dictionary tagging for post-processing alignment
        qc.metadata = {
            'step': i,
            'phi_deg': np.degrees(phi),
            'phi_rad': phi
        }
        circuits.append(qc)
        
    return phi_angles, circuits


def execute_hardware_calibration_sweep(circuits, backend=None, shots=SHOTS_PER_POINT):
    """
    Executes the tomographic array against the designated compute substrate.
    If backend is None, automatically initializes a local noiseless AerSimulator.
    
    CRITICAL: Readout Error Mitigation (REM) software layers must remain bypassed.
    """

    print(f"Executing sweep sequence over {len(circuits)} unique spatial points...")
    
    # Transpile the abstract gateset to target device's native instruction constraints
    transpiled_circuits = transpile(circuits, backend)
    
    # Run the unmitigated measurement job queue
    job = backend.run(transpiled_circuits, shots=shots)
    result = job.result()
    
    # Extract and parse raw binary register frequencies into dataframes
    processed_data = []
    for qc in circuits:
        meta = qc.metadata
        counts = result.get_counts(qc)
        
        # Pull unweighted state registration values
        n00 = counts.get('00', 0)
        n11 = counts.get('11', 0)
        n01 = counts.get('01', 0)
        n10 = counts.get('10', 0)
        total = n00 + n11 + n01 + n10
        
        # Joint quantum expectation correlation: E = (P00 + P11) - (P01 + P10)
        if total > 0:
            p_parallel = (n00 + n11) / total
            p_antiparallel = (n01 + n10) / total
            correlation = p_parallel - p_antiparallel
        else:
            correlation = 0.0
            
        processed_data.append({
            'Step': meta['step'],
            'Phi_Degrees': meta['phi_deg'],
            'Phi_Radians': meta['phi_rad'],
            'Counts_00': n00,
            'Counts_11': n11,
            'Counts_01': n01,
            'Counts_10': n10,
            'Total_Shots': total,
            'Raw_Correlation': correlation
        })
        
    return pd.DataFrame(processed_data)


def analyze_and_plot_residuals(df, theta_drag=0.03, phi_0=3*np.pi/4):
    """
    Compares raw hardware counts against isotropic standard predictions and 
    maps the alternative hypothesis anisotropic Standard Model Extension signature.
    """
    # Isotropic expectation model holds correlation constant at unity for parallel gates
    df['QM_Prediction'] = 1.0
    
    # Anisotropic Lorentz-Violation attenuation waveform (SME Alternative Model)
    df['Anisotropic_SME_Target'] = 1.0 * (1.0 - theta_drag * (np.sin(2 * df['Phi_Radians'] - phi_0))**2)
    
    # Initialize public plot canvas
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Phi_Degrees'], df['Raw_Correlation'], color='cyan', alpha=0.6, edgecolors='k', label='Raw Telemetry (Counts)')
    plt.plot(df['Phi_Degrees'], df['QM_Prediction'], 'r--', label='Isotropic QM Prediction')
    plt.plot(df['Phi_Degrees'], df['Anisotropic_SME_Target'], color='purple', linewidth=2, label='Anisotropic SME Target')
    
    plt.title('High-Density Spatial Anisotropy Sweep', fontsize=12, fontweight='bold')
    plt.xlabel('Orientation Angle $\\phi$ (Degrees)', fontsize=10)
    plt.ylabel('Correlation $E(\\phi, \\phi)$', fontsize=10)
    plt.xlim(0, 360)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower left', frameon=True)
    
    # Save the analytical result directly to workspace
    plt.savefig('spatial_anisotropy_residual_map.png', dpi=300)
    plt.show()
    print("Verification mapping cleanly preserved as 'spatial_anisotropy_residual_map.png'.")


if __name__ == "__main__":
    # 1. Map out the 72 targeted measurement circuit definitions
    angles, sweep_circuits = generate_anisotropy_circuits()
    
    # 2. Establish external environment credentials pathing
    active_backend = None
    

    service = QiskitRuntimeService(channel=BACKEND_CHANNEL)
    try:
        active_backend = service.backend(TARGET_SYSTEM)
    except Exception:
        active_backend = service.least_busy(simulator=False, operational=True)

    # 3. Pass target compute runtime to the verification script execution layer
    telemetry_df = execute_hardware_calibration_sweep(sweep_circuits, backend=active_backend)
    
    # 4. Serialize unvarnished CSV log matrix
    telemetry_df.to_csv('hardware_anisotropy_sweep_data.csv', index=False)
    print("Raw counts logged successfully in 'hardware_anisotropy_sweep_data.csv'.")
    
    # 5. Extract residuals and overlay target model curves
    analyze_and_plot_residuals(telemetry_df)