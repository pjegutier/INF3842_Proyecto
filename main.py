import altair as alt
import pandas as pd
import streamlit as st

data_set = {
    'countries': ['India', 'Australia', 'Japan', 'America', 'Russia'],
    'values': [4500, 2500, 1053, 500, 3200]
}

df = pd.DataFrame(data_set)

line = alt.Chart(df).mark_line().encode(
    x = 'countries',
    y = 'values'
).properties(width=500, height=500)

st.altair_chart(line)
