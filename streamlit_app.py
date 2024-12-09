import streamlit as st
import numpy as np
import pandas as pd

# Title and introduction
st.title("CBAM Impact Analysis Visualizations")
st.write("This dashboard dynamically demonstrates the key models and formulas with enhanced graphs and wider parameter ranges.")

# Sidebar for input parameters
st.sidebar.title("Input Parameters")

# Default values
default_emissions = 50.0
default_output = 100.0
default_delta_y = 20.0
identity_matrix = 1.0
mrio_coeff = 0.8  # Fixed dummy value
default_wage_vector = 2.0  # Fixed dummy value
default_employment_vector = 3.0  # Fixed dummy value

# Adjustable inputs using sliders (with wider ranges)
emissions = st.sidebar.slider("Total Emissions", min_value=0.0, max_value=500.0, value=default_emissions, step=5.0)
output = st.sidebar.slider("Total Output", min_value=0.0, max_value=500.0, value=default_output, step=5.0)
delta_y = st.sidebar.slider("Direct Impact (deltaY)", min_value=0.0, max_value=500.0, value=default_delta_y, step=5.0)

# Fixed values
i = identity_matrix  # Identity matrix (fixed)
a = mrio_coeff  # MRIO Technical Coefficient (dummy fixed)

# Emission intensity formula
if output != 0:
    emission_intensity = emissions / output
else:
    emission_intensity = 0

# Total output change (deltaX)
try:
    delta_x = (i - a) ** -1 * delta_y
except ZeroDivisionError:
    delta_x = 0

# Wage and employment impact formulas
delta_w = default_wage_vector * delta_x
delta_n = default_employment_vector * delta_x

# Dynamic visualization functions
def update_emission_intensity_chart(output, emissions):
    emission_data = pd.DataFrame({
        'Output': np.linspace(0, max(output, 1), 100),
        'Emission Intensity': np.linspace(0, 500, 100) * (emissions / max(output, 1))
    })
    st.line_chart(emission_data.set_index('Output'), use_container_width=True)

def update_output_change_chart(delta_y, a):
    output_change_data = pd.DataFrame({
        'deltaY': np.linspace(0, max(delta_y, 1), 100),
        'deltaX': (i - a) ** -1 * np.linspace(0, max(delta_y, 1), 100)
    })
    st.line_chart(output_change_data.set_index('deltaY'), use_container_width=True)

def update_wage_employment_chart(delta_x, wage_vector, employment_vector):
    wage_employment_data = pd.DataFrame({
        'deltaX': np.linspace(0, max(delta_x, 1), 100),
        'Wage Impact': wage_vector * np.linspace(0, max(delta_x, 1), 100),
        'Employment Impact': employment_vector * np.linspace(0, max(delta_x, 1), 100)
    })
    st.line_chart(wage_employment_data.set_index('deltaX'), use_container_width=True)

# Visualization sections
st.subheader("Emission Intensity by Product")
st.write("The formula used:")
st.latex(r"e_{i,k} = \frac{\Sigma_j \text{emissions}_{j,k}}{\Sigma_j \text{output}_{j,k}}")
st.write(f"Emission Intensity: {emission_intensity:.2f}")
update_emission_intensity_chart(output, emissions)

# Layout for side-by-side graphs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Output Change (deltaX)")
    st.write("The formula used:")
    st.latex(r"\Delta \mathbf{X} = (\mathbf{I} - \mathbf{A})^{-1} \Delta \mathbf{Y}")
    st.write(f"Total Output Change (deltaX): {delta_x:.2f}")
    update_output_change_chart(delta_y, a)

with col2:
    st.subheader("Wage and Employment Impacts")
    st.write("The formulas used:")
    st.latex(r"\Delta \mathbf{W} = \mathbf{w} \odot \Delta \mathbf{X}")
    st.latex(r"\Delta \mathbf{N} = \mathbf{n} \odot \Delta \mathbf{X}")
    st.write(f"Wage Impact (deltaW): {delta_w:.2f}")
    st.write(f"Employment Impact (deltaN): {delta_n:.2f}")
    update_wage_employment_chart(delta_x, default_wage_vector, default_employment_vector)

# Trigger updates based on slider changes
if st.session_state.get('key') != (output, emissions, delta_y):
    st.session_state['key'] = (output, emissions, delta_y)
    update_emission_intensity_chart(output, emissions)
    update_output_change_chart(delta_y, a)
    update_wage_employment_chart(delta_x, default_wage_vector, default_employment_vector)

st.markdown(
    """
    <br><br>
    <div style="text-align: center; color: gray; font-size: 12px;">
        &copy; Gelora Damayanti Manalu 2024.
    </div>
    """, 
    unsafe_allow_html=True
)