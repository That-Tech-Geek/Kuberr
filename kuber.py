import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Create a title and description for the UI
st.title("Budget Drafting Assistant")
st.write("This model helps companies draft budgets with minimal human intervention. Please upload a CSV file with the required data.")

# Create a file uploader widget
uploaded_file = st.file_uploader("Select a CSV file:", type=["csv"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Create input fields for revenue, expenses, and industry
    revenue = st.number_input("Enter the company's revenue:")
    expenses = st.number_input("Enter the company's expenses:")
    industry = st.selectbox("Select the company's industry:", ["Tech", "Finance", "Healthcare", "Other"])

    # Create a button to submit the input data
    if st.button("Submit"):
        # Create a dataframe with the input data
        input_data = pd.DataFrame({'Revenue': [revenue], 'Expenses': [expenses], 'Industry': [industry]})

        # Load the trained machine learning model
        model = RandomForestRegressor()
        model.load('budget_model.pkl')

        # Make a prediction on the input data
        prediction = model.predict(input_data)

        # Display the predicted budget
        st.subheader(f"Predicted Budget: ${prediction[0]:.2f}")
else:
    st.write("Please upload a CSV file to proceed.")
