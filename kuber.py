import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LinearRegression
import numpy as np
import base64

# Load dataset
data = {
    'Campaign': ['Facebook', 'Google', 'Instagram', 'Twitter', 'LinkedIn', 'YouTube', 'TikTok', 'Snapchat', 'Reddit', 'Quora'],
    'Budget': [1000, 2000, 1500, 1200, 1800, 2500, 800, 1000, 500, 300],
    'Impressions': [10000, 20000, 15000, 12000, 18000, 25000, 8000, 10000, 5000, 3000],
    'Clicks': [500, 1000, 750, 600, 900, 1200, 400, 500, 250, 150],
    'Conversions': [20, 40, 30, 25, 35, 50, 20, 25, 15, 10],
    'ROI': [0.2, 0.4, 0.3, 0.25, 0.35, 0.5, 0.2, 0.25, 0.15, 0.1]
}
df = pd.DataFrame(data)

# Add more ROI's
df['ROI_2'] = df['ROI'] * 1.1
df['ROI_3'] = df['ROI'] * 1.2
df['ROI_4'] = df['ROI'] * 1.3
df['ROI_5'] = df['ROI'] * 1.4

# Create a feature matrix and target vector
X = df[['Budget', 'Impressions', 'Clicks', 'Conversions']]
y = df['ROI']

# Scale the data using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA to reduce dimensionality
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3)
kmeans.fit(X_pca)
labels = kmeans.labels_

# Select the top 2 features using SelectKBest
selector = SelectKBest(f_classif, k=2)
X_selected = selector.fit_transform(X_scaled, y)

# Create a linear regression model
lr_model = LinearRegression()
lr_model.fit(X_selected, y)

# Create a function to generate recommendations
def generate_recommendations(budget, impressions, clicks, conversions):
    X_new = pd.DataFrame({'Budget': [budget], 'Impressions': [impressions], 'Clicks': [clicks], 'Conversions': [conversions]})
    X_new_scaled = scaler.transform(X_new)
    X_new_pca = pca.transform(X_new_scaled)
    label = kmeans.predict(X_new_pca)[0]
    X_new_selected = selector.transform(X_new_scaled)
    roi_pred = lr_model.predict(X_new_selected)[0]
    return label, roi_pred

# Create a Streamlit app
st.title("ROI Optimization Tool")
st.write("Enter campaign details to get recommendations:")

budget = st.number_input("Budget", value=1000)
impressions = st.number_input("Impressions", value=10000)
clicks = st.number_input("Clicks", value=500)
conversions = st.number_input("Conversions", value=20)

if st.button("Get Recommendations"):
    label, roi_pred = generate_recommendations(budget, impressions, clicks, conversions)
    st.write(f"Recommended cluster: {label}")
    st.write(f"Predicted ROI: {roi_pred:.2f}")
    st.write("Top 3 campaigns to increase ROI:")
    top_campaigns = df.sort_values(by='ROI', ascending=False).head(3)
    st.write(top_campaigns)

    # Create a CSV file with recommendations
    csv = pd.DataFrame({'Campaign': top_campaigns['Campaign'], 'Budget': top_campaigns['Budget'], 'Impressions': top_campaigns['Impressions'], 'Clicks': top_campaigns['Clicks'], 'Conversions': top_campaigns['Conversions'], 'ROI': top_campaigns['ROI']})
    csv_string = csv.to_csv(index=False)
    b64 = base64.b64encode(csv_string.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="recommended_campaigns.csv">Download CSV</a>'
    st.write(href, unsafe_allow_html=True)
