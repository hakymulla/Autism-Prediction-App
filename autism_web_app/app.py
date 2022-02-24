#app.py
import streamlit as st
from apps import details, autism
from multiapp import MultiApp

app = MultiApp()

# Add all your application here
app.add_app("Home", details.app)
app.add_app("Prediction", autism.app)
# The main app
app.run()