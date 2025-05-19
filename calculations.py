# calculations.py
import numpy as np

# ... (funciones problem_2_2, problem_2_7 sin cambios) ...

def problem_2_2(frequency, D_spacing, num_filaments, diameter_filament_cm, diameter_outer_cable_cm):
    """
    Calculates the inductive reactance for Problem 2.2.
    Based on the user-provided PDF.
    """
    r_prime_m = 0.005 # as per document
    gmr = r_prime_m * np.exp(1 / num_filaments) # Calculation from PDF

    if frequency == 50:
        xl = 0.1445 * np.log10(D_spacing / gmr) # Formula from PDF for 50Hz
    else:
        inductance_per_m = 2e-7 * np.log(D_spacing / gmr) # H/m
        xl = 2 * np.pi * frequency * inductance_per_m * 1000 # Ohms/km
    return xl, gmr

def problem_2_7(frequency, I_current, Dp_powerline_spacing, Ds_telephone_spacing, D_between_lines):
    """
    Calculates mutual inductance and induced voltage for Problem 2.7.
    """
    dm_pdf = D_between_lines + (Dp_powerline_spacing / 2) + (Ds_telephone_spacing / 2) # As per PDF calculation
    req_pdf = np.sqrt(Dp_powerline_spacing * Ds_telephone_spacing) # As per PDF calculation

    mutual_inductance_per_m = 2e-7 * np.log(dm_pdf / req_pdf) # H/m, formula from PDF
    mutual_inductance_per_km = mutual_inductance_per_m * 1000 # H/km

    voltage_induced_per_km = 2 * np.pi * frequency * mutual_inductance_per_km * I_current # Formula from PDF
    return mutual_inductance_per_km, voltage_induced_per_km, dm_pdf, req_pdf

def problem_2_8(frequency, current_power_line, d_at_m, d_bt_m, d_ct_m, d_tel_spacing_m=1.0):
    """
    Calculates mutual inductance and induced voltage for Problem 2.8.
    Assumes distances d_at, d_bt, d_ct are to the center/reference of the telephone line bundle.
    d_tel_spacing_m is the GMD of the telephone line itself, PDF uses 1m.
    """
    d_mt = (d_at_m * d_bt_m * d_ct_m)**(1/3)

    mutual_inductance_per_m = 2e-7 * np.log(d_mt / d_tel_spacing_m)
    mutual_inductance_per_km = mutual_inductance_per_m * 1000

    voltage_induced_per_km = 2 * np.pi * frequency * mutual_inductance_per_km * current_power_line
    return mutual_inductance_per_km, voltage_induced_per_km, d_mt

def problem_2_9(frequency, conductor_diameter_m, bundle_spacing_m, phase_spacing_eq_m): # Nombre de función cambiado
    """
    Calculates inductive reactance for Problem 2.9 (formerly referred to as 2.4 Fig P-2.9 in PDF context).
    Assumes 2 conductors per bundle and equilateral phase spacing as per PDF solution.
    """
    radius_m = conductor_diameter_m / 2

    gmr_bundle_pdf = np.sqrt(radius_m * bundle_spacing_m)
    
    d_m_phases = phase_spacing_eq_m

    if frequency == 50:
        xl_per_km = 0.1445 * np.log10(d_m_phases / gmr_bundle_pdf)
    else:
        inductance_per_m = 2e-7 * np.log(d_m_phases / gmr_bundle_pdf) # H/m
        xl_per_km = 2 * np.pi * frequency * inductance_per_m * 1000 # Ohms/km
    return xl_per_km, gmr_bundle_pdf, d_m_phases

def problem_2_10(line_length_km, conductor_diameter_m, max_total_reactance_ohms, frequency=50):
    """
    Determines maximum permissible spacing for a single-phase line.
    """
    xl_per_km = max_total_reactance_ohms / line_length_km
    radius_m = conductor_diameter_m / 2
    gmr_conductor_pdf = radius_m

    if frequency == 50:
        spacing_D_m = gmr_conductor_pdf * (10**(xl_per_km / 0.1445))
    else:
        spacing_D_m = gmr_conductor_pdf * (10**(xl_per_km / 0.1445)) # Assuming 50Hz context for constant
    return spacing_D_m, xl_per_km, gmr_conductor_pdf

def problem_2_11(gmr_single_conductor_m, dist_aa_prime_m, dist_bb_prime_m, dist_cc_prime_m,
                 dab_m, dbc_m, dca_m, frequency=50):
    """
    Calculates reactance per phase for a double circuit line.
    Uses simplified GMRphase and GMD calculations as per PDF.
    """
    gmr_phase_combined = np.sqrt(gmr_single_conductor_m * dist_aa_prime_m)
    
    gmd_phases = (dab_m * dbc_m * dca_m)**(1/3)

    if frequency == 50:
        xl_per_km = 0.1445 * np.log10(gmd_phases / gmr_phase_combined)
    else:
        inductance_per_m = 2e-7 * np.log(gmd_phases / gmr_phase_combined) # H/m
        xl_per_km = 2 * np.pi * frequency * inductance_per_m * 1000 # Ohms/km
    return xl_per_km, gmr_phase_combined, gmd_phases