import altair as alt
import pandas as pd
import streamlit as st
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", 'lxml'])

bici = pd.read_csv('san-juan-xl.csv',sep=';',decimal=',')

line = alt.Chart(bici).mark_line().encode(
    x = 'ns1:LatitudeDegrees4',
    y = 'ns1:LongitudeDegrees5'
).properties(width=500, height=500)

st.altair_chart(line)
st.write(bici.head())

