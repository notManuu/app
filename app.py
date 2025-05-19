import streamlit as st
import numpy as np
import calculations # Your file with the functions

st.set_page_config(
    page_title="ASEP 8EM1",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Calculadora de Problemas de Ingeniería Eléctrica")
st.markdown("""
Esta aplicación calcula soluciones a varios problemas de ingeniería eléctrica basados en el problemario proporcionado.
Seleccione un problema del menú desplegable y ingrese los parámetros requeridos.
""")

# Sidebar for problem selection
st.sidebar.header("Seleccionar Problema")
problem_options = {
    "2.2: Reactancia Inductiva de un Cable": "problem_2_2",
    "2.7: Inductancia Mutua y Voltaje Inducido (Monofásica y Telefónica)": "problem_2_7",
    "2.8: Inductancia Mutua y Voltaje Inducido (Trifásica y Telefónica)": "problem_2_8",
    "2.9: Reactancia de Línea con Conductores en Haz": "problem_2_9", # Cambiado
    "2.10: Máximo Espaciamiento Permitido": "problem_2_10",
    "2.11: Reactancia de Línea de Doble Circuito": "problem_2_11"
}
selected_problem_display = st.sidebar.selectbox("Problema:", list(problem_options.keys()))
selected_problem_key = problem_options[selected_problem_display]

st.header(f"Resolviendo: {selected_problem_display}")
st.markdown("---")

if selected_problem_key == "problem_2_2":
    st.subheader("Entradas para Problema 2.2")
    st.markdown("Calcule la reactancia inductiva a 50hz y un espaciamiento de 1m, en ohms/km, de un cable constituido por 12 filamentos iguales alrededor de un núcleo no conductor. El diámetro de cada filamento es de 0.25cm y el diámetro exterior del cable es de 1.25cm.")

    col1, col2 = st.columns(2)
    with col1:
        freq_2_2 = st.number_input("Frecuencia (f) en Hz", min_value=1.0, value=50.0, step=1.0, help="Frecuencia del sistema", key="freq_2_2")
        d_spacing_2_2 = st.number_input("Espaciamiento (D) en metros", min_value=0.01, value=1.0, step=0.1, help="Espaciamiento entre conductores", key="d_spacing_2_2")
    with col2:
        num_fil_2_2 = st.number_input("Número de Filamentos", min_value=1, value=12, step=1, help="Total de filamentos", key="num_fil_2_2")
        diam_filament_cm_2_2 = st.number_input("Diámetro de Filamento (cm)", min_value=0.01, value=0.25, step=0.01, disabled=True, key="diam_f_2_2")
        diam_outer_cable_cm_2_2 = st.number_input("Diámetro Exterior Cable (cm)", min_value=0.1, value=1.25, step=0.01, disabled=True, key="diam_oc_2_2")
    st.info("Nota: El cálculo de GMR en el PDF utiliza un $r' = 0.005\\text{m}$ derivado de las dimensiones (0.25cm y 1.25cm) y una fórmula específica para el GMR del cable: $GMR = r' \cdot e^{(1/\text{num_filamentos})}$.")

    if st.button("Calcular Reactancia (Problema 2.2)", key="calc_2_2"):
        xl, gmr = calculations.problem_2_2(freq_2_2, d_spacing_2_2, num_fil_2_2, diam_filament_cm_2_2, diam_outer_cable_cm_2_2)
        st.subheader("Resultados (Problema 2.2):")
        st.markdown(f"**GMR Calculado (según PDF):** ${gmr:.6f} \\text{{m}}$")
        st.markdown(f"**Reactancia Inductiva ($X_L$):** ${{{xl:.5f}}} \\Omega/\\text{{km}}$")
        st.markdown("Fuente: Problema 2.2 del PDF.")

elif selected_problem_key == "problem_2_7":
    st.subheader("Entradas para Problema 2.7")
    st.markdown("Línea eléctrica monofásica (separación $D_p$) y línea telefónica (separación $D_s$) paralelas. Distancia entre conductores más cercanos $D$. Corriente $I$. Frecuencia $f$. Hallar $M$ y $V_{inducido}$.")
    col1, col2, col3 = st.columns(3)
    with col1:
        freq_2_7 = st.number_input("Frecuencia (f) en Hz", min_value=1.0, value=50.0, step=1.0, key="freq_2_7")
        i_current_2_7 = st.number_input("Corriente línea eléctrica (A)", min_value=1.0, value=150.0, step=1.0, key="i_2_7")
    with col2:
        dp_power_spacing_2_7 = st.number_input("Espaciamiento línea eléctrica (Dp) (m)", min_value=0.1, value=2.5, step=0.1, key="dp_2_7")
        ds_tel_spacing_2_7 = st.number_input("Espaciamiento línea telefónica (Ds) (m)", min_value=0.1, value=0.6, step=0.1, key="ds_2_7")
    with col3:
        d_between_lines_2_7 = st.number_input("Distancia entre líneas (D) (m)", min_value=0.1, value=20.0, step=0.1, key="d_btw_2_7")

    if st.button("Calcular $M$ y $V_{ind}$ (Problema 2.7)", key="calc_2_7"):
        m_per_km, v_induced_km, dm_calc, req_calc = calculations.problem_2_7(freq_2_7, i_current_2_7, dp_power_spacing_2_7, ds_tel_spacing_2_7, d_between_lines_2_7)
        st.subheader("Resultados (Problema 2.7):")
        st.markdown(f"**$D_m$ (calculada según PDF):** ${dm_calc:.4f} \\text{{m}}$")
        st.markdown(f"**$r_{{eq}}$ (calculada según PDF):** ${req_calc:.4f} \\text{{m}}$")
        st.markdown(f"**Inductancia Mutua ($M$):** ${{{m_per_km:.6f}}} \\text{{H/km}}$")
        st.markdown(f"**Voltaje Inducido por km ($V_{{ind}}$):** ${{{v_induced_km:.4f}}} \\text{{V/km}}$")
        st.markdown("Fuente: Problema 2.7 del PDF.")

elif selected_problem_key == "problem_2_8":
    st.subheader("Entradas para Problema 2.8")
    st.markdown("Línea telefónica paralela a línea eléctrica trifásica no transpuesta. Corriente $I_{fase}$. Frecuencia $f$. Calcular $L_m$ y $V_{inducido}$.")
    st.markdown("Distancias de fases 'a', 'b', 'c' de la línea eléctrica a la línea telefónica (se asume al centro o GMR de la línea telefónica). La separación interna de la línea telefónica se asume $1\\text{m}$ como en el PDF.")

    col1, col2 = st.columns(2)
    with col1:
        freq_2_8 = st.number_input("Frecuencia (f) en Hz", min_value=1.0, value=50.0, step=1.0, key="freq_2_8")
        current_2_8 = st.number_input("Corriente por fase línea eléctrica (A)", min_value=1.0, value=400.0, step=1.0, key="curr_2_8")
        d_tel_spacing_2_8 = st.number_input("Espaciamiento GMR telefónica (m)", min_value=0.01, value=1.0, step=0.1, key="dtel_2_8", help="PDF usa 1.0m")
    with col2:
        dat_2_8 = st.number_input("Distancia fase 'a' a telefónica (Dat) (m)", min_value=0.1, value=25.5, step=0.1, key="dat_2_8", help="Valor del PDF")
        dbt_2_8 = st.number_input("Distancia fase 'b' a telefónica (Dbt) (m)", min_value=0.1, value=20.5, step=0.1, key="dbt_2_8", help="Valor del PDF")
        dct_2_8 = st.number_input("Distancia fase 'c' a telefónica (Dct) (m)", min_value=0.1, value=15.5, step=0.1, key="dct_2_8", help="Valor del PDF")

    if st.button("Calcular $L_m$ y $V_{ind}$ (Problema 2.8)", key="calc_2_8"):
        lm_km, v_km, d_mt_calc = calculations.problem_2_8(freq_2_8, current_2_8, dat_2_8, dbt_2_8, dct_2_8, d_tel_spacing_2_8)
        st.subheader("Resultados (Problema 2.8):")
        st.markdown(f"**$D_{{mt}}$ (GMD mutua calculada):** ${d_mt_calc:.4f} \\text{{m}}$")
        st.markdown(f"**Inductancia Mutua ($L_m$):** ${{{lm_km:.6f}}} \\text{{H/km}}$")
        st.markdown(f"**Voltaje Inducido por km ($V_{{ind}}$):** ${{{v_km:.4f}}} \\text{{V/km}}$")
        st.markdown("Fuente: Problema 2.8 del PDF.")

elif selected_problem_key == "problem_2_9": # Cambiada la condición del key
    st.subheader("Entradas para Problema 2.9") # Cambiado
    st.markdown("Línea de 500 kV con haz de dos conductores por fase. Calcular $X_L$.")
    st.markdown("Se asume espaciamiento de fase equilátero según la solución del PDF. El PDF se refiere a este problema en el texto como 2.4 pero usa la figura P-2.9.") # Aclaración
    col1, col2 = st.columns(2)
    with col1:
        freq_2_9 = st.number_input("Frecuencia (f) en Hz", min_value=1.0, value=50.0, step=1.0, key="freq_2_9") # key cambiado
        cond_diam_m_2_9 = st.number_input("Diámetro del conductor (m)", min_value=0.001, value=0.03, step=0.001, format="%.3f", key="dcond_2_9", help="PDF usa 0.03m") # key cambiado
    with col2:
        bundle_spacing_m_2_9 = st.number_input("Espaciamiento en el haz (Ds) (m)", min_value=0.01, value=0.5, step=0.01, key="ds_2_9", help="PDF usa 0.5m") # key cambiado
        phase_spacing_m_2_9 = st.number_input("Espaciamiento equilátero de fase (Dm) (m)", min_value=1.0, value=15.0, step=0.1, key="dphase_2_9", help="PDF usa 15m") # key cambiado

    if st.button("Calcular Reactancia $X_L$ (Problema 2.9)", key="calc_2_9"): # Cambiado y key del botón cambiado
        # Llamada a la función con el nuevo nombre
        xl_km, gmr_b_pdf, dm_pdf_calc = calculations.problem_2_9(freq_2_9, cond_diam_m_2_9, bundle_spacing_m_2_9, phase_spacing_m_2_9)
        st.subheader("Resultados (Problema 2.9):") # Cambiado
        st.markdown(f"**$GMR_{{bundle}}$ (calculado según PDF):** ${gmr_b_pdf:.4f} \\text{{m}}$")
        st.markdown(f"**$D_m$ (GMD de fases, equilátero):** ${dm_pdf_calc:.2f} \\text{{m}}$")
        st.markdown(f"**Reactancia Inductiva ($X_L$):** ${{{xl_km:.5f}}} \\Omega/\\text{{km}}$")
        st.markdown("Fuente: Problema 2.9 (originalmente etiquetado como 2.4 con Fig P-2.9) del PDF.") # Cambiado

elif selected_problem_key == "problem_2_10":
    st.subheader("Entradas para Problema 2.10")
    st.markdown("Línea monofásica de 50 km, conductores de 2.56 cm de diámetro. Reactancia total no debe exceder 31.4 $\\Omega$. Determinar máximo espaciamiento permisible D.")
    col1, col2 = st.columns(2)
    with col1:
        line_len_km_2_10 = st.number_input("Longitud de línea (km)", min_value=1.0, value=50.0, step=1.0, key="len_2_10")
        cond_diam_cm_2_10 = st.number_input("Diámetro conductor (cm)", min_value=0.1, value=2.56, step=0.01, key="dcond_2_10")
    with col2:
        max_react_total_2_10 = st.number_input("Máxima Reactancia Total ($\Omega$)", min_value=0.1, value=31.4, step=0.1, key="xtotal_2_10")
        freq_2_10 = st.number_input("Frecuencia (Hz) (para constante 0.1445)", min_value=50.0, value=50.0, step=1.0, key="freq_2_10", disabled=True)

    if st.button("Determinar Espaciamiento Máximo D (Problema 2.10)", key="calc_2_10"):
        cond_diam_m_2_10 = cond_diam_cm_2_10 / 100.0
        spacing_D, xl_km_calc, gmr_pdf_calc = calculations.problem_2_10(line_len_km_2_10, cond_diam_m_2_10, max_react_total_2_10)
        st.subheader("Resultados (Problema 2.10):")
        st.markdown(f"**$X_{{L/km}}$ Calculada:** ${{{xl_km_calc:.4f}}} \\Omega/\\text{{km}}$")
        st.markdown(f"**Radio $r$ (usado como GMR en PDF):** ${gmr_pdf_calc:.4f} \\text{{m}}$")
        st.markdown(f"**Máximo Espaciamiento Permisible (D):** ${spacing_D:.2f} \\text{{m}}$")
        st.markdown("Fuente: Problema 2.10 del PDF.")

elif selected_problem_key == "problem_2_11":
    st.subheader("Entradas para Problema 2.11")
    st.markdown("Dos circuitos trifásicos en una torre. Calcular $X_L$ por fase del sistema combinado.")
    st.markdown("Valores de GMR y GMD según las simplificaciones/datos del PDF.")

    col1, col2, col3 = st.columns(3)
    with col1:
        gmr_sc_m_2_11 = st.number_input("GMR de un solo conductor (m)", min_value=0.001, value=0.005, step=0.001, format="%.3f", key="gmr_sc_2_11", help="PDF: auto GMD 1cm -> r=0.005m")
        dist_aa_m_2_11 = st.number_input("Distancia a-a' (representativa para GMR_fase) (m)", min_value=0.1, value=7.5, step=0.1, key="daa_2_11", help="PDF usa 7.5m para GMR_fase")
    with col2:
        dab_m_2_11 = st.number_input("Distancia GMD $D_{ab}$ (m)", min_value=0.1, value=8.5, step=0.1, key="dab_2_11", help="Valor del PDF")
        dbc_m_2_11 = st.number_input("Distancia GMD $D_{bc}$ (m)", min_value=0.1, value=7.5, step=0.1, key="dbc_2_11", help="Valor del PDF")
    with col3:
        dca_m_2_11 = st.number_input("Distancia GMD $D_{ca}$ (m)", min_value=0.1, value=10.97, step=0.01, key="dca_2_11", help="Valor del PDF")
        freq_2_11 = st.number_input("Frecuencia (Hz)", min_value=50.0, value=50.0, step=1.0, key="freq_2_11", disabled=True)

    st.info("Nota: Las distancias para $GMD_{fase}$ ($D_{ab}, D_{bc}, D_{ca}$) y la distancia representativa $a-a'$ para $GMR_{fase}$ se toman de los cálculos del PDF, que son específicos para la geometría dada en la Fig P-2.11.")

    if st.button("Calcular Reactancia $X_L$ (Problema 2.11)", key="calc_2_11"):
        xl_km_2_11, gmr_phase_c_2_11, gmd_phases_2_11 = calculations.problem_2_11(
            gmr_sc_m_2_11, dist_aa_m_2_11, 10.0, dist_aa_m_2_11,
            dab_m_2_11, dbc_m_2_11, dca_m_2_11, float(freq_2_11)
        )
        st.subheader("Resultados (Problema 2.11):")
        st.markdown(f"**$GMR_{{fase}}$ (combinado, según PDF):** ${gmr_phase_c_2_11:.4f} \\text{{m}}$")
        st.markdown(f"**$GMD_{{fases}}$ (según PDF):** ${gmd_phases_2_11:.4f} \\text{{m}}$")
        st.markdown(f"**Reactancia Inductiva ($X_L$):** ${{{xl_km_2_11:.4f}}} \\Omega/\\text{{km}}$")
        st.markdown("Fuente: Problema 2.11 del PDF.")


st.sidebar.markdown("---")
st.sidebar.markdown("Creado con Streamlit.")
st.sidebar.markdown("Basado en 'Problemas ASEP.pdf'")