import streamlit as st
import pandas as pd
from scipy.optimize import minimize

# Create a title and description for the UI
st.title("Budget Optimization Program")
st.write("This program helps companies optimize their budget allocation based on various parameters. Please enter the required data.")

# Create input fields for revenue, expenses, and industry
revenue = st.number_input("Enter the company's revenue:")
expenses = st.number_input("Enter the company's expenses:")
industry = st.selectbox("Select the company's industry:", ["Tech", "Finance", "Healthcare", "Other"])
employee_count = st.number_input("Enter the number of employees:")
office_space = st.selectbox("Does the company have office space?", ["Yes", "No"])
marketing_expenses = st.number_input("Enter the marketing expenses:")

# Define the budget allocation parameters
budget_params = ['Employee Salaries', 'Office Rent', 'Marketing', 'Research and Development', 'Miscellaneous']

# Create a button to submit the input data
if st.button("Submit"):
    # Define the objective function to minimize
    def objective_function(allocation):
        # Calculate the total budget
        total_budget = revenue - expenses
        
        # Calculate the allocation for each parameter
        employee_salaries = allocation[0] * total_budget
        office_rent = allocation[1] * total_budget
        marketing = allocation[2] * total_budget
        research_and_development = allocation[3] * total_budget
        miscellaneous = allocation[4] * total_budget
        
        # Calculate the penalty for exceeding the total budget
        penalty = max(0, employee_salaries + office_rent + marketing + research_and_development + miscellaneous - total_budget)
        
        # Return the penalty as the objective function value
        return penalty
    
    # Define the bounds for the allocation parameters
    bounds = [(0, 1) for _ in range(len(budget_params))]
    
    # Initialize the allocation parameters
    init_allocation = [0.2 for _ in range(len(budget_params))]
    
    # Run the optimization
    result = minimize(objective_function, init_allocation, method="SLSQP", bounds=bounds)
    
    # Display the optimized budget allocation
    st.subheader("Optimized Budget Allocation:")
    for i, param in enumerate(budget_params):
        st.write(f"{param}: {result.x[i] * (revenue - expenses):.2f}")
else:
    st.write("Please enter the required data and click Submit.")
