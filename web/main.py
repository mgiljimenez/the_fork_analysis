import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pydeck as pdk
from webconfig import chat_map
import webbrowser

data=pd.read_csv("./data_restaurantes_final.csv", sep=";", encoding="utf-8")



st.set_page_config(
    page_title="Proyecto Restaurantes",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

image, col_menu = st.columns((0.15,0.85))
with image:
    st.image("img/logo_the_fork_trans.png", width=200)

with col_menu:
    selected = option_menu(None, ["Inicio","Scraping","AED", "Conclusiones", 'Buscador','Modelo IA'], 
        icons=['house','database-down' ,'graph-up', "folder2-open", 'search','app-indicator'], 
        menu_icon="cast", default_index=0, orientation="horizontal")


if selected == "Inicio":
    st.info("Bienvenido al proyecto de Restaurantes")
    st.error("Hola")
    pass

elif selected == "Scraping":
    
    col1, col2 = st.columns(2)
    with col1:
        container1 = st.container()
        container1.info("OBTENCIÓN DE DATOS")
        if st.button("Ver repositorio en GitHub"):
            webbrowser.open_new_tab("www.sincronity.com")

        st.markdown("- **Web scrapping** de la página de The Fork")
        st.markdown("- Tecnologías empleadas:")
        st.markdown("- Python, BeautifulSoup, Request, JSON")

        container1.image("img/webscrapping.png", use_column_width=True)


    with col2:
        container2 = st.container()
        container2.info("PROCEDIMIENTO DE LIMPIEZA Y TRANSFORMACIÓN DE DATOS")
        container2.image("img/webscrapping.png", use_column_width=True)


elif selected == "AED":
    pass



elif selected == "Conclusiones":
    pass

elif selected == "Buscador":
    #Análisis de la competencia de una sola provincia
    st.info("ANALIZE A TODA LA COMPETENCIA DE SU PROVINCIA")
    col1, col2, col3 = st.columns(3)
    with col1:
        provincia_input= st.selectbox("Seleccione su provincia", sorted(data["Provincia"].unique()), index=6)
        chat_map(data[data["Provincia"]==provincia_input][["Longitude","Latitude"]], data[data["Provincia"]==provincia_input]["Longitude"].median(), data[data["Provincia"]==provincia_input]["Latitude"].median())


    with col2:
        st.warning("Información adicional")
        col2_1, col2_2= st.columns(2)
        with col2_1:
            st.warning("Cantidad de Restaurantes")
            st.warning("Estrellas Michelin")
            st.warning("Precio medio")
            st.warning("Precio mediano")
            st.warning("Bookable")
        with col2_2:
            cantidad_restaurantes_data=str(len(data[data["Provincia"]==provincia_input]))
            st.warning(cantidad_restaurantes_data)
            st.warning(len(data[(data["Provincia"]==provincia_input) & (data["Michelin"]==True)]))
            st.warning(str(round(data[data["Provincia"]==provincia_input]["Average_Price"].mean(),2)) + "€")
            st.warning(str(round(data[data["Provincia"]==provincia_input]["Average_Price"].median(),2)) + "€")
            st.warning(str(len(data[(data["Provincia"]==provincia_input) & (data["Bookable"]==True)]))+"/"+cantidad_restaurantes_data)
    with col3:
        st.warning("Gráficas de interés")
        

        


    #Análisis de la competencia filtrando por sus datos
    st.info("ANALIZE A TODA LA COMPETENCIA DE FORMA PERSONALIZADA")
    with st.form("my_form"):
        st.info("Analize su competencia mediante este buscador")
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")
        provincia_input= st.selectbox("Provincia", ("a","b"))
        estrella_mich_input=st.radio("¿Es una estrella Michelin?", options=("True","False"))
        tipo_comida_input=st.selectbox("Tipo de Restaurante", ("Italiano","Mexicano"))

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)

    st.info("¿QUIERE MONTAR UN RESTAURANTE PERO NO SABE DÓNDE?")
    with st.form("form_encontrar_ciudad"):  
        tipo_comida_input=st.selectbox("Tipo de Comida", sorted(data["Tipo_comida"].unique()))
        precio_medio_input=st.slider("Precio medio", min_value=0, max_value=500, value=50, step=1)
        michelin_input=st.radio("¿Va a ser tu restaurante un potencial Estrella Michelin?", options=("True","False"))
        bookable_input=st.radio("¿Se podrá reservar una mesa online en su restaurante?", options=("True","False"))

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)

elif selected == "Modelo IA":
    with st.form("form_prediccion"):
        st.info("¿Cuánto debería pagar un cliente de media en su restaurante?")
        provincia_input= st.selectbox("Seleccione su provincia", sorted(data["Provincia"].unique()), index=6)
        st.number_input("nws")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", provincia_input, "checkbox")