import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.io.arff import loadarff


def load_dataframe():
    data = loadarff('./jm1.arff')
    df = pd.DataFrame(data[0])
    return df


def prepare_dataframe(df):
    null_values = sum(df.isnull().sum())

    if null_values != 0:
        df.dropna(inplace=True)

    df['defects'] = df['defects'].apply(lambda value: 1 if value.decode('UTF-8') == 'true' else 0)
    return df


dataframe = load_dataframe()
dataframe = prepare_dataframe(dataframe)

st.title("Software defect prediction")
option = st.sidebar.selectbox("What should be done?", ("Visualize data", "Filter data"))
column_names = dataframe.columns.values.tolist()

if option == 'Filter data':

    parameter = st.sidebar.selectbox("Select a column", column_names)
    operator = st.sidebar.selectbox('Select an operator', (">", "<", "="))
    number = st.sidebar.number_input('Insert a number')

    if operator == '>':
        dataframe = dataframe[dataframe[parameter] > number]
    elif operator == '<':
        dataframe = dataframe[dataframe[parameter] < number]
    elif operator == '=':
        dataframe = dataframe[dataframe[parameter] == number]

    st.write(dataframe)

elif option == 'Visualize data':

    number_of_parameters = st.sidebar.selectbox("Select the number of parameters", (2, 3))

    first_parameter = st.sidebar.selectbox("Select a first parameter", column_names)
    second_parameter = st.sidebar.selectbox("Select a second parameter", column_names)

    if number_of_parameters == 2:
        dot_color = st.sidebar.color_picker('Pick a color', '#00f900')

    elif number_of_parameters == 3:
        third_parameter = st.sidebar.selectbox("Select a third parameter", column_names)

    opacity = st.sidebar.slider("Select an opacity", min_value=0.0, max_value=1.0, value=1.0, step=0.01)

    if number_of_parameters == 2:
        fig = px.scatter(dataframe,
                         x=first_parameter,
                         y=second_parameter,
                         color_discrete_sequence=[dot_color],
                         opacity=opacity)

    elif number_of_parameters == 3:
        fig = px.scatter(dataframe,
                         x=first_parameter,
                         y=second_parameter,
                         color=third_parameter,
                         opacity=opacity)

    st.plotly_chart(fig, use_container_width=True)
