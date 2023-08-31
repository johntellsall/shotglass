# demo_altair.py

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Create a DataFrame with random data
np.random.seed(42)
data = pd.DataFrame({
    'x': np.random.rand(50),
    'y': np.random.rand(50)
})

# Create an Altair scatter plot
scatter_plot = alt.Chart(data).mark_circle().encode(
    x='x',
    y='y'
)

# st.altair_chart(scatter_plot, use_container_width=False, theme="streamlit")
st.altair_chart(scatter_plot)


