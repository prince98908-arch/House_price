import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load('house_price_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')

st.title('House Price Prediction App')

st.write('Enter property details below:')

# User Inputs
posted_by = st.selectbox('Posted By', ['Owner', 'Dealer', 'Builder'])
under_construction = st.selectbox('Under Construction', [0, 1])
rera = st.selectbox('RERA Approved', [0, 1])
bhk_no = st.number_input('BHK Number', min_value=1, max_value=20, value=2)
bhk_or_rk = st.selectbox('BHK or RK', ['BHK', 'RK'])
square_ft = st.number_input('Square Feet', min_value=100.0, value=1000.0)
ready_to_move = st.selectbox('Ready To Move', [0, 1])
resale = st.selectbox('Resale', [0, 1])
address = st.text_input('Address', 'Mumbai')
longitude = st.number_input('Longitude', value=72.8777)
latitude = st.number_input('Latitude', value=19.0760)

# Encode inputs
posted_by_encoded = label_encoders['POSTED_BY'].transform([posted_by])[0] \
    if posted_by in label_encoders['POSTED_BY'].classes_ else 0

bhk_or_rk_encoded = label_encoders['BHK_OR_RK'].transform([bhk_or_rk])[0] \
    if bhk_or_rk in label_encoders['BHK_OR_RK'].classes_ else 0

address_encoded = label_encoders['ADDRESS'].transform([address])[0] \
    if address in label_encoders['ADDRESS'].classes_ else 0

# Create dataframe
input_data = pd.DataFrame({
    'POSTED_BY': [posted_by_encoded],
    'UNDER_CONSTRUCTION': [under_construction],
    'RERA': [rera],
    'BHK_NO.': [bhk_no],
    'BHK_OR_RK': [bhk_or_rk_encoded],
    'SQUARE_FT': [square_ft],
    'READY_TO_MOVE': [ready_to_move],
    'RESALE': [resale],
    'ADDRESS': [address_encoded],
    'LONGITUDE': [longitude],
    'LATITUDE': [latitude]
})

# Prediction
if st.button('Predict Price'):
    prediction = model.predict(input_data)

    st.success(f'Estimated House Price: {prediction[0]:.2f} Lakhs')
