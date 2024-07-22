import streamlit as st
import pandas as pd
from scipy.optimize import minimize

# Create a title and description for the UI
st.title("Comprehensive Budget Optimization Program")
st.write("This program helps companies optimize their budget allocation based on various parameters. Please enter the required data.")

# Create input fields for revenue, expenses, and industry
revenue = st.number_input("Enter the company's revenue:")
expenses = st.number_input("Enter the company's expenses:")
industry = st.selectbox("Select the company's industry:", ["Tech", "Finance", "Healthcare", "Other"])
employee_count = st.number_input("Enter the number of employees:")
office_space = st.selectbox("Does the company have office space?", ["Yes", "No"])
marketing_expenses = st.number_input("Enter the marketing expenses:")
research_and_development_expenses = st.number_input("Enter the research and development expenses:")
operating_expenses = st.number_input("Enter the operating expenses:")
depreciation_expenses = st.number_input("Enter the depreciation expenses:")
interest_expenses = st.number_input("Enter the interest expenses:")
taxes = st.number_input("Enter the taxes:")

office_rent = 0
if office_space == "Yes":
    office_rent = st.number_input("Enter the office rent:")

# Define the budget allocation parameters
budget_params = ['Employee Salaries', 'Office Rent', 'Marketing', 'Research and Development', 'Operating Expenses', 'Miscellaneous']

# Define the weights for each parameter based on industry and other factors
weights = {
    'Tech': [0.3, 0.2, 0.1, 0.2, 0.1, 0.2],
    'Finance': [0.2, 0.3, 0.1, 0.1, 0.1, 0.2],
    'Healthcare': [0.4, 0.2, 0.1, 0.1, 0.1, 0.1],
    'Other': [0.3, 0.2, 0.1, 0.2, 0.1, 0.2]
}[industry]

# Create a button to submit the input data
if st.button("Submit"):
    # Calculate the total budget available for optimization
    total_budget = revenue - expenses - interest_expenses - taxes - office_rent
    
    # Define the objective function to minimize
    def objective_function(allocation):
        # Calculate the allocation for each parameter
        allocations = [allocation[i] * total_budget * weights[i] for i in range(len(budget_params))]
        
        # Calculate the penalty for exceeding the total budget
        penalty = max(0, sum(allocations) - total_budget)
        
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
        if param == 'Office Rent' and office_space == "No":
            st.write(f"{param}: 0.00")
        else:
            st.write(f"{param}: {result.x[i] * total_budget * weights[i]:.2f}")
else:
    st.write("Please enter the required data and click Submit.")
