# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 13:10:16 2023

To do's

- Write function to load all the scenarios in the MKDC
    - Use observation type to make the difference between the different hazards
        - So for flooding its in 
- Functon to load the chosen rasterlayer and view (dit lukt nog niet)
- Function to calculate the damages based on the landuse (lukt ook nog niet want nog geen map van damages en land use)
- Functon to display the results map (template)
- Function to display the result in a table, use plotly > this is downloadable
- Button en function to download the results raster (this is possilble)
- Use authenticator (not needed)


@author: Kizje.Marif
"""

#Input packages

import streamlit as st
from streamlit_option_menu import option_menu
import pyproj
import pandas as pd
import requests
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from forex_python.converter import CurrencyRates
import folium
from streamlit_folium import st_folium
from PIL import Image
import time

import branca.colormap as cm
from matplotlib import colormaps


#import leafmap
#import leafmap.foliumap as leafmap

#%% Constants etc


# lizard_headers = {
#     "username": '__key__',
#     "password": ' ',
#     "Content-Type": "application/json",
# }


lizard_headers = {
    "username": st.secrets["USERNAME"],
    "password": st.secrets["PASSWORD"],
    "Content-Type": "application/json",
}


wgs84 = pyproj.CRS("EPSG:4326")
epsg3857 = pyproj.CRS("EPSG:3857")
project = pyproj.Transformer.from_crs(wgs84, epsg3857, always_xy=True).transform

LANDUSE_PIXEL_SIZE = 10
POPULATION_DENSITY_PIXEL_SIZE = 30

# Flooding map for a scenario (later it will be multiple scenario's)
# FLOODING_TEMPLATE_URL = 'https://demo.lizard.net/api/v4/rasters/953f223a-c094-4d03-bfbb-09cd0412387d/'


# r = requests.get(url = FLOODING_TEMPLATE_URL, headers = lizard_headers)
# results = r.json()['options']['styles']

# Displaced people templates
DISPLACED_PEOPLE_TEMPLATE_URL = "https://demo.lizard.net/api/v4/rasters/f612969d-aed9-4b75-800e-1a9ac4c9d98b/template/"

# Damage templates
DAMAGE_TEMPLATE_URL = "https://vietnam.lizard.net/api/v4/rasters/11c27acc-c031-497f-b48d-0c4d3a7ffda6//template/"


#%%%
damage_curve_flood = pd.read_csv('./input/damage_curve_vietnam_flood.csv',sep=';')
#Create plotly graphs for this, dont foret to change the euros to dong

# raster url's of damage maps
template_url = 'https://demo.lizard.net/api/v4/rasters/11c27acc-c031-497f-b48d-0c4d3a7ffda6/'

# get boundary id for specific area (in this case Vietnam)
boundary_url = 'https://nens.lizard.net/api/v4/boundaries/?code={}'.format('VN.CN')
boundary_data = requests.get(url = boundary_url,headers = lizard_headers).json()['results']
boundary_id = boundary_data['features'][0]['id']


# basemaps = {
#     "land use": {
#         "map": "mkdc-projectteam:monre-lulc-v2-reclass",
#         "uuid": "832b8573-6806-4972-abd5-4e694613da08",
#         "center": [50.86505, 5.83576],
#         "zoom": 14,
#         "pixel_size": 10,
#     },
#     "populatation": {
#         "map": "nelen-schuurmans-consultancy:global_population_general_abm_tool",
#         "uuid": "16171a5f-be38-4287-a8e1-4acb0c6b4879",
#         "center": [50.86505, 5.83576],
#         "zoom": 14,
#         "pixel_size": 0.5,
#     }}


wms_layers = [
    {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name":"Land use",
        "layers": "mkdc-projectteam:monre-lulc-v2-reclass",
        "time": 20#timestep_4wk
    },
    {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name":"Gemiddeld - 4 weken",
        "layers": "waterschap-limburg-dtw:historische-grondwaterstanden-nat",
        "time": 20#timestep_4wk
    },]

wms_layers_1 = [
     {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name": "JAXA LULC 2020",
        "layers": "mkdc-projectteam:jaxa-lulc-2020",
        "styles":"mkdc-lulc-jaxa",
        # "time": rasteryear,
     },
     {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name": "MONRE LULC DSS-5",
        "layers": "mkdc-projectteam:monre-lulc-dss-5",
        "styles":"mkdc-lulc",
        # "time": rasteryear,
     },
    {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name":"DSS-5 Flood template",
        "layers": "mkdc-projectteam:dss-5-flood-template",
        "styles": '3di-depth'#timestep_4wk
    },
    {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name": "Geoblock template damage flood",
        "layers": "mkdc-projectteam:geoblock-template-flood-tpkpupjs",
        "styles": '3di-damage-estim:0:1000000'#timestep_4wk
     }]



#%%Data load and overview

# harde manier om legend uit lizard te krijgen, geen betere oplossing?
# import xml.etree.ElementTree as xmlet
# import lxml.etree as xmltree
# from IPython.display import Image, display
# from PIL import Image

# url_legend_flooding = 'https://demo.lizard.net/wms/raster_953f223a-c094-4d03-bfbb-09cd0412387d/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:dss-5-flood-template&style=3di-depth'

# im_legend_flooding = Image.open(requests.get(url_legend_flooding, stream=True).raw)





# Functions

    


# def generate_damage(
#     waterdepth_uuid
#     # flood_residential_maximum,
#     # polygon_wkt,
#     # waterdepth_sink,
#     # waterdepth_pixel_size,
# ):

#     #if waterdepth_pixel_size < LANDUSE_PIXEL_SIZE:
#     #    correction = waterdepth_pixel_size ** 2
#     #else:
#     #    correction = LANDUSE_PIXEL_SIZE ** 2
#     json = {https://demo.lizard.net/wms/scenario_6f311736-690b-4384-9fb4-7a2af11e2e79/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=scenarios:35278:depth-dtri&style=3di_waterdepth:0.0:2.0"/
#         "flood_map": waterdepth_uuid
#         # "flood_residential_maximum": flood_residential_maximum * 1,
#         # "measure": polygon_wkt,
#         # "sink_raster": waterdepth_sink,
#     }
#     params = {
#         "parameters": {key: value for key, value in json.items() if value is not None}
#     }

#     r = requests.post(url=DAMAGE_TEMPLATE_URL, json=params, headers=HEADERS)
#     results = r.json()
#     damage_map = results["wms_info"]["layer"]
#     damage_url = results["url"]

#     return damage_map, damage_url



poly_wkt = boundary_data['features'][0]['id']
pixel_size = 10 # make check that chose raster with smallest pixel size and use that pixel size


def get_zonal_sum(template_url, poly_wkt, pixel_size):
    # used to calculate total damage in area
    
    
    params = {
        "geom": poly_wkt,
        "zonal_statistic": "sum",
        "zonal_projection": "EPSG:3857",
        "pixel_size": pixel_size,
        'auto_pixel_size': True # dit hoort eigenlijk niet, maar zegt dat raster nog steeds te groot is
    }
    
    params = {key: value for key, value in params.items() if value is not None}

    zonal_request_url = template_url + "zonal"
    zonal_request = requests.get(zonal_request_url, params=params, headers=lizard_headers)

    print(params)
    print(zonal_request.json())

    try:
        zonal_value = zonal_request.json()["results"][0]["value"]
    except:
        zonal_value = 0

    return zonal_value




# def get_zonal_area(template_url, poly_wkt, pixel_size):

#     params = {
#         "geom": poly_wkt,
#         "zonal_statistic": "count",
#         "zonal_projection": "EPSG:3857",
#         "pixel_size": pixel_size,
#     }

#     params = {key: value for key, value in params.items() if value is not None}


#     zonal_request_url = template_url + "zonal"
#     zonal_request = requests.get(zonal_request_url, params=params, headers=lizard_headers)

#     try:
#         zonal_value = zonal_request.json()["results"][0]["value"]
#     except:
#         zonal_value = 0

#     area = zonal_value * pixel_size

#     return area



# def initial_scenario_changed(selected_map_initial):
#     if selected_map_initial is not None:
#         waterdepth_initial_uuid = AVAILABLE_SCENARIOS[selected_map_initial]["uuid"]
#         waterdepth_initial_map = AVAILABLE_SCENARIOS[selected_map_initial]["map"]
#         waterdepth_intial_pixel_size = AVAILABLE_SCENARIOS[selected_map_initial][
#             "pixel_size"
#         ]
#         waterdepth_initial_output = {
#             "map": waterdepth_initial_map,
#             "uuid": waterdepth_initial_uuid,
#             "pixel_size": waterdepth_intial_pixel_size,
#         }
#         return waterdepth_initial_output

#     else:
#         print('nothing selected')

# def update_displaced_people_initial(waterdepth_initial_data):

#     waterdepth_initial_uuid = waterdepth_initial_data["uuid"]

#     if waterdepth_initial_uuid is not None:

#         waterdepth_pixel_size = waterdepth_initial_data["pixel_size"]

#         displaced_people_map, displaced_people_url = generate_displaced_people(
#             waterdepth_uuid=waterdepth_initial_uuid,
#             waterdepth_pixel_size=waterdepth_pixel_size,
#             polygon_wkt=None,
#             waterdepth_sink=None,
#         )
#         displaced_people_initial_output = {
#             "map": displaced_people_map,
#             "url": displaced_people_url,
#         }
#         return displaced_people_initial_output

#     else:
#         print('nothing selected')


#%%
# pre-process data

#change from euro's (EUR) to Vietnamese dong (VND)
c = CurrencyRates()
euro_to_dong = 26045.58 # would be nice if this goes automatically

damage_curve_flood[['Residential damage (E/m2)', 
                    'Agricultural damage (E/m2)', 
                    'Commercial damage (E/m2)',
                    'Industrial damage (E/m2)', 
                    'Infrastructural damage (E/m2)',
                    'Transport damage (E/m2)']] = damage_curve_flood[['Residential damage (E/m2)', 
                                                                            'Agricultural damage (E/m2)', 
                                                                            'Commercial damage (E/m2)',
                                                                            'Industrial damage (E/m2)', 
                                                                            'Infrastructural damage (E/m2)', 
                                                                            'Transport damage (E/m2)']].multiply(euro_to_dong)

# latitude and longitude of place of interest                                                                            
lat = '10.08'
lon = '105.73'

#%%
def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Home", "Projects", "Contact"],  # required
                icons=["house", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Projects", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Floods", "Drought",'Saline intrusion',"Landslide"],  # required
            icons=["water", "sun","salt" ,'moon'],  # optional
            # menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#00A9C1","color":"white"},
            },
        )
        return selected
 
st.set_page_config(page_title="DSS 5", page_icon=":water:", layout="wide")

EXAMPLE_NO = 3
st.write('  ')
selected = streamlit_menu(example=EXAMPLE_NO)

# =============================================================================
# Body of dashboard
# =============================================================================

if selected == 'Floods':

    col1, col2, col3 = st.columns([0.2,0.79,0.01])
    
    #introduce session state to store the 'pressed' state of each button
    if "button1" not in st.session_state: # 1 = Damage curve
        st.session_state["button1"] =False
     
    if "button2" not in st.session_state: # 2 = Land use
        st.session_state["button2"] = False
    
    if "button3" not in st.session_state: # 3 = Calculate Damage
        st.session_state["button3"] = False
        
    if "button4" not in st.session_state: # 3 = Go back to Flood map
        st.session_state["button4"] = False 
        
    # if 'button5' not in st.session_state:
    #     st.session_state['button5']
    
    with col1:
        # Section 1: Select Scenario and Display Map
        st.header("Menu")
        
        # use this later on
        #scenarios = ["Scenario 1", "Scenario 2", "Scenario 3", 'template']
        
        #demo
        scenarios = ['template']
        
        selected_scenario = st.selectbox("Select a Scenario", scenarios)
    
        if selected_scenario == 'template':
            selected_scenario = 'DSS-5 Flood'
     
        if st.button("Flood map"):
            # toggle button3 session state
            st.session_state["button4"] = not st.session_state["button4"]
            st.session_state["button1"] =False
            st.session_state["button2"] = False
            st.session_state["button3"] = False    
           # st.session_state["button5"] = False
     
        st.write('Choose background information:')
            
        if st.button("Go to Damage Curve"):
            st.session_state["button1"] = not st.session_state["button1"]
            st.session_state["button3"] = False
            st.session_state["button2"] = False
            st.session_state["button4"] = False
           # st.session_state["button5"] = False
            
        if st.button("Go to Land Use"):
            st.session_state["button2"] = not st.session_state["button2"]
            st.session_state["button1"] =False
            st.session_state["button3"] = False
            st.session_state["button4"] = False
            #st.session_state["button5"] = False
        
        st.write('   ')
        st.write('Make calculations:')
        
            
        if st.button("Calculate Damage", type= 'primary'):
            # toggle button3 session state
            st.session_state["button3"] = not st.session_state["button3"]
            st.session_state["button1"] =False
            st.session_state["button2"] = False
            st.session_state["button4"] = False

           
    
    
                
    
    
    with col2:
        
        
        subcol1, subcol2 = st.columns([0.8, 0.2])
        if st.session_state['button4']:
            
            if selected_scenario == 'DSS-5 Flood':
        
                for layer in wms_layers_1:
                    if selected_scenario in layer["name"]:
                        with subcol1:
                            st.subheader('Flood map')
                            folium_map_start = folium.Map(location=[lat, lon], zoom_start=11)
                            folium.raster_layers.WmsTileLayer(
                                url = layer['url'],
                                name = layer['name'],
                                format = 'image/png',
                                layers = layer['layers'],
                                transparent = False,
                                overlay = True,
                                opacity = 0.95,
                                styles = layer['styles'],
                                show = True, 
                                control = True).add_to(folium_map_start)
                            
                            
                            
                            folium.LayerControl().add_to(folium_map_start)
                            
                            #colormap.add_to(folium_map_start) --> check wat wenselijk is?
                            #FloatImage(im, bottom=0, left=86).add_to(folium_map_start) 
                            #folium_map_start.add_child(colormap)
                            st_data_start = st_folium(folium_map_start, width = 900, height= 400)
                            
                            st.session_state["flood_map"] = folium_map_start
                        with subcol2:
                            # show legengd of flooding map    
                            url_legend_flooding = 'https://demo.lizard.net/wms/raster_953f223a-c094-4d03-bfbb-09cd0412387d/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:dss-5-flood-template&style=3di-depth'     
                            im_legend_flooding = Image.open(requests.get(url_legend_flooding, stream=True).raw)   
                            st.image(im_legend_flooding, caption='waterdepth (m)')
    # For demo not relevant
    # =============================================================================
    #         elif selected_scenario == 'Scenario 2':
    #             with subcol1:
    #                 st.subheader('Flood map')
    #                 folium_map_start = folium.Map(location=[lat, lon], zoom_start=11)
    #                 st_data_start = st_folium(folium_map_start, width = 900, height= 400)
    #                 st.write('For this scenario there is no data available, but shows that switching between scenarios directly results in related map (as an example).')
    #             with subcol2:
    #                 # show legengd of flooding map    
    #                 url_legend_flooding = 'https://demo.lizard.net/wms/raster_953f223a-c094-4d03-bfbb-09cd0412387d/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:dss-5-flood-template&style=3di-depth'     
    #                 im_legend_flooding = Image.open(requests.get(url_legend_flooding, stream=True).raw)   
    #                 st.image(im_legend_flooding, caption='waterdepth (m)')                        
    #         else:
    #             st.subheader('Flood map')
    #             st.write(' no data available for this scenario. Choice the template scenario for a nice example')
    # =============================================================================
                
        if st.session_state["button1"]: # add under this line damage curve
    
            #st.header("Step 2: Damage Curves")
            
            # Load and display bar plots of damage curves here.
            # You can use Plotly, Matplotlib, or any other plotting library.
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Residential damage (E/m2)'], name='Residential damage',
                                  line=dict(color='firebrick', width=1)))
            fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Agricultural damage (E/m2)'], name='Agricultural damage',
                                  line=dict(color='royalblue', width=1)))   
            fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Commercial damage (E/m2)'], name='Commercial damage',
                                  line=dict(color='orange', width=1)))
            fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Industrial damage (E/m2)'], name='Industrial damage',
                                  line=dict(color='purple', width=1))) 
            fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Infrastructural damage (E/m2)'], name='Infrastructural damage',
                                  line=dict(color='darkgreen', width=1)))
            fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Transport damage (E/m2)'], name='Transport damage',
                                  line=dict(color='yellow', width=1)))
            
            fig.update_layout(title='Damage curves per land use',
                            xaxis_title='Flood depth (m)',
                            yaxis_title='Damage (VND/m2)') 
            
            st.plotly_chart(fig, use_container_width=True) 
            
        if st.session_state["button2"]: #add under this line land use and population maps
    
            #st.header("Step 3: Land use and population")
            col1, col2 = st.columns([0.7, 0.3])
            # Display the first WMS map
            with col1:
                st.subheader("Landuse map")
                
                for layer in wms_layers_1:
                    #find way to add legend
                    # maybe use layer in basemap?
                    if 'MONRE' in layer["name"]:
                        folium_map_lucl = folium.Map(location=[lat, lon], zoom_start=10)
                        folium.raster_layers.WmsTileLayer(
                            url = layer['url'],
                            name = layer['name'],
                            format = 'image/png',
                            layers = layer['layers'],
                            transparent = True,
                            overlay = True,
                            opacity = 0.95,
                            styles = layer['styles'],
                            show = True, 
                            control = True).add_to(folium_map_lucl)
                        
                        folium.LayerControl().add_to(folium_map_lucl)
                        #folium_map_start.add_child(colormap)
                        st_data_lucl = st_folium(folium_map_lucl, width = 800, height= 400)
                    
                with col2:
                    #show legend of land use map
                    url_legend_landuse = 'https://demo.lizard.net/wms/raster_67cc7ab8-f63b-4a0e-9e68-cfe9ad046eb4/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:monre-lulc-dss-5&style=mkdc-lulc'
                    im_legend_landuse = Image.open(requests.get(url_legend_landuse, stream=True).raw)
                    st.image(im_legend_landuse, caption='Legend')
                    
        if st.session_state["button3"]: #add under this line the table with damages per land use class
            if "button5" not in st.session_state: # 1 = Damage curve
                st.session_state["button5"] =True
             
            if "button6" not in st.session_state: # 2 = Land use
                st.session_state["button6"] = False
            
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                if st.button("Map"):
                # toggle button3 session state
                    st.session_state["button5"] = not st.session_state["button5"]
                    st.session_state["button6"] =False
            with col2:
                if st.button("Statistics"):
                    # toggle button3 session state
                    st.session_state["button6"] = not st.session_state["button6"]
                    st.session_state["button5"] =False
 
        
        
    
            #st.header("Step 4: Calculate Damage")
    
                #     # Collect user input for damage calculation (if any).
                #     # Perform damage calculations based on user inputs and selected_scenario.
                            # Not sure, but not nessecary? 
                            # Only show the total damage (map and number)+
                            # affected people (splitted in men, woman, child, map and number)
                #     # Display the table with damages per land use class.
                #     # You can use Pandas DataFrames to present the data in a table.
            if st.session_state["button5"]:
                
            
                col1, col2 = st.columns([0.8, 0.2])
                if selected_scenario == 'DSS-5 Flood':
                
                
                    with col1:
                        st.subheader("Calculated Damage Map")
                        with st.spinner('Calculating...'):
                            time.sleep(5)
                        for layer in wms_layers_1:
                            #find way to add legend
                            # maybe use layer in basemap?
                            if 'Geoblock' in layer["name"]:
                                folium_map_damage = folium.Map(location=[lat, lon], zoom_start=11)
                                folium.raster_layers.WmsTileLayer(
                                    url = layer['url'],
                                    name = layer['name'],
                                    format = 'image/png',
                                    layers = layer['layers'],
                                    transparent = True,
                                    overlay = True,
                                    opacity = 0.95,
                                    styles = layer['styles'],
                                    show = True, 
                                    control = True).add_to(folium_map_damage)
                                
                                folium.LayerControl().add_to(folium_map_damage)
                                #folium_map_start.add_child(colormap)
                                st_data_damage = st_folium(folium_map_damage, width = 900, height= 400)
                                                            
                        
                    with col2:
                    
                        # show legend damage map
                        url_legend_damage = 'https://demo.lizard.net/wms/raster_11c27acc-c031-497f-b48d-0c4d3a7ffda6/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:geoblock-template-flood-tpkpupjs&style=3di-damage-estim:0:1000000'
                        im_legend_damage = Image.open(requests.get(url_legend_damage, stream=True).raw)
                        st.image(im_legend_damage, caption='Damage (VND/m2)')
                        
            if st.session_state["button6"]:    
                st.subheader("Damage Statistics")
                with st.spinner('Calculating...'):
                    time.sleep(5)
                    
                zonal_val = get_zonal_sum(template_url, boundary_id, LANDUSE_PIXEL_SIZE)
                st.write('The total damage caused by flooding is '+str(zonal_val)+' VND')
                
           

# for other taps, add text that it's not working yet
else:
    st.write('Not working yet')
                
                

                
# For demo not relevant                
# =============================================================================
#         elif selected_scenario == 'Scenario 2':
#             with subcol1:
#                 st.subheader('Calculated Damage Map')
#                 folium_map_start = folium.Map(location=[lat, lon], zoom_start=11)
#                 st_data_start = st_folium(folium_map_start, width = 900, height= 400)
#                 st.write('For this scenario there is no data available, but shows that switching between scenarios directly results in related map (as an example).')
#             with subcol2:
#                 # show legend damage map    
#                 url_legend_damage = 'https://demo.lizard.net/wms/raster_11c27acc-c031-497f-b48d-0c4d3a7ffda6/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:geoblock-template-flood-tpkpupjs&style=3di-damage-estim:0:1000000'
#                 im_legend_damage = Image.open(requests.get(url_legend_damage, stream=True).raw)
#                 st.image(im_legend_damage, caption='Damage (VND/m2)')                      
#         else:
#             st.subheader('Calculated Damage Map')
#             st.write(' no data available for this scenario. Choice the template scenario for a nice example ')
# =============================================================================
            
        

 

    


# You can use selected_scenario to load the corresponding map.
# check how map can be downloaded from Lizard? and which map it really is

# introduce session state to store the 'pressed' state of each button

# if "button1" not in st.session_state:
#     st.session_state["button1"] = False

# if "button2" not in st.session_state:
#     st.session_state["button2"] = False

# if "button3" not in st.session_state:
#     st.session_state["button3"] = False

# if st.button("Go to Damage Curve"):
#     st.session_state["button1"] = not st.session_state["button1"]
    
# if st.session_state["button1"]: # add under this line damage curve

#     st.header("Step 2: Damage Curves")
    
#     # Load and display bar plots of damage curves here.
#     # You can use Plotly, Matplotlib, or any other plotting library.
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Residential damage (E/m2)'], name='Residential damage',
#                          line=dict(color='firebrick', width=1)))
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Agricultural damage (E/m2)'], name='Agricultural damage',
#                          line=dict(color='royalblue', width=1)))   
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Commercial damage (E/m2)'], name='Commercial damage',
#                          line=dict(color='orange', width=1)))
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Industrial damage (E/m2)'], name='Industrial damage',
#                          line=dict(color='purple', width=1))) 
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Infrastructural damage (E/m2)'], name='Infrastructural damage',
#                          line=dict(color='darkgreen', width=1)))
    
#     fig.update_layout(title='Damage curves per land use',
#                    xaxis_title='Flood depth (m)',
#                    yaxis_title='Damage (VND/m2)') 
    
#     st.plotly_chart(fig, use_container_width=True)    
    

# if st.session_state["button1"]:
#     # Add a 'Next' button to move to the next section
#     if st.button("Go to Land Use and Population"):
#         st.session_state["button2"] = not st.session_state["button2"]

# if st.session_state["button2"]: #add under this line land use and population maps

#     st.header("Step 3: Land use and population")
#     col1, col2 = st.columns([0.7, 0.3])
#     # Display the first WMS map
#     with col1:
#         st.subheader("Landuse map")
        
#         for layer in wms_layers_1:
#             #find way to add legend
#             # maybe use layer in basemap?
#             if 'JAXA' in layer["name"]:
#                 folium_map_lucl = folium.Map(location=[lat, lon], zoom_start=11)
#                 folium.raster_layers.WmsTileLayer(
#                     url = layer['url'],
#                     name = layer['name'],
#                     format = 'image/png',
#                     layers = layer['layers'],
#                     transparent = True,
#                     overlay = True,
#                     opacity = 0.95,
#                     styles = layer['styles'],
#                     show = True, 
#                     control = True).add_to(folium_map_lucl)
                
#                 folium.LayerControl().add_to(folium_map_lucl)
#                 #folium_map_start.add_child(colormap)
#                 st_data_lucl = st_folium(folium_map_lucl, width = 800, height= 400)
                
#         st.subheader('Population density map')
        
#         folium_map_pop = folium.Map(location=[lat, lon], zoom_start=11)
#         #folium.WmsTileLayer(wms_url_2).add_to(folium_map_pop)
#         st_data2 =st_folium(folium_map_pop, width = 800, height= 400) 

#         #folium_map_1 = folium.Map(location=[lat, lon], zoom_start=2)
#     #     folium.WmsTileLayer(wms_url_1).add_to(folium_map_1)
#         #st_data = st_folium(folium_map_1)
    
#
#     with col2:
#         #show legend of land use map
#         url_legend_landuse = 'https://demo.lizard.net/wms/raster_8d212c0e-18cd-481c-9337-d4e357056555/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:jaxa-lulc-2020&style=mkdc-lulc-jaxa'
#         im_legend_landuse = Image.open(requests.get(url_legend_landuse, stream=True).raw)
#         st.image(im_legend_landuse, caption='Legend')
       

# if st.session_state["button1"] and st.session_state["button2"]:
#     # Add a 'Next' button to move to the next section
#     if st.button("Calculate damage"):
#         # toggle button3 session state
#         st.session_state["button3"] = not st.session_state["button3"]

# if st.session_state["button3"]: #add under this line the table with damages per land use class

#     st.header("Step 4: Calculate Damage")

#         #     # Collect user input for damage calculation (if any).
#         #     # Perform damage calculations based on user inputs and selected_scenario.
#                     # Not sure, but not nessecary? 
#                     # Only show the total damage (map and number)+
#                     # affected people (splitted in men, woman, child, map and number)
#         #     # Display the table with damages per land use class.
#         #     # You can use Pandas DataFrames to present the data in a table.
#     col1, col2 = st.columns([0.8, 0.2])
#     with col1:
    
#         for layer in wms_layers_1:
#             #find way to add legend
#             # maybe use layer in basemap?
#             if 'Geoblock' in layer["name"]:
#                 folium_map_damage = folium.Map(location=[lat, lon], zoom_start=11)
#                 folium.raster_layers.WmsTileLayer(
#                     url = layer['url'],
#                     name = layer['name'],
#                     format = 'image/png',
#                     layers = layer['layers'],
#                     transparent = True,
#                     overlay = True,
#                     opacity = 0.95,
#                     styles = layer['styles'],
#                     show = True, 
#                     control = True).add_to(folium_map_damage)
                
#                 folium.LayerControl().add_to(folium_map_damage)
#                 #folium_map_start.add_child(colormap)
#                 st_data_damage = st_folium(folium_map_damage, width = 900, height= 400)
#     with col2:
    
#         # show legend damage map
#         url_legend_damage = 'https://demo.lizard.net/wms/raster_11c27acc-c031-497f-b48d-0c4d3a7ffda6/?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=256&height=256&layer=mkdc-projectteam:geoblock-template-flood-tpkpupjs&style=3di-damage-estim:0:1000000'
#         im_legend_damage = Image.open(requests.get(url_legend_damage, stream=True).raw)
#         st.image(im_legend_damage, caption='Damage (VND/m2)')

#---------------------------------------------------------------------------------------------

# if "Go to Damage Curve_1" not in st.session_state:
#     st.session_state["Go to Damage Curve_1"] = False
# if "Go to Land Use and Population_2" not in st.session_state:
#     st.session_state["Go to Land Use and Population_2"] = False
# #if "button3" not in st.session_state:
# #    st.session_state["button3"] = False
    
# if st.button("Go to Damage Curve"):
#     st.session_state["Go to Damage Curve_1"] = not st.session_state["Go to Damage Curve_1"]
    
# if st.session_state["Go to Damage Curve_1"]:
    
    
# # Add a 'Next' button to move to the next section
# #if st.button("Go to Damage Curve"):
#     st.header("Step 2: Damage Curves")

#     # Load and display bar plots of damage curves here.
#     # You can use Plotly, Matplotlib, or any other plotting library.
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Residential damage (E/m2)'], name='Residential damage',
#                          line=dict(color='firebrick', width=1)))
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Agricultural damage (E/m2)'], name='Agricultural damage',
#                          line=dict(color='royalblue', width=1)))   
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Commercial damage (E/m2)'], name='Commercial damage',
#                          line=dict(color='orange', width=1)))
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Industrial damage (E/m2)'], name='Industrial damage',
#                          line=dict(color='purple', width=1))) 
#     fig.add_trace(go.Scatter(x = damage_curve_flood['Flood depth'], y = damage_curve_flood['Infrastructural damage (E/m2)'], name='Infrastructural damage',
#                          line=dict(color='darkgreen', width=1)))
    
#     fig.update_layout(title='Damage curves per land use',
#                    xaxis_title='Flood depth (m)',
#                    yaxis_title='Damage (VND/m2)') 
    
#     st.plotly_chart(fig, use_container_width=True)
#     #verder uitwerken voor andere landuses
    

    
    
#     #plot(fig)
#     #fig.update_layout(title= "{} R2 is {} and NSE is {}".format(poldername, r2_val1, nse_val1))

    

#     if st.button("Go to Land Use and Population"):
#         st.session_state["Go to Land Use and Population_2"] = not st.session_state["Go to Land Use and Population_2"]
        
# if st.session_state('Go to Land Use and Population_2'):
#     # Add a 'Next' button to move to the next section
#     #if st.button("Go to Land Use and Population"):
#         st.write('hello')
#         # col1, col2 = st.columns(2)
#         # st.header("Step 3: Land use and population")
#         #  #Display the first WMS map
#         # with col1:
#         #     st.subheader("Landuse map")
#         #     folium_map_1 = folium.Map(location=[39, -75], zoom_start=2, tiles=None)
#         # #     folium.WmsTileLayer(wms_url_1).add_to(folium_map_1)
#         #     st_data = st_folium(folium_map_1)
        
#         # # Display the second WMS map
#         # with col2:
#         #       st.subheader("Population density map")
#         #       folium_map_2 = folium.Map(location=[50, -75], zoom_start=2, tiles=None)
#         #       #folium.WmsTileLayer(wms_url_2).add_to(folium_map_2)
#         #       st_data2 =st_folium(folium_map_2)    

    
#         # if st.button("Calculate damage"):
#         #      st.header("Step 4: Calculate Damage")

#         #     # Collect user input for damage calculation (if any).
#         #     # Perform damage calculations based on user inputs and selected_scenario.

#         #     # Display the table with damages per land use class.
#         #     # You can use Pandas DataFrames to present the data in a table.