import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load historical budget data
data = pd.read_csv('budget_data.csv')

# Create a title and description for the UI
st.title("Budget Drafting Assistant")
st.write("This model helps companies draft budgets with minimal human intervention. Please input the required information below.")

# Input fields for revenue, expenses, and industry
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
