from citipy import citipy


city = citipy.nearest_city(latitude, longitude)


import matplotlib.pyplot as plt

# Assuming data is in a list of dictionaries
latitudes = [city_data['latitude'] for city_data in city_data_list]
temperatures = [city_data['temperature'] for city_data in city_data_list]

plt.scatter(latitudes, temperatures)
plt.xlabel('Latitude')
plt.ylabel('Temperature (°C)')
plt.title('Latitude vs. Temperature')
plt.show()


from scipy.stats import linregress

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(latitudes, temperatures)

# Plot the regression line
plt.scatter(latitudes, temperatures)
plt.plot(latitudes, slope * np.array(latitudes) + intercept, color='r', label=f'y={slope:.2f}x+{intercept:.2f}')
plt.xlabel('Latitude')
plt.ylabel('Temperature (°C)')
plt.title('Latitude vs. Temperature with Linear Regression')
plt.legend()
plt.show()

# Print the R^2 value
print(f"R^2: {r_value**2}")


import geopandas as gpd
import geoviews as gv
from bokeh.plotting import show

# Assuming you have a DataFrame `city_data_df` with city coordinates and humidity
gdf = gpd.GeoDataFrame(city_data_df, geometry=gpd.points_from_xy(city_data_df['longitude'], city_data_df['latitude']))

# Plot the cities with their humidity values affecting the point size
hv_points = gv.Points(gdf, vdims='humidity').opts(size=hv.dim('humidity')*10)  # Scaling the humidity for visual impact
show(hv_points)


ideal_cities = city_data_df[
    (city_data_df['temperature'] < 27) &
    (city_data_df['temperature'] > 21) &
    (city_data_df['wind_speed'] < 4.5) &
    (city_data_df['cloudiness'] == 0)
]
import requests

# Define Geoapify API key
geoapify_api_key = "YOUR_API_KEY"

# Query for hotels near each city
def find_nearby_hotel(city):
    url = f"https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=circle:{city['longitude']},{city['latitude']},10000&apiKey={geoapify_api_key}"
    response = requests.get(url)
    hotel_data = response.json()
    if hotel_data['features']:
        return hotel_data['features'][0]['properties']['name']
    return "No hotel found"

city_data_df['hotel'] = city_data_df.apply(find_nearby_hotel, axis=1)


hv_points = gv.Points(gdf, vdims=['humidity', 'hotel']).opts(size=hv.dim('humidity')*10, 
                                                           tools=['hover'], 
                                                           hover_cols=['hotel'])
show(hv_points)

