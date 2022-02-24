import streamlit as st
from PIL import Image
from datetime import datetime
from apps import autism
import os

path = 'autism_web_app/model'

def app():

    image_autism = Image.open(f'{path}/autism.jpg')
    image_autism = image_autism.resize((800, 300))
    st.image(image_autism)

    

    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
    st.write(cwd)
    st.write(files)
    st.markdown("""
    # Autism Prediction App

    ### Predict the likelihood of a person having autism using survey and demographic variables
    """)

    expander = st.expander('About Data')
    expander.markdown("""
    Autism is a neurodevelopmental disorder characterized by difficulties with social interaction and communication, and by restricted and repetitive behavior

    **Data Source:** [Kaggle] (https://www.kaggle.com/andrewmvd/autism-screening-on-adults)

    **More Information About Autism:** [autismspeaks] (https://www.autismspeaks.org/what-autism)

    **Disclaimer**

    These resources are implementation tools and should be used alongside the published guidance. The information does not supersede or replace the guidance itself.

    **Get More Information Here :** [National Institute for Care and Health Excellence] (https://www.nice.org.uk/guidance/cg142/resources/autism-spectrum-quotient-aq10-test-143968)

    """)

    image = Image.open(f'{path}/aq10.png')
    image = image.resize((800, 1000))

    st.image(image, caption = 'Autism spectrum quotient (AQ-10) test')