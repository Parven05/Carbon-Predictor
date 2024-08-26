import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

# Load the dataset
df = pd.read_csv('train/A5-Construction-Training.csv')

# Drop the 'No' column as it's not needed for modeling
df = df.drop(columns=['No'])

# Define features and generate target
X = df[['Machinery', 'Quantity', 'Fuel_consumption_rate','Hours_of_operation','Carbon_emission_factor']]  # Features
y = df['Quantity'] * df['Fuel_consumption_rate'] * df['Hours_of_operation'] * df['Carbon_emission_factor']  # Target

# Define the categorical and numeric features
categorical_feature = 'Machinery'
numeric_features = ['Quantity', 'Fuel_consumption_rate','Hours_of_operation', 'Carbon_emission_factor']

# Preprocessing for numeric data
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean'))
])

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, [categorical_feature])
    ])

# Create the model
model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.5,
    max_depth=5,
    subsample=1,
    colsample_bytree=0.5
)

# Create and evaluate the pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Print predictions and actual values for comparison
comparison_df = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred
}).reset_index(drop=True)

print("\nComparison of Actual vs. Predicted Values:")
print(comparison_df)

# Save the pipeline (model and preprocessing) using pickle
with open('models/Gradient-Boosting-A5.pkl', 'wb') as file:
    pickle.dump(pipeline, file)

print("Model saved as Gradient-Boosting-A5.pkl")
