# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 11:01:28 2023

@author: pvantets
"""

import streamlit as st
import requests
import pandas as pd
import leafmap.foliumap as leafmap
import folium
from shapely.geometry import shape
from pyproj import Proj

# Define the headers for authentication
HEADERS = {
    "username": st.secrets["USERNAME"],
    "password": st.secrets["PASSWORD"],
    "Content-Type": "application/json",
}

classes_monre_details = pd.read_csv("input/koppeltabel_monre_statistieken.csv")
classes_jaxa_details = pd.read_csv("input/koppeltabel_jaxa_statistieken.csv")
classes_jaxa_temp_details = pd.read_csv("input/koppeltabel_jaxa_statistieken_temp.csv")

provinces = ["VN.AG", "VN.BL", "VN.BR", "VN.CM", "VN.CN", "VN.DT", "VN.HU", "VN.KG", "VN.LA", "VN.ST", "VN.TG", "VN.TV", "VN.VL"]
raster_url_monre = "https://vietnam.lizard.net/api/v4/rasters/b789b10d-969e-4d5d-ad66-ec86820d2517/" # MONRE
raster_url_jaxa = "https://vietnam.lizard.net/api/v4/rasters/8d212c0e-18cd-481c-9337-d4e357056555/"
raster_url_jaxa_temp = "https://nens.lizard.net/api/v4/rasters/cd58d436-d2b9-4f95-a20d-985c7c454ae2/"
raster_style = "mkdc-lulc-monre-classes"
raster_style_jaxa = "mkdc-lulc-jaxa"
raster_style_jaxa_temp = "JAXA_LULC_1990-2020"

lat = '10'
lon = '105.8'

jaxa_time_dictionary = {'1990': '1990-06-19T20:00:00Z', '1991': '1991-06-19T20:00:00Z', '1992': '1992-06-18T20:00:00Z', '1993': '1993-06-18T20:00:00Z', 
                        '1994': '1994-06-18T20:00:00Z', '1995': '1995-06-18T20:00:00Z', '1996': '1996-06-17T20:00:00Z', '1997': '1997-06-17T20:00:00Z', 
                        '1998': '1998-06-17T20:00:00Z', '1999': '1999-06-17T20:00:00Z', '2000': '2000-06-16T20:00:00Z', '2001': '2001-06-16T20:00:00Z', 
                        '2002': '2002-06-16T20:00:00Z', '2003': '2003-06-16T20:00:00Z', '2004': '2004-06-15T20:00:00Z', '2005': '2005-06-15T20:00:00Z', 
                        '2006': '2006-06-15T20:00:00Z', '2007': '2007-06-15T20:00:00Z', '2008': '2008-06-14T20:00:00Z', '2009': '2009-06-14T20:00:00Z', 
                        '2010': '2010-06-14T20:00:00Z', '2011': '2011-06-14T20:00:00Z', '2012': '2012-06-13T20:00:00Z', '2013': '2013-06-13T20:00:00Z', 
                        '2014': '2014-06-13T20:00:00Z', '2015': '2015-06-13T20:00:00Z', '2016': '2016-06-12T20:00:00Z', '2017': '2017-06-12T20:00:00Z', 
                        '2018': '2018-06-12T20:00:00Z', '2019': '2019-06-12T20:00:00Z', '2020': '2020-06-11T20:00:00Z'}

#%% Legends opvragen: eenmalig gebruikt, niet operationeel vanwege request tijd en data
def get_legend(lulc_option, year_option):
    if lulc_option == "MONRE":
        legend_url = "https://vietnam.lizard.net/wms/?layer=mkdc-projectteam%3Amonre-lulc-v2&request=getlegend&service=wms&style=mkdc-lulc-monre-classes"
    elif lulc_option == "JAXA":
        if year_option == 2020:
            legend_url = "https://vietnam.lizard.net/wms/?layer=mkdc-projectteam%3Ajaxa-lulc-2020&request=getlegend&service=wms&style=mkdc-lulc-jaxa"
    else:
        print("legend option not configured")
        return
    r = requests.get(url=legend_url, headers=HEADERS)
    legend_dict = r.json()
    labels = list(next(iter(legend_dict["labels"].values())).values())
    colors_dict = legend_dict["legend"]
    colors = []
    for color in colors_dict:
        colors.append(color['color'])
    return labels, colors



#%% Functions

def create_map(lulc_option): 
    m = leafmap.Map(
        center=(lat, lon),
        zoom=8,
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        tiles="CartoDB positron",
    )
    
    wms_layers = [
        {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name": "MONRE land use land cover",
        "layers": "mkdc-projectteam:monre-lulc-v2",
        "styles":raster_style,
        "labels":['Annual cropland', 'Land for rice cultivation', 'Land for perennial crops', 'Forestry land', 'Production forest land', 'Protection forest land', 
                  'Special-use forest land', 'Aquaculture land', 'Soil for salt', 'Other agricultural land', 'Landscape', 'Land in countryside', 'Land in urban areas', 
                  'Land to build office headquarters', 'Defense land', 'Security land', 'Land for construction of non-business works', 'Non-agricultural production and business land', 
                  'Land for public purposes', 'Land transport', 'Irrigation land', 'Land for energy works', 'Land cemetery, cemetery, funeral home, crematorium', 
                  'Land of rivers, streams, canals, canals, streams', 'Land with specialized water surface', 'Unused flat land', 'Unused hilly land', 'Rocky mountains without trees'],
        "colors":['#0080FF', '#0080FF', '#0080FF', '#006400', '#006400', '#806400', '#006400', '#4D68FF', '#8AB9D1', '#FFC1BF', '#ABDA9D', '#ABDA9D', '#ABDA9D', 
                  '#FF0000', '#FF0000', '#FF0000', '#FF0000', '#FF0000', '#FF0000', '#FF0000', '#FF0000', '#FF0000', '#FF0000', '#000064', '#000064', '#E1E100', '#80FF00', '#BABABA']
        # "time": rasteryear,
        },
        {
        "url": "https://demo.lizard.net/wms/verdamping/?SERVICE=WMS",
        "name": "JAXA LULC 2020",
        "layers": "mkdc-projectteam:jaxa-lulc-2020",
        "styles":raster_style_jaxa,
        "labels": ['Water',     'Urban/Built-up',     'Rice',     'Other Crops',     'Grass/Shrub',     'Woody Crops/Orchards',     'Barren',
         'Evergreen Forest',     'Deciduous Forest',     'Plantation Forest',     'Mangrove Forest',     'Aquaculture'],
        "colors": ['#000064',     '#FF0000',     '#0080FF',     '#FFC1BF',     '#E1E100',     '#80FF00',     '#BABABA',     '#006400',     '#ABDA9D',
         '#E563D0',     '#806400',     '#4D68FF']
        # "time": rasteryear,
        },
    ]
    for layer in wms_layers:
        if lulc_option in layer["name"]: 
            wms_layer = folium.raster_layers.WmsTileLayer(
                url=layer["url"],
                name=layer["name"],
                format="image/png",
                layers=layer["layers"],
                transparent=True,
                overlay=True,
                opacity=0.95,
                styles=layer["styles"],
                # COLORSCALERANGE='10, 30',
                # time=layer["time"],
            )
            wms_layer.add_to(m)
            
            labels=layer["labels"],
            colors=layer["colors"]
            m.add_legend(title='Legend', labels=labels[0], colors=colors)
    
    return m

@st.cache_data
def areas_per_boundary(provinces):
    dict_boundary_areas = {}
    for province in provinces:
        boundary_url = 'https://nens.lizard.net/api/v4/boundaries/?code={}'.format(province) 
        boundary_data = requests.get(url = boundary_url,headers = HEADERS).json()['results']
        boundary_properties = boundary_data['features'][0]["properties"]
        province_column_name = boundary_properties["name"]
        boundary_geom = boundary_data['features'][0]['geometry']
        
        try: 
            lon, lat = zip(*boundary_geom['coordinates'][0])
            pa = Proj("+proj=aea +lat_1=37.0 +lat_2=41.0 +lat_0=39.0 +lon_0=-106.55")
            x, y = pa(lon, lat)
            cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
            
            boundary_area = shape(cop).area / 1000000 # m2 to km2
            dict_boundary_areas[province_column_name] = boundary_area
        except:
            # voor 2 provincies kan geen area berekend worden
            if province == "VN.CM":
                dict_boundary_areas[province_column_name] = 5331
            elif province == "VN.KG":
                dict_boundary_areas[province_column_name] = 6299
            else: 
                dict_boundary_areas[province_column_name] = None
    return dict_boundary_areas

def percentages_to_areas(df_percentages):
    dict_boundary_areas = areas_per_boundary(provinces)

    for province in dict_boundary_areas.keys():
        df_percentages[province] = df_percentages[province] * dict_boundary_areas[province] / 100
    
    return df_percentages

@st.cache_data
def statistics_per_province(raster_url, raster_style, province, time = None): 
    classes_number = 80 # MONRE contains 79 classes, max number of classes
    boundary_url = 'https://nens.lizard.net/api/v4/boundaries/?code={}'.format(province) 
    boundary_data = requests.get(url = boundary_url,headers = HEADERS).json()['results']
    boundary_properties = boundary_data['features'][0]["properties"]
    boundary_id = boundary_data['features'][0]['id'] 
    if time: 
        timestep = jaxa_time_dictionary[str(time)]
        statistics_url = "{}counts/?geom={}&style={}&limit={}&time={}".format(raster_url, boundary_id, raster_style, classes_number, timestep)
    else:
        statistics_url = "{}counts/?geom={}&style={}&limit={}".format(raster_url, boundary_id, raster_style, classes_number)

    r = requests.get(url = statistics_url, headers = HEADERS)
    df_classes = pd.DataFrame(r.json()["results"])
    total_count = r.json()["total"]
    province_column_name = boundary_properties["name"]
    df_classes[province_column_name] = df_classes["count"]/total_count * 100
    df_classes.drop(columns=["label","count","color"], inplace=True)
    
    return df_classes

def all_provinces_one_year(lulc_option, year_option):
    if lulc_option == "MONRE":
        classes_monre_provinces = classes_monre_details.copy()

        for province in provinces: 
            df_classes = statistics_per_province(raster_url_monre, raster_style, province)
            classes_monre_provinces = classes_monre_provinces.join(df_classes.set_index('class'), on='class', rsuffix='check')
        classes_provinces = classes_monre_provinces.drop(['class','id', 'label'], axis=1).copy()
 
    elif lulc_option == "JAXA":
        if year_option == "2020": 
            classes_jaxa_provinces = classes_jaxa_details.copy()
            for province in provinces: 
                df_classes = statistics_per_province(raster_url_jaxa, raster_style_jaxa, province)
                classes_jaxa_provinces = classes_jaxa_provinces.join(df_classes.set_index('class'), on='class', rsuffix='check')
            
        else: 
            classes_jaxa_provinces = classes_jaxa_temp_details.copy()
            for province in provinces: 
                df_classes = statistics_per_province(raster_url_jaxa_temp, raster_style_jaxa_temp, province, time = year_option)
                classes_jaxa_provinces = classes_jaxa_provinces.join(df_classes.set_index('class'), on='class', rsuffix='check')
        classes_provinces = classes_jaxa_provinces.drop('class', axis=1).copy()
   
    classes_provinces = classes_provinces.fillna(0)
    classes_provinces = classes_provinces.round(2)
    return classes_provinces

def all_provinces_multiple_years(first_year_option, second_year_option, lulc_option):
    start_year = min(first_year_option, second_year_option)
    end_year = max(first_year_option, second_year_option)
    if lulc_option == "JAXA":
        classes_jaxa_provinces_start = classes_jaxa_temp_details.copy()
        classes_jaxa_provinces_end = classes_jaxa_temp_details.copy()
        for province in provinces: 
            df_classes_startyear = statistics_per_province(raster_url_jaxa_temp, raster_style_jaxa_temp, province, time = start_year) 
            df_classes_endyear = statistics_per_province(raster_url_jaxa_temp, raster_style_jaxa_temp, province, time = end_year)
            classes_jaxa_provinces_start = classes_jaxa_provinces_start.join(df_classes_startyear.set_index('class'), on='class', rsuffix='start')
            classes_jaxa_provinces_end = classes_jaxa_provinces_end.join(df_classes_endyear.set_index('class'), on='class', rsuffix='end')
        
        classes_jaxa_provinces_start = classes_jaxa_provinces_start.fillna(0)
        classes_jaxa_provinces_end = classes_jaxa_provinces_end.fillna(0)
        # classes_jaxa_provinces_start = classes_jaxa_provinces_start.convert_dtypes()
        # classes_jaxa_provinces_end = classes_jaxa_provinces_end.convert_dtypes()
        
        provinces_list = list(range(classes_jaxa_provinces_start.shape[1]))[2:]
        year_differences = classes_jaxa_provinces_end.iloc[:,provinces_list].subtract(classes_jaxa_provinces_start.iloc[:,provinces_list],axis="columns").copy()
        # st.write(classes_jaxa_provinces_end)
        # st.write(year_differences)
        year_differences = year_differences.div(classes_jaxa_provinces_start.iloc[:,provinces_list],axis="columns")#.mul(100)

        # year_differences.insert(loc=0, column='class', value=classes_jaxa_provinces_end["class"])
        year_differences.insert(loc=0, column='label', value=classes_jaxa_provinces_end["label"])
        year_differences = year_differences.round(2)
        year_differences.fillna(0, inplace=True)     

        # st.write(classes_jaxa_provinces_start)
        # st.write(classes_jaxa_provinces_end)
    else: 
        st.write("Calculation for multiple years for MONRE is not implemented yet")
        year_differences = None
    return year_differences


@st.cache_data 
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def reset_states():
    st.session_state["table_data"] = None
    st.session_state["show_map"] = True
    st.session_state["show_table"] = False
    st.session_state["year_differences_calc"] = False
    st.session_state["area_table"] = None
