import streamlit as st
import pandas as pd
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import seaborn as sns
from pycaret.regression import *
import base64
import io
from classification import build_classifier
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
    wip = 'Building your models, Please Wait....'
    st.write(wip) 
    if usecase == "classification":
        table = build_classifier(df,label)
    else:
        m1 = setup(data = df,target = label,silent =True)
        best = compare_models()
        table = pull() 
    st.subheader('2. Table of Model Performance')

    st.write(pull())
    st.markdown(filedownload(table,'model_comparison.csv'), unsafe_allow_html=True)

    st.subheader('3. Plot of Model Performance')
    fig = plt.figure(figsize=(15,6))
    plt.xlabel('Models')
    if usecase == "regression":
        plt.bar(table['Model'].head(), table['R2'].head())
        plt.ylabel('R Square')
    else:
        plt.bar(table['Model'].head(), table['Accuracy'].head())
        plt.ylabel('Accuracy')
    st.pyplot(fig)
    st.markdown(imagedownload(fig,'r2_comparison'), unsafe_allow_html=True)
    

def filedownload(df, filename):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

def imagedownload(plt, filename):
    s = io.BytesIO()
    plt.savefig(s, format='png', bbox_inches='tight')
    b64 = base64.b64encode(s.getvalue()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download {filename} Image</a>'
    return href

#---------------------------------#
st.write("""
# The Automatic Machine Learning App
""")

#---------------------------------#
# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

st.sidebar.subheader('OR')

with st.sidebar.header('Paste CSV data link here'):
    uploaded_text = st.sidebar.text_input("Paste csv data link here")
    if uploaded_text.endswith(".csv") and uploaded_text.startswith("http"):
        uploaded_file = uploaded_text
    elif uploaded_text == '':
        pass
    else:
        st.sidebar.error('Please enter a valid csv link')
    

# Sidebar - Specify parameter settings
with st.sidebar.header('2. Set Parameters'):
    usecase = st.sidebar.selectbox('Select dataset type (Regression/Classification)', ['regression','classification'])    

#---------------------------------#
# Main panel
# Displays the dataset
st.subheader('1. Dataset')

if uploaded_file is not None:
    
    if type(uploaded_file) is not str:
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
        usecase = 'regression'
        df = pd.concat( [X,Y], axis=1 )

        st.markdown('The Boston housing dataset is used as the example.')
        st.write(df.head(5))
        build_model(df)


with st.sidebar.subheader('Created by:'):
    st.sidebar.markdown('''[Atharva Khedkar](https://linktr.ee/atharvakhedkar/)''')
