import streamlit as st
import numpy as np
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import pytorch

# Load a pre-trained NLP model for text classification
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
nlp_model = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def generate_budget_draft(user_input):
    # Analyze the sentiment of the user input
    sentiment = nlp_model(user_input)[0]
    sentiment_score = sentiment["score"]

    # Generate a random budget draft based on the sentiment score
    budget_draft = {}
    num_categories = 5
    for i in range(num_categories):
        category_name = f"Category {i+1}"
        allocation = np.random.uniform(0, 100) * sentiment_score
        budget_draft[category_name] = allocation

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
