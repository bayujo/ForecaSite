from flask import Flask, render_template, request
import pickle
import folium
from geopy.distance import distance
import pandas as pd
import requests
import datetime

app = Flask(__name__)
app.debug = True

with open('model/linear_regression_model.pkl', 'rb') as f:
    linear_model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html', active_link = 'index')

@app.route('/predict')
def predict():
    start_location = request.args.get('start_location')
    end_location = request.args.get('end_location')
    user_surge_multiplier = request.args.get('surge_multiplier')

    types = {
        'Lyft': ['Shared', 'Lux', 'Lyft', 'Lux Black XL', 'Lyft XL', 'Lux Black'],
        'Uber': ['UberXL', 'Black', 'UberX', 'WAV', 'Black SUV', 'UberPool']
    }

    user_distance = calculate_distance(start_location, end_location, True)
    result = {}

    for service, names in types.items():
        result[service] = []
        for name in names:
            user_input = pd.DataFrame({
                'cab_type': [service],
                'name': [name],
                'distance': [user_distance],
                'surge_multiplier': [user_surge_multiplier]
            })

            user_input_encoded = pd.get_dummies(user_input)

            new_df_onehot = pd.DataFrame(columns=['price', 'distance', 'surge_multiplier', 'cab_type_Lyft', 'cab_type_Uber',
                                              'name_Black', 'name_Black SUV', 'name_Lux', 'name_Lux Black', 'name_Lux Black XL',
                                              'name_Lyft', 'name_Lyft XL', 'name_Shared', 'name_UberPool', 'name_UberX',
                                              'name_UberXL', 'name_WAV'])

            user_input_encoded = user_input_encoded.reindex(columns=new_df_onehot.drop('price', axis=1).columns, fill_value=0)
            
            # Make a prediction using the model
            prediction = linear_model.predict(user_input_encoded.values)

            # Format the prediction as a dollar amount with two decimal places
            prediction = f'{prediction[0]:,.2f}'
            result[service].append(prediction)

    return render_template('uberlyfttable.html', predictions=result, types=types)

def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(url).json()
    if response:
        lat = float(response[0]['lat'])
        lon = float(response[0]['lon'])
        return (lat, lon)
    return None

@app.route('/map')
def map():
    start_location = request.args.get('start_location')
    end_location = request.args.get('end_location')

    start_coordinates = get_coordinates(start_location)
    end_coordinates = get_coordinates(end_location)

    if start_coordinates and end_coordinates:
        # Create a map object centered at the midpoint
        map_obj = folium.Map()

        # Add markers for the start and end locations
        folium.Marker(location=start_coordinates, icon=folium.Icon(color='blue')).add_to(map_obj)
        folium.Marker(location=end_coordinates, icon=folium.Icon(color='red')).add_to(map_obj)

        # Calculate the map bounds
        bounds = [
            (start_coordinates[0], start_coordinates[1]),
            (end_coordinates[0], end_coordinates[1])
        ]

        # Get the center of the bounds
        center_lat = (start_coordinates[0] + end_coordinates[0]) / 2
        center_lng = (start_coordinates[1] + end_coordinates[1]) / 2

        # Adjust the zoom level and padding
        map_obj.fit_bounds(bounds, padding=(50, 50))
        map_obj.location = [center_lat, center_lng]
        map_obj.zoom_start = 10

        # Render the map
        return map_obj._repr_html_()

    return "Invalid locations"

@app.route('/distance')
def calculate_distance(start_location = None, end_location = None, internal = False):
    if internal:
        start_coordinates = get_coordinates(start_location)
        end_coordinates = get_coordinates(end_location)
    else:
        internal = False
        start_coordinates = get_coordinates(request.args.get('start_location'))
        end_coordinates = get_coordinates(request.args.get('end_location'))        

    if start_coordinates and end_coordinates:
        start_point = (start_coordinates[0], start_coordinates[1])
        end_point = (end_coordinates[0], end_coordinates[1])
        dist = distance(start_point, end_point).km
        if internal:
            return int(dist)
        else:
            return str(dist)

    return "Invalid locations"

@app.route('/rain-tomorrow-index')
def rain_index():
    return render_template('wheater-aus.html', active_link = 'rain')

@app.route('/rain-tomorrow')
def predict_rain():
    location = request.args.get('location')

    with open('model/logistic_regression_model.pkl', 'rb') as f:
        logistic_model = pickle.load(f)

    encoder = pd.read_pickle('model/encoder_rain.pkl')

    scaler = pd.read_pickle('model/scaler_rain.pkl')

    current_date = datetime.date.today()

    yesterday = current_date - datetime.timedelta(days=1)

    year = yesterday.year
    month = yesterday.month
    day = yesterday.day

    response = requests.get(f"https://api.weatherapi.com/v1/history.json?key=c3a2c3def8f94ba9a8945726230606&q={location}&dt={year}-{month}-{day}")
    weather_data = response.json()
    try:
        wind_directions = [hour["wind_dir"] for hour in weather_data["forecast"]["forecastday"][0]["hour"]]
    except:
        prediction = ['error']
        return render_template('wheater-prediction.html', prediction=prediction)
    
    most_common_wind_dir = max(set(wind_directions), key=wind_directions.count)

    hour_list = weather_data['forecast']['forecastday'][0]['hour']
    filtered_hour_list = [hour for hour in hour_list if hour['time'].endswith('09:00') or hour['time'].endswith('15:00')]

    weather_data['forecast']['forecastday'][0]['hour'] = filtered_hour_list            



    max_temp_c = weather_data['forecast']['forecastday'][0]['day']['maxtemp_c']
    min_temp_c = weather_data['forecast']['forecastday'][0]['day']['mintemp_c']
    rain_mm = weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm']
    uv = weather_data['forecast']['forecastday'][0]['day']['uv']
    WindGustSpeed = weather_data['forecast']['forecastday'][0]['day']['maxwind_kph']
    WindDir9am = weather_data['forecast']['forecastday'][0]['hour'][0]['wind_dir']
    WindSpeed9am = weather_data['forecast']['forecastday'][0]['hour'][0]['wind_kph']
    Humidity9am = weather_data['forecast']['forecastday'][0]['hour'][0]['humidity']
    Pressure9am = weather_data['forecast']['forecastday'][0]['hour'][0]['pressure_mb']
    Cloud9am = weather_data['forecast']['forecastday'][0]['hour'][0]['cloud'] / 12.5
    Temp9am = weather_data['forecast']['forecastday'][0]['hour'][0]['temp_c']
    WindDir3pm = weather_data['forecast']['forecastday'][0]['hour'][1]['wind_dir']
    WindSpeed3pm = weather_data['forecast']['forecastday'][0]['hour'][1]['wind_kph']
    Humidity3am = weather_data['forecast']['forecastday'][0]['hour'][1]['humidity']
    Pressure3am = weather_data['forecast']['forecastday'][0]['hour'][1]['pressure_mb']
    Cloud3am = weather_data['forecast']['forecastday'][0]['hour'][1]['cloud'] / 12.5
    Temp3am = weather_data['forecast']['forecastday'][0]['hour'][1]['temp_c']
    condition_text = weather_data['forecast']['forecastday'][0]['day']['condition']['text']

    sunrise_time = weather_data['forecast']['forecastday'][0]['astro']['sunrise']
    sunset_time = weather_data['forecast']['forecastday'][0]['astro']['sunset']

    sunrise_hour = int(sunrise_time.split(':')[0])
    if 'PM' in sunrise_time and sunrise_hour != 12:
        sunrise_hour += 12

    sunset_hour = int(sunset_time.split(':')[0])
    if 'PM' in sunset_time and sunset_hour != 12:
        sunset_hour += 12

    sunny_hour_count = 0

    for hour in weather_data['forecast']['forecastday'][0]['hour']:
        hour_time = int(hour['time'].split(' ')[1].split(':')[0])
        cloud_cover = hour['cloud']

        if 'PM' in hour['time'] and hour_time != 12:
            hour_time += 12

        if sunrise_hour <= hour_time <= sunset_hour and cloud_cover < 50:
            sunny_hour_count += 4

    if 'rain' in condition_text.lower():
        RainToday = 'Yes'
    else:
        RainToday = 'No'

    values = ['E', 'ENE', 'ESE', 'N', 'NE', 'NNE', 'NNW', 'NW', 'S', 'SE', 'SSE', 'SSW', 'SW', 'W', 'WNW', 'WSW']

    if WindDir3pm == WindDir9am or WindDir3pm == most_common_wind_dir:
        valid_values = [v for v in values if v != WindDir9am]
        WindDir3pm = valid_values[0]

    if WindDir9am == WindDir3pm or WindDir9am == most_common_wind_dir:
        valid_values = [v for v in values if v != WindDir3pm]
        WindDir9am = valid_values[0]

    if most_common_wind_dir == WindDir3pm or most_common_wind_dir == WindDir9am:
        valid_values = [v for v in values if v != WindDir3pm and v != WindDir9am]
        most_common_wind_dir = valid_values[0]

    user_input = pd.DataFrame({'Location': [location],
                            'MinTemp': [min_temp_c],
                            'MaxTemp': [max_temp_c],
                            'Rainfall': [rain_mm],
                            'Evaporation': [uv],
                            'Sunshine': [sunny_hour_count],
                            'WindGustDir': [most_common_wind_dir],
                            'WindGustSpeed': [WindGustSpeed],
                            'WindDir9am': [WindDir9am],
                            'WindDir3pm': [WindDir3pm],
                            'WindSpeed9am': [WindSpeed9am],
                            'WindSpeed3pm': [WindSpeed3pm],
                            'Humidity9am': [Humidity9am],
                            'Humidity3pm': [Humidity3am],
                            'Pressure9am': [Pressure9am],
                            'Pressure3pm': [Pressure3am],
                            'Cloud9am': [Cloud9am],
                            'Cloud3pm': [Cloud3am],
                            'Temp9am': [Temp9am],
                            'Temp3pm': [Temp3am],
                            'RainToday': [RainToday],
                            'Year': [year],
                            'Month': [month],
                            'Day': [day]})

    user_input = encoder.transform(user_input)
    user_input = pd.concat([user_input[['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am', 'Temp3pm', 'Year', 'Month', 'Day']], user_input[['RainToday_0', 'RainToday_1']],
                            pd.get_dummies(user_input.Location),
                            pd.get_dummies(user_input.WindGustDir),
                            pd.get_dummies(user_input.WindDir9am),
                            pd.get_dummies(user_input.WindDir3pm)], axis=1)
    
    user_input = user_input.reindex(columns=['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am', 'Temp3pm', 'Year', 'Month', 'Day', 'RainToday_0', 'RainToday_1', 'Adelaide', 'Albany', 'Albury', 'AliceSprings', 'BadgerysCreek', 'Ballarat', 'Bendigo', 'Brisbane', 'Cairns', 'Canberra', 'Cobar', 'CoffsHarbour', 'Dartmoor', 'Darwin', 'GoldCoast', 'Hobart', 'Katherine', 'Launceston', 'Melbourne', 'MelbourneAirport', 'Mildura', 'Moree', 'MountGambier', 'MountGinini', 'Newcastle', 'Nhil', 'NorahHead', 'NorfolkIsland', 'Nuriootpa', 'PearceRAAF', 'Penrith', 'Perth', 'PerthAirport', 'Portland', 'Richmond', 'Sale', 'SalmonGums', 'Sydney', 'SydneyAirport', 'Townsville', 'Tuggeranong', 'Uluru', 'WaggaWagga', 'Walpole', 'Watsonia', 'Williamtown', 'Witchcliffe', 'Wollongong', 'Woomera', 'E', 'ENE', 'ESE', 'N', 'NE', 'NNE', 'NNW', 'NW', 'S', 'SE', 'SSE', 'SSW', 'SW', 'W', 'WNW', 'WSW', 'E', 'ENE', 'ESE', 'N', 'NE', 'NNE', 'NNW', 'NW', 'S', 'SE', 'SSE', 'SSW', 'SW', 'W', 'WNW', 'WSW', 'E', 'ENE', 'ESE', 'N', 'NE', 'NNE', 'NNW', 'NW', 'S', 'SE', 'SSE', 'SSW', 'SW', 'W', 'WNW', 'WSW'], fill_value=0)

    user_input = scaler.transform(user_input)

    prediction = logistic_model.predict(user_input)

    return render_template('wheater-prediction.html', prediction=prediction)

if __name__ == '__main__':
    app.run()