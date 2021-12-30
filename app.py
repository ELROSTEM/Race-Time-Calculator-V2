import streamlit as st

from apps import calculation, homepage
from multiapp import MultiApp

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here
apps.add_app("Home", homepage.app)
apps.add_app("Calc", calculation.app)

# The main app
apps.run()
