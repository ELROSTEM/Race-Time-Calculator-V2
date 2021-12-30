import streamlit as st

from apps import calculation, homepage
from multiapp import MultiApp

st.set_page_config(
    page_title='Race Time Calculator',
    layout="wide",
    initial_sidebar_state="expanded",
)

apps = MultiApp()

# Add all your application here
apps.add_app("Home", homepage.app)
apps.add_app("Calc", calculation.app)

# The main app
apps.run()
