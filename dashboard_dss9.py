# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:33:05 2023

@author: pvantets
"""

import streamlit as st

# from streamlit_folium import st_folium

# import geopandas as gpd
# import plotly.express as px
# import plotly.graph_objects as go
# import numpy as np
import functions.lizard_functions as liz

# from datetime import datetime

st.set_page_config(
    layout="wide",
    page_title="Home",
)


#%% Pagina lay-out
page_start = """
    <style>
        .css-18ni7ap {
                position: fixed;
                height:1rem;
            }
        .css-z5fcl4 {
                margin-top:-8rem;
                padding-bottom: 0rem;
                padding-left: 4rem;
                padding-right: 3rem;
            }
        .css-k1ih3n{
                margin-top: -8rem;
                padding-bottom: 0rem;
                padding-left: 4rem;
                padding-right: 3rem;
        }
        .css-1d391kg {
                padding-top: 1.5rem;
                padding-right: 1rem;
                padding-bottom: 1.5rem;
                padding-left: 1rem;
        }
        .css-kjtpls{
            background:#176d8a;
        }
        .css-1b0udgb{
            color: rgb(49, 51, 63);
        }
        .css-1offfwp p {
            font-weight: bold;
        }
        .css-ocqkz7.e1tzin5v4{
            margin-top:0rem;
        }
        .css-1offfwp p{
            font-weight: normal;
        }
    </style>
    """
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

hide_img_fs = """
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
"""


# Hide default streamlit menu
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Remove whitespace from the top of the page and sidebar
# st.markdown(
#     page_start,
#     unsafe_allow_html=True,
# )

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)

st.markdown(
    hide_img_fs,
    unsafe_allow_html=True,
)

if "show_map" not in st.session_state:
    st.session_state["show_map"] = True
if "show_table" not in st.session_state:
    st.session_state["show_table"] = False
if "table_data" not in st.session_state:
    st.session_state["table_data"] = None
if "year_differences_calc" not in st.session_state:
    st.session_state["year_differences_calc"] = False
if "area_table" not in st.session_state:
    st.session_state["area_table"] = None


#%% Start dashboard
# =============================================================================
# Title of dashboard
# =============================================================================
st.markdown("")
# col1, col2, col3 = st.columns([])
dashboardname = (
    "<h1 style='text-align: center;'>DSS-9 Land use and land use change</h1>"
)
st.markdown(dashboardname, unsafe_allow_html=True)

# =============================================================================
# Body of dashboard
# =============================================================================

col1, col2, col3 = st.columns([0.2, 0.7, 0.1])
with col1:

    lulc_option = st.selectbox(
        "Select a land use land cover dataset",
        ("MONRE", "JAXA"),
        index=None,
        placeholder="Select an option",
        on_change=liz.reset_states,
    )

    # st.write('You selected:', lulc_option)

    aggregate_option = st.selectbox(
        "Select a statistics option",
        (
            "Statistics for all provinces for one year",
            "Statistics for multiple years for one province",
            "Statistics for changes between years for one province",
        ),
        index=None,
        placeholder="Select an option",
        on_change=liz.reset_states,
    )

    # st.write('You selected:', aggregate_option)

    if aggregate_option == "Statistics for all provinces for one year":
        year_option = st.selectbox(
            "Select a year",
            list(reversed(range(1990, 2021))),
            # ("2020",
            #  "2000",
            #  "1990",
            #  "1995"),
            index=None,
            placeholder="Select an option",
        )

    if aggregate_option == "Statistics for all provinces for one year":
        if year_option != 2020 and lulc_option == "MONRE":
            st.write("The MONRE dataset is only available for 2020.")
        elif lulc_option is not None and year_option is not None:
            calculation_button_one_year = st.button(
                "Calculate", type="primary"
            )

            if calculation_button_one_year:
                # st.write('Calculating...')
                st.session_state["table_data"] = liz.all_provinces_one_year(
                    lulc_option, year_option
                )
                st.session_state["show_map"] = False
                st.session_state["show_table"] = True

            if st.session_state["table_data"] is not None:
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    graph_button = st.button("Show table", type="secondary")
                    if graph_button:
                        st.session_state["show_table"] = True
                        st.session_state["show_map"] = False
                with subcol2:
                    map_button = st.button("Show map", type="secondary")
                    if map_button:
                        st.session_state["show_table"] = False
                        st.session_state["show_map"] = True

    if aggregate_option == "Statistics for multiple years for one province":
        if lulc_option is not None:
            st.write("This option is not configured yet")

    if (
        aggregate_option
        == "Statistics for changes between years for one province"
    ):
        if lulc_option == "MONRE":
            st.write(
                "The MONRE dataset is only available for 2020, no comparison possible"
            )

        elif lulc_option is not None:
            # st.write("This option is not configured yet")
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                first_year_option = st.selectbox(
                    "Select a first year",
                    list(reversed(range(1990, 2021))),
                    index=None,
                    placeholder="Select an option",
                    on_change=liz.reset_states,
                )
            with subcol2:
                second_year_option = st.selectbox(
                    "Select second year",
                    list(reversed(range(1990, 2021))),
                    index=None,
                    placeholder="Select an option",
                    on_change=liz.reset_states,
                )
            if first_year_option == second_year_option:
                st.write("Please select two different years")
            elif (
                first_year_option is not None
                and second_year_option is not None
            ):
                calculation_button_year_differences = st.button(
                    "Calculate", type="primary"
                )
                if calculation_button_year_differences:
                    st.session_state["year_differences_calc"] = True
                    year_differences = liz.all_provinces_multiple_years(
                        first_year_option, second_year_option, lulc_option
                    )
                    st.session_state["table_data"] = year_differences

with col2:
    if (
        lulc_option is not None
        and aggregate_option == "Statistics for all provinces for one year"
    ):
        if year_option:
            if st.session_state["show_map"]:
                m = liz.create_map(lulc_option)
                m.to_streamlit()
            elif st.session_state["area_table"] is not None:
                if len(st.session_state["table_data"]) < 14:
                    table_height = (
                        35 * len(st.session_state["table_data"]) + 38
                    )
                else:
                    table_height = 35 * 14 + 55
                provinces_list = list(st.session_state["table_data"].columns)[
                    1:
                ]
                st.dataframe(
                    st.session_state["table_data"].style.format(
                        "{:.1f}", subset=provinces_list
                    ),
                    # column_config = {col: st.column_config.NumberColumn(format="%.1f %") for col in provinces_list},
                    height=table_height,
                    hide_index=True,
                )
            elif st.session_state["show_table"]:
                if len(st.session_state["table_data"]) < 14:
                    table_height = (
                        35 * len(st.session_state["table_data"]) + 38
                    )
                else:
                    table_height = 35 * 14 + 55
                provinces_list = list(st.session_state["table_data"].columns)[
                    1:
                ]
                st.dataframe(
                    st.session_state["table_data"],
                    column_config={
                        col: st.column_config.NumberColumn(format="%.2f %%")
                        for col in provinces_list
                    },
                    height=table_height,
                    hide_index=True,
                )

    if (
        lulc_option is not None
        and aggregate_option
        == "Statistics for changes between years for one province"
    ):

        def color_negative_red(val):
            """
            Takes a scalar and returns a string with
            the css property `'color: red'` for negative
            strings, green otherwise.
            """
            if val < 0:
                color = "red"
            elif val > 0:
                color = "green"
            else:
                color = "grey"
            # color = 'red' if val < 0 else 'green'
            return "color: %s" % color

        if not lulc_option == "MONRE":
            if (
                first_year_option is not None
                and second_year_option is not None
            ):
                if st.session_state["year_differences_calc"]:
                    year_differences = st.session_state["table_data"]
                    if len(year_differences) < 14:
                        table_height = 35 * len(year_differences) + 38
                    else:
                        table_height = 35 * 14 + 55
                    provinces_list = list(year_differences.columns)[1:]

                    st.dataframe(
                        year_differences.style.applymap(
                            color_negative_red, subset=provinces_list
                        ).format(  # .set_precision(0)\
                            "{:.0%}", subset=provinces_list
                        ),
                        height=table_height,
                        hide_index=True,
                    )

with col3:
    if st.session_state["table_data"] is not None:
        if st.session_state["show_table"]:
            area_button = st.button("Table in km2", type="secondary")
            if area_button:
                st.session_state["area_table"] = liz.percentages_to_areas(
                    st.session_state["table_data"]
                )
                st.rerun()
        download_data = liz.convert_df(st.session_state["table_data"])
        st.download_button(
            "Download csv",
            download_data,
            file_name="MKDC_statistics.csv",
            mime="text/csv",
        )
