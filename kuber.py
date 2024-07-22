import streamlit as st
import pandas as pd
from scipy.optimize import minimize

# Industry types
industry_types = {
    "Retail": ["Fashion", "Electronics", "Food", "Home Goods"],
    "Finance": ["Banking", "Investments", "Insurance", "Wealth Management"],
    "Healthcare": ["Hospitals", "Pharmaceuticals", "Medical Devices", "Health Insurance"],
    "Technology": ["Software", "Hardware", "IT Services", "Cybersecurity"],
    "Events": ["Conferences", "Trade Shows", "Weddings", "Festivals"],  # Added Events industry type
    "Real Estate": ["Residential", "Commercial", "Industrial", "Property Management"],
    "Manufacturing": ["Automotive", "Aerospace", "Chemicals", "Food Processing"],
    "Energy": ["Oil and Gas", "Renewable Energy", "Utilities", "Energy Trading"],
    "Media": ["Television", "Radio", "Print", "Digital Media"]
}

# Campaign effectiveness data
campaign_effectiveness_data = {
    "Retail": {"Fashion": 0.15, "Electronics": 0.20, "Food": 0.10, "Home Goods": 0.12},
    "Finance": {"Banking": 0.18, "Investments": 0.22, "Insurance": 0.15, "Wealth Management": 0.20},
    "Healthcare": {"Hospitals": 0.12, "Pharmaceuticals": 0.18, "Medical Devices": 0.15, "Health Insurance": 0.10},
    "Technology": {"Software": 0.20, "Hardware": 0.18, "IT Services": 0.15, "Cybersecurity": 0.22},
    "Events": {"Conferences": 0.15, "Trade Shows": 0.18, "Weddings": 0.12, "Festivals": 0.10},  # Added Events industry type
    "Real Estate": {"Residential": 0.12, "Commercial": 0.15, "Industrial": 0.10, "Property Management": 0.12},
    "Manufacturing": {"Automotive": 0.15, "Aerospace": 0.18, "Chemicals": 0.12, "Food Processing": 0.10},
    "Energy": {"Oil and Gas": 0.18, "Renewable Energy": 0.20, "Utilities": 0.15, "Energy Trading": 0.12},
    "Media": {"Television": 0.12, "Radio": 0.10, "Print": 0.08, "Digital Media": 0.15}
}

# ROI values
roi_values = [0.05, 0.10, 0.15, 0.20]

# Create a title and description for the UI
st.title("Comprehensive Budget Optimization Program")
st.write("This program helps companies optimize their budget allocation based on various parameters. Please enter the required data.")

# Create input fields for revenue, expenses, and industry
revenue = st.number_input("Enter the company's revenue:")
expenses = st.number_input("Enter the company's expenses:")
industry_type = st.selectbox("Select the company's industry type:", list(industry_types.keys()))
sub_industry_type = st.selectbox("Select the company's sub-industry type:", industry_types[industry_type])
employee_count = st.number_input("Enter the number of employees:")
office_space = st.selectbox("Does the company have office space?", ["Yes", "No"])
marketing_expenses = st.number_input("Enter the marketing expenses:")
research_and_development_expenses = st.number_input("Enter the research and development expenses:")
operating_expenses_base = st.number_input("Enter the operating expenses (excluding taxes and interest):")
interest_expenses = st.number_input("Enter the interest expenses:")
taxes = st.number_input("Enter the taxes:")

office_rent = 0
if office_space == "Yes":
    office_rent = st.number_input("Enter the office rent:")

# Calculate the total operating expenses
operating_expenses = operating_expenses_base + interest_expenses + taxes

# Define the budget allocation parameters
budget_params = ['Employee Salaries', 'Office Rent', 'Marketing', 'Research and Development', 'Operating Expenses', 'Miscellaneous']

# Define the weights for each parameter based on industry and other factors
weights = {
    'Tech': [0.3, 0.2, 0.1, 0.2, 0.1, 0.2],
    'Finance': [0.2, 0.3, 0.1, 0.1, 0.1, 0.2],
    'Healthcare': [0.4, 0.2, 0.1, 0.1, 0.1, 0.1],
    'Other': [0.3, 0.2, 0.1, 0.2, 0.1, 0.2]
}[industry_type]

# Calculate campaign effectiveness
campaign_effectiveness = campaign_effectiveness_data[industry_type][sub_industry_type]

# Calculate ROI
roi = campaign_effectiveness * roi_values[0]

# Display campaign effectiveness and ROI
st.write(f"Campaign effectiveness for {sub_industry_type} in {industry_type} industry: {campaign_effectiveness:.2f}")
st.write(f"ROI for {sub_industry_type} in {industry_type} industry: {roi:.2f}")

# Budget optimizer
st.header("Budget Optimizer")

# Calculate the total budget available for optimization
total_budget = revenue - expenses - office_rent

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

# Calculate and display the ROI (Return on Investment) for each parameter
st.subheader("ROI Analysis:")
roi_params = ['Marketing', 'Research and Development']
roi_values = [0.01, 0.05]
for i, param in enumerate(roi_params):
    roi = campaign_effectiveness * roi_values[i]
    st.write(f"{param} ROI: {roi:.2f}")

# Calculate the total ROI
total_roi = sum([campaign_effectiveness * roi_values[i] for i in range(len(roi_params))])
st.write(f"Total ROI: {total_roi:.2f}")

# Calculate the ROI for each budget parameter
roi_allocations = []
for i, param in enumerate(budget_params):
    if param == 'Office Rent' and office_space == "No":
        roi_allocations.append(0)
    else:
        roi_allocation = result.x[i] * total_budget * weights[i] * total_roi
        roi_allocations.append(roi_allocation)
        st.write(f"{param} ROI Allocation: {roi_allocation:.2f}")

# Display the optimized budget allocation with ROI
st.subheader("Optimized Budget Allocation with ROI:")
for i, param in enumerate(budget_params):
    if param == 'Office Rent' and office_space == "No":
        st.write(f"{param}: 0.00")
    else:
        st.write(f"{param}: {result.x[i] * total_budget * weights[i]:.2f} ({roi_allocations[i]:.2f} ROI)")
