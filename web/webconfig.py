import streamlit as st
import pydeck as pdk
import streamlit.components.v1 as components
import base64

def chat_map(chart_data, long_inicial,lat_inicial):

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=lat_inicial,
            longitude=long_inicial,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[Longitude, Latitude]',
            radius=50,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=50,
            ),
        ],
    ))

