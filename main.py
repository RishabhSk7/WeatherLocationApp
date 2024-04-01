from pyowm import OWM
from cityclass import city
from locationclass import location
from pyowm.utils import timestamps
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
        text-align: left;
        } 
        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: center;
        } 
        div[data-testid="column"]:nth-of-type(3)
        {
            text-align: right;
        } 
        div[data-testid="column"]:nth-of-type(5)
        {
            text-align: left;
        } 
        .big-font {
        font-size:22px;
        }
    </style>
    """,unsafe_allow_html=True
)

global key, reg, url
url = "https://weatherapi-com.p.rapidapi.com/future.json"
key = OWM("9566bfafde80b413d3258b9f291bb4b1")

#9566bfafde80b413d3258b9f291bb4b1
reg = key.city_id_registry()

def return_closest_city(reg, name):
    closest = reg.ids_for(name, matching='like')
    return closest

col1, padding,padding1,col2 = st.columns((10,2,2,10), gap="large")
col3, col4, col5 = col2.columns(3)
col1.title("Weather Information")
col1.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

global place, unit
place=col1.text_input("NAME OF THE CITY :", "")
unit=col1.selectbox("Select Temperature Unit",("celsius","fahrenheit"))
#g_type=col1.selectbox("Select Graph Type",("Line Graph","Bar Graph"))
placeholder = col1.empty()

if col1.button("Go"):

    closest = return_closest_city(reg, place)

    if len(closest)>0:
        col1.map(pd.DataFrame([[closest[0][-2], closest[0][-1]]], columns=["lat", "lon"]), zoom=11)
    
        c1 = city(key, closest[0], url)
        col3.metric("Weather", f"{c1.current_weather()}", "")
        col4.metric(f"Temperature", str(c1.today_temprature(unit=unit))+" "+unit.title())
        wind = c1.current_wind()
        col5.metric(f"Wind", str(wind.get('speed'))+"kmph")

        rain  = c1.current_rain()
        col2.write('')
        col2.write('')
        col2.write('')
        col2.write('')
        col2.write('')
        col2.write('')
        
        if len(rain.values()) == 0:
            col2.markdown("<p class='big-font'>There has been no rain recently.</p>", unsafe_allow_html=True)
        else:
            col2.markdown("<p class='big-font'>Rain in the last: </p>", unsafe_allow_html=True)
            for key, value in rain.items():
                col2.markdown(f"<p class='big-font'>{key}: {value}mms.</p>", unsafe_allow_html=True)

        col2.markdown(f"<p class='big-font'>Visibility of {c1.visibility()} Meters</p>", unsafe_allow_html=True)

        a = c1.sun_timings()
        col2.markdown(f'''<p class='big-font'>Sun rise at: {a[0]}<br>
        Sunset at: {a[1]}</p>''', unsafe_allow_html=True)

        # c1.weather_day_forecast()

        a = c1.air_pollutants()
        col2.markdown(f'''<p class='big-font'>Air Pollutants:\n
        Carbon Monoxide level: {a[0]}\n
    Nitric Oxide level: {a[1]}\n
    Nitrogen Dioxide level: {a[2]}\n
    Ozone level: {a[3]}\n
    Sulphur Dioxide level: {a[4]}\n
    Particulate Matter(PM2.5) level: {a[5]}\n
    Particulate Matter(PM10) level: {a[6]}\n
    Ammonia level: {a[7]}</p>''', unsafe_allow_html=True)  



    else:
        col2.write("name not recognisable, please enter a valid name")

# l1 = location(key)
# """coords = [float(x) for x in input("Enter coordinates for radial search: ").split(" ")]
# lim = int(input("Enter limit for radial search: "))
# l1.radial_search(coords, lim) """

#coords = [float(x) for x in input("Enter coordinates for box search: ").split(" ")]
#zoom = int(input("Enter limit for box search: "))
#l1.box_search(coords, zoom)
