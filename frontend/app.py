import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sale Revenue Predictor")

# Section for online prediction
#st.subheader("Online Prediction")

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, max_value=25.0,step=0.25, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area =st.number_input("Product Allocated Area", min_value=0.0, max_value=0.3, step=0.02, value=0.2)
Product_MRP = st.number_input("Product MRP", min_value=0.0, max_value=300.0, step=1.0, value=100.0)
Store_Size = st.selectbox("Store Size", ["Medium", "High", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 2", "Tier 1", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type2", "Departmental Store", "Supermarket Type1",
       "Food Mart"])
Product_Id_char = st.selectbox("Product Id char", ["FD", "NC", "DR"])
Store_Age_Years = st.selectbox("Store Age Years", [17, 27, 39, 28])
Product_Type_Category = st.selectbox("Product Type Category", ["Non Perishables", "Perishables"])

# Convert user input into a DataFrame
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)  # Send data to Flask API
    if response.status_code == 200:
       result = response.json()
       predicted_sales = result["Sales"]
       st.write(f"Predicted Product Store Sales Total: ₹{predicted_sales:.2f}")
    else:
        st.error("Error in API request")
        
# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")

