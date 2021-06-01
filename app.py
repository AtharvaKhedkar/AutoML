import streamlit as st
import pandas as pd
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
from pycaret.regression import *
import seaborn as sns
import streamlit.components.v1 as components

import base64
import io
#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(page_title='The Automatic Machine Learning App',
    layout='wide')
#---------------------------------#
# Model building

def build_model(df):
    X = df.drop(columns=[label])
    Y = df[label]

    st.markdown('**1.3. Dataset dimension**')
    st.write('X')
    st.info(X.shape)
    st.write('Y')
    st.info(Y.shape)

    st.markdown('**1.4. Variable details**:')
    st.write('X variable (first 20 are shown)')
    st.info(list(X.columns[:20]))
    st.write('Y variable')
    st.info(Y.name)

    # Build  model
    st.write('Building your models, Please Wait....')
    m1 = setup(data = df, target = label, silent =True)

    best = compare_models()
    st.subheader('2. Table of Model Performance')
    table = pull()
    st.write(pull())
    st.markdown(filedownload(table,'model_comparison.csv'), unsafe_allow_html=True)

    st.subheader('3. Plot of Model Performance')

def filedownload(df, filename):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

def imagedownload(plt, filename):
    s = io.BytesIO()
    plt.savefig(s, format='png', bbox_inches='tight')
    plt.close()
    b64 = base64.b64encode(s.getvalue()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

#---------------------------------#
st.write("""
# The Automatic Machine Learning App
""")

#---------------------------------#
# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    usecase = st.sidebar.selectbox('Select dataset type (Regression/Classification)', ['regression','classification'])
with st.sidebar.subheader('Created by:'):
    st.sidebar.markdown('''[Atharva Khedkar](https://atharvakhedkar.co/)''')
    

#---------------------------------#
# Main panel
# Displays the dataset
st.subheader('1. Dataset')

if uploaded_file is not None:
    if usecase == 'regression':
        from pycaret.regression import *
    elif usecase == 'classification':
        from pycaret.classification import *
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)
    st.markdown('**1.1. Glimpse of dataset**')
    st.write(df)
    label = None 
    label = st.sidebar.selectbox('Select target attribute',df.columns)
    if label is not None:
        build_model(df)
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        boston = load_boston()
        X = pd.DataFrame(boston.data, columns=boston.feature_names)
        Y = pd.Series(boston.target, name='Price')
        label = 'Price'
        usecase = 'classification'
        df = pd.concat( [X,Y], axis=1 )

        st.markdown('The Boston housing dataset is used as the example.')
        st.write(df.head(5))

        build_model(df)

