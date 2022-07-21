import altair as alt
import pandas as pd
import streamlit as st
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", 'lxml'])

bici = pd.read_csv('san-juan-xl.csv',sep=';',decimal=',')

line = alt.Chart(bici).mark_circle(size=60).encode(
    x = 'ns1:LatitudeDegrees4:Q',
    y = 'ns1:LongitudeDegrees5:Q'
).properties(width=500, height=500).interactive()

st.altair_chart(line)
st.write(bici.head())

