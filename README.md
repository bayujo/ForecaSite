
# ForecaSite

This project is a machine learning application built using Flask, HTML, Tailwind CSS, and deployed on PythonAnywhere. It provides four machine learning models for different predictions: Uber and Lyft fare estimation, rain prediction for today, prediction of patient heart failures due to cardiovascular diseases (CVD), and credit card user clustering. The project utilizes data from various APIs, including WeatherAPI.com for weather data, OpenStreetMap API for point data and map visualization using Leaflet, and calculates the distance between two points for parameter usage.
## Features

- Rain Prediction for Today
Using weather data from WeatherAPI.com, this model predicts the likelihood of rain for the current day. It considers factors like temperature, humidity, wind speed, and historical precipitation patterns to make accurate predictions.
- Rain Prediction for Today
Using weather data from WeatherAPI.com, this model predicts the likelihood of rain for the current day. It considers factors like temperature, humidity, wind speed, and historical precipitation patterns to make accurate predictions.
- Patient Heart Failure Prediction due to CVD
This model aims to predict the occurrence of heart failures in patients with cardiovascular diseases (CVD). By analyzing various patient data such as age, blood pressure, cholesterol levels, and other relevant factors, it provides insights into the risk of heart failure.
- Credit Card User Cluster Prediction
This model categorizes credit card users into different clusters based on their spending patterns, credit limits, and payment behavior. By clustering users, it helps in identifying distinct segments and understanding their characteristics for targeted marketing strategies.


## Stack

This project utilizes the following APIs and frameworks:

- WeatherAPI.com - Provides weather data for accurate rain prediction.
- OpenStreetMap API - Retrieves point data and enables map visualization using Leaflet.
- Flask - A web framework for building the application.
- HTML - Markup language for creating web pages.
- Tailwind CSS - A utility-first CSS framework for designing a visually appealing user interface.
Feel free to explore the code and customize it to suit your requirements.
## Installation

To set up the project locally, follow these steps:

1. Clone the repository: 

```git clone https://github.com/bayujo/ForecaSite.git```

2. Navigate to the project directory: cd project-repo

3. Install the required dependencies: 

```pip install -r requirements.txt```

4. Configure the necessary API keys in the project settings.

5. Run the Flask application: 

```python app.py```

6. Access the project in your web browser at http://localhost:5000.
    
## Contributing

To utilize this project, feel free to fork the repository and adapt it to your needs. It is provided free of charge for learning purposes. If you have any business-related inquiries or need assistance with the project, please feel free to contact me.

## License
This project is released under the MIT License. Feel free to use, modify, and distribute it.
