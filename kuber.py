import streamlit as st
import pandas as pd
from scipy.optimize import minimize
import requests

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
}[industry]

# Create a function to research campaign effectiveness in real-time using Google Trends API
def research_campaign_effectiveness():
    api_key = "YOUR_API_KEY"
    url = f"https://api.serper.io/search?engine=google_trends&api_key={api_key}&q=marketing+campaigns+effectiveness"
    response = requests.get(url)
    data = response.json()
    # Extract relevant data from the API response
    campaign_effectiveness_data = []
    for result in data["organic_results"]:
        campaign_effectiveness_data.append({
            "Campaign": result["title"],
            "Search Volume": result["search_volume"],
            "Trends": result["trends"]
        })
    return campaign_effectiveness_data

# Create a button to research campaign effectiveness
if st.button("Research Campaign Effectiveness"):
    campaign_effectiveness_data = research_campaign_effectiveness()
    st.write("Campaign Effectiveness Data:")
    st.write(pd.DataFrame(campaign_effectiveness_data))

# Create a button to submit the input data
if st.button("Submit"):
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
    roi = campaign_effectiveness_data[i][list(campaign_effectiveness_data[i].keys())[0]] * roi_values[i]
    st.write(f"{param} ROI: {roi:.2f}")

# Calculate the total ROI
total_roi = sum([campaign_effectiveness_data[i][list(campaign_effectiveness_data[i].keys())[0]] * roi_values[i] for i in range(len(roi_params))])
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
