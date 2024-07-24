import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from transformers import pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

# Set page config
st.set_page_config(page_title="Advanced Streamlit App", layout="wide")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Analysis", "ML Model", "NLP"])

# Home page
if page == "Home":
    st.title("Welcome to the Advanced Streamlit App")
    st.write("This app demonstrates various data science and ML capabilities.")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=300)

# Data Analysis page
elif page == "Data Analysis":
    st.title("Data Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data.head())
        
        # Basic stats
        st.write("Basic Statistics:")
        st.write(data.describe())
        
        # Plotting
        st.subheader("Data Visualization")
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.pyplot(data.hist(figsize=(10, 10)))
        with fig_col2:
            fig = px.scatter(data, x=data.columns[0], y=data.columns[1])
            st.plotly_chart(fig)

# ML Model page
elif page == "ML Model":
    st.title("Machine Learning Model")
    
    # Sample dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Model evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Model Accuracy: {accuracy:.2f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': iris.feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    st.bar_chart(feature_importance.set_index('feature'))

# NLP page
elif page == "NLP":
    st.title("Natural Language Processing")
    
    # Load NLP model
    @st.cache(allow_output_mutation=True)
    def load_nlp_model():
        return pipeline("sentiment-analysis")
    
    nlp_model = load_nlp_model()
    
    # Text input
    text_input = st.text_area("Enter text for sentiment analysis:")
    if text_input:
        result = nlp_model(text_input)[0]
        st.write(f"Sentiment: {result['label']}")
        st.write(f"Confidence: {result['score']:.4f}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Created with Streamlit")
