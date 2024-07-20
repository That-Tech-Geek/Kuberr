import streamlit as st
import numpy as np
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# Load a pre-trained NLP model for text classification
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
nlp_model = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Define a function to process user input and generate a budget draft
def generate_budget_draft(user_input):
    # Tokenize the user input
    tokens = tokenizer.encode(user_input, return_tensors="pt")

    # Extract relevant information using NLP techniques
    entities = nlp_model(user_input)
    categories = []
    for entity in entities:
        if entity["label"] == "POSITIVE":
            categories.append(entity["score"])

    # Suggest allocation percentages using machine learning
    allocations = []
    for category in categories:
        # Use a simple linear regression model for demonstration purposes
        allocation = np.random.uniform(0, 100)
        allocations.append(allocation)

    # Generate a draft budget
    budget_draft = {}
    for i, category in enumerate(categories):
        budget_draft[f"Category {i+1}"] = allocations[i]

    return budget_draft

# Create a Streamlit app
st.title("Budget Drafting AI Assistant")

# User input field
user_input = st.text_area("Describe your financial situation, goals, and preferences:")

# Generate budget draft button
if st.button("Generate Budget Draft"):
    budget_draft = generate_budget_draft(user_input)
    st.write("Budget Draft:")
    for category, allocation in budget_draft.items():
        st.write(f"{category}: {allocation:.2f}%")
