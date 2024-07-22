import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load historical budget data
data = pd.read_csv('budget_data.csv')

# Preprocess data
X = data.drop(['Budget'], axis=1)  # features
y = data['Budget']  # target variable

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on new data
new_data = pd.DataFrame({'Revenue': [1000000], 'Expenses': [500000], 'Industry': ['Tech']})
prediction = model.predict(new_data)

# Print the predicted budget
print('Predicted Budget:', prediction[0])
