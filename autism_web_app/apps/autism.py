import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pickle
from PIL import Image
from datetime import datetime

def load_label_dict():
    with open('label_encode.json', 'r') as file:
        json_file = json.load(file)
        return json_file

def load_model():
    with open('lgbm.pkl', 'rb') as file:
        model = pickle.load(file)
        return model

def app():
    dict_file = load_label_dict()
    model = load_model()

    choices1 = {'Definitely Agree':1, 'Slightly Agree':1, 'Definitely Disagree':0, 'Slightly Disagree':0}
    choices2 = {'Definitely Agree':0, 'Slightly Agree':0, 'Definitely Disagree':1, 'Slightly Disagree':1}
    genders = ['Male', 'Female']
    ethnicities = ['Black', 'White-European', 'South Asian', 'Asian', 'Middle Eastern', 'others', 'Latino', 'Turkish', 'Others', 'Hispanic', 'Pasifika']
    yes_no = ['Yes', 'No']
    relations = ['Self', 'Health care professional', 'Parent', 'Relative','Others']
    countries = ['United States', 'Australia', 'United Kingdom', 'New Zealand',
        'Italy', 'Nicaragua', 'Canada', 'United Arab Emirates',
        'Netherlands', 'Sri Lanka', 'India', 'Armenia', 'Sierra Leone',
        'Argentina', 'Azerbaijan', 'Iceland', 'Egypt', 'Serbia',
        'Afghanistan', 'Costa Rica', 'Jordan', 'Angola', 'Pakistan',
        'Brazil', 'Ireland', 'Kazakhstan', 'Viet Nam', 'Ethiopia',
        'Austria', 'Finland', 'France', 'Malaysia', 'Japan', 'Spain',
        'Philippines', 'Iran', 'Czech Republic', 'Russia', 'Romania',
        'Mexico', 'Belgium', 'Aruba', 'Uruguay', 'Indonesia', 'Ukraine',
        'AmericanSamoa', 'Germany', 'China', 'Iraq', 'Tonga',
        'South Africa', 'Saudi Arabia', 'Hong Kong', 'Bahamas', 'Ecuador',
        'Cyprus', 'Bangladesh', 'Oman', 'Bolivia', 'Sweden', 'Niger']
    st.markdown(""" 
            ##  AQ-10 
            ### Autism Spectrum Quotient (AQ)
            """)
    question1 = st.selectbox('I often notice small sounds when others do not', choices1.keys())
    question2 = st.selectbox('I usually concentrate more on the wholepicture, rather than the small details', choices2.keys())
    question3 = st.selectbox('I find it easy to do more than one thing at once', choices2.keys())
    question4 = st.selectbox('If there is an interruption, I can switch back to what I was doing very quickly', choices2.keys())
    question5 = st.selectbox('I find it easy to ‘read between the lines’ whensomeone is talking to me', choices2.keys())
    question6 = st.selectbox('I know how to tell if someone listening to me is getting bored', choices2.keys())
    question7 = st.selectbox('When I’m reading a story I find it difficult to work out the characters’ intentions', choices1.keys())
    question8 = st.selectbox(' like to collect information about categories ofthings (e.g. types of car, types of bird, typesof train, types of plant etc)', choices1.keys())
    question9 = st.selectbox('I find it easy to work out what someone is thinking or feeling just by looking at their face', choices2.keys())
    question10 = st.selectbox('I find it difficult to work out people’s intentions', choices1.keys())


    question1 = choices1[question1]
    question2 = choices2[question2]
    question3 = choices2[question3]
    question4 = choices2[question4]
    question5 = choices2[question5]
    question6 = choices2[question6]
    question7 = choices1[question7]
    question8 = choices1[question8]
    question9 = choices2[question9]
    question10 = choices1[question10]

    # Only 1 point can be scored for each question. Score 1 point for Definitely or
    # Slightly Agree on each of items 1, 7, 8, and 10. Score 1 point for Definitely or Slightly
    # Disagree on each of items 2, 3, 4, 5, 6, and 9. If the individual scores more than 6 out of 10,
    # consider referring them for a specialist diagnostic assessment.

    result = question1 + question2 + question3 + question4 + question5 + question6 +question7 + question8 + question9 + question10

    autism_score = st.button('Get Autism spectrum quotient (AQ-10) score')
    if autism_score:
        st.success (f'Your Autism spectrum quotient (AQ-10) test score is: {result}')


    st.markdown("""
                ***

            ### Demographic Variables
    """)

    age = st.number_input('Enter Your Age')
    gender = st.selectbox('Gender', genders)
    ethnicity = st.selectbox('Ethnicity', ethnicities)
    jaundice = st.selectbox('Whether the patient had Jaundice at the time of birth', yes_no)
    country = st.selectbox('Country of Residence', countries)
    austism = st.selectbox('Whether an immediate family member has been diagnosed with autism', yes_no)
    used_app_before = st.selectbox('Whether the patient has undergone a screening test before', yes_no)
    relations = st.selectbox('Relation of patient who completed the test', relations)




    predict = st.button('Predict')
    if predict:
        result = (question1 + question2 + question3 + question4 + question5 + question6 + question7 + question8 + question9 + question10)

        data = [question1, question2, question3, question4, question5, question6, question7, question8, question9, question10,
            age, gender, ethnicity, jaundice, austism, country, used_app_before, result, relations
            ]
        df = pd.DataFrame(data).T

        df.columns = ['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score','A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score', 
                    'age', 'gender', 'ethnicity', 'jaundice', 'autism', 'country_of_residence', 'used_app_before', 'result', 'relation'
            ]
        
        for key in dict_file.keys():
            try:
                df[key] = df[key].map(dict_file[key])
            except KeyError:
                pass
        int_col = ['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score','A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score', 'age', 'result']
        for col in int_col:
            df[col] = df[col].astype('int')

            inv_dict = {v:k for k,v in dict_file['Class/ASD'].items()}

        prediction = model.predict(df)
        

        autism_diagnosis = inv_dict.get(prediction[0])
        if autism_diagnosis == 'Yes':
            st.success(f'You do have Autism')
        if autism_diagnosis == 'No':
            st.success(f"You Don't have Autism")

