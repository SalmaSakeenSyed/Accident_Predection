import streamlit as st
import pickle
import requests

# Load the trained model
with open('model1.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define dictionaries for dropdown options
vehicle_type_dict = {
    0: 'Select your Vehicle Type',
    1: 'Pedal cycle',
    2: 'Motorcycle 50cc and under',
    3: 'Motorcycle 125cc and under',
    4: 'Motorcycle over 125cc and up to 500cc',
    5: 'Motorcycle over 500cc',
    8: 'Taxi/Private hire car',
    9: 'Car',
    10: 'Minibus (8 - 16 passenger seats)',
    11: 'Bus or coach (17 or more pass seats)',
    16: 'Ridden horse',
    17: 'Agricultural vehicle',
    18: 'Tram',
    19: 'Van/Goods 3.5 tonnes mgw or under',
    20: 'Goods over 3.5t. and under 7.5t',
    21: 'Goods 7.5 tonnes mgw and over',
    22: 'Mobility scooter',
    23: 'Electric motorcycle',
    90: 'Other vehicle',
    97: 'Motorcycle - unknown cc',
    98: 'Goods vehicle-unknown weight'
}

day_dict = {
    0: 'Select day',
    1: 'Sunday',
    2: 'Monday',
    3: 'Tuesday',
    4: 'Wednesday',
    5: 'Thursday',
    6: 'Friday',
    7: 'Saturday'
}

weather_dict = {
    0: 'Choose weather condition',
    1: 'Fine no high winds',
    2: 'Raining no high winds',
    3: 'Snowing no high winds',
    4: 'Fine + high winds',
    5: 'Raining + high winds',
    6: 'Snowing + high winds',
    7: 'Fog or mist',
    8: 'Other'
}

light_dict = {
    0: 'Choose lighting condition',
    1: 'Daylight',
    4: 'Darkness - lights lit',
    5: 'Darkness - lights unlit',
    6: 'Darkness - no lighting',
    7: 'Darkness - lighting unknown',
}

roadsc_dict = {
    0: 'Select Road Surface',
    1: 'Dry',
    2: 'Wet or damp',
    3: 'Snow',
    4: 'Frost or ice',
    5: 'Flood over 3cm. deep',
    6: 'Oil or diesel',
    7: 'Mud'    
}

gender_dict = {
    0: 'Gender',
    1: 'Male',
    2: 'Female',
    3: 'Prefer not to say'
}

@st.cache_data
def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json()
        ip_address = data['ip']
        return ip_address
    except Exception as e:
        st.error(f"Error getting public IP address: {e}")
        return None

@st.cache_data
def get_location(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()
        location = data.get('loc')
        if location:
            latitude, longitude = location.split(',')
            return float(latitude), float(longitude)
        else:
            st.warning("Location not found.")
            return None, None
    except Exception as e:
        st.error(f"Error getting location: {e}")
        return None, None

# Function to make predictions
def make_predictions(age_of_driver, vehicle_type, age_of_vehicle, engine_cc, day, weather, light, roadsc, gender, speedl, latitude, longitude):
    # Preprocess input and make predictions using the model
    # Replace this with your actual prediction code
    raw_prediction = model.predict([[age_of_driver, vehicle_type, age_of_vehicle, engine_cc, day, weather, light, roadsc, gender, speedl, latitude, longitude]])

    # Map raw predictions to severity levels
    if raw_prediction == 1:
        prediction = "Safe"
    elif raw_prediction == 2:
        prediction = "Moderate"
    elif raw_prediction == 3:
        prediction = "Severe"
    else:
        prediction = "Unknown"

    return prediction


# Streamlit app
def main():
    st.title('Road Accident Severity Prediction')

    # Input fields
    age_of_driver = st.number_input('Age of Driver', min_value=0)
    vehicle_type = st.selectbox('Vehicle Type', list(vehicle_type_dict.values()))
    age_of_vehicle = st.number_input('Age of Vehicle', min_value=0)
    engine_cc = st.number_input('Engine CC', min_value=0)
    day = st.selectbox('Day', list(day_dict.values()))
    weather = st.selectbox('Weather', list(weather_dict.values()))
    light = st.selectbox('Light', list(light_dict.values()))
    roadsc = st.selectbox('Road Conditions', list(roadsc_dict.values()))
    gender = st.selectbox('Gender', list(gender_dict.values()))
    speedl = st.number_input('Speed', min_value=0)

    # Choose location input method
    location_method = st.radio("Choose location input method:", ("Manual", "Dynamic"))

    if location_method == "Manual":
        latitude = st.number_input('Latitude', value=0.0, step=0.000001, format="%.6f")
        longitude = st.number_input('Longitude', value=0.0, step=0.000001, format="%.6f")
    else:  # Dynamic location
        ip_address = get_public_ip()
        if ip_address:
            latitude, longitude = get_location(ip_address)
        else:
            st.error("Failed to retrieve public IP address.")
            latitude, longitude = None, None

    # Predict button
    if st.button('Predict'):
        prediction = make_predictions(age_of_driver, list(vehicle_type_dict.keys())[list(vehicle_type_dict.values()).index(vehicle_type)], age_of_vehicle, engine_cc, list(day_dict.keys())[list(day_dict.values()).index(day)], list(weather_dict.keys())[list(weather_dict.values()).index(weather)], list(light_dict.keys())[list(light_dict.values()).index(light)], list(roadsc_dict.keys())[list(roadsc_dict.values()).index(roadsc)], list(gender_dict.keys())[list(gender_dict.values()).index(gender)], speedl, latitude, longitude)
        
        st.write('Predicted Severity:', prediction)

if __name__ == "__main__":
    main()
