import streamlit as st

from apps import calculation, homepage, methodology
from multiapp import MultiApp

st.set_page_config(
    page_title='Race Time Calculator',
    layout="wide",
    initial_sidebar_state="expanded",
)

apps = MultiApp()

# Add all your application here
apps.add_app("Calc", calculation.app)
# apps.add_app("Methodology", methodology.app)
apps.add_app("About", homepage.app)

# The main app
apps.run()
