import streamlit as st
import pydeck as pdk
import streamlit.components.v1 as components
# import base64
import plotly.express as px

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

def tipos_comida_chart(data, provincia_input):
        data_graph_cir=data[data["Provincia"]==provincia_input]["Tipo_comida"].value_counts().head(10)
        fig = px.pie(data_graph_cir, values='Tipo_comida', names=data_graph_cir.index, title=f'Restaurantes con 10 tipos de comida más populares en {provincia_input.capitalize()}',width=500, height=400)
        fig.update_layout(
            title={
                'y':0.95,  # Posición vertical del título
                'x':0.5,   # Posición horizontal del título (centrado)
                'xanchor': 'center',  # Anclaje horizontal del título
                'yanchor': 'top'      # Anclaje vertical del título
            }
        )
        st.plotly_chart(fig)