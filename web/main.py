import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pydeck as pdk
from webconfig import chat_map,tipos_comida_chart
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
    selected = option_menu(None, ["Inicio","Datos","AED", "Conclusiones", 'Buscador','Modelo IA'], 
        icons=['house','database-down' ,'graph-up', "folder2-open", 'search','app-indicator'], 
        menu_icon="cast", default_index=0, orientation="horizontal")

###############
#PAGINA INICIO#
###############
if selected == "Inicio":
    st.info("Algún mensaje de Bienvenida???")
    col1, col2=st.columns(2)
    with col1:
        st.info("Nuestro Equipo")
        st.image("img/componentes_grupo.png", use_column_width=True)

    
    with col2:
        st.info("Nuestro Objetivo")
        st.markdown("**¿Cúal es nuestro objetivo principal?**")
        st.write("- Comprobar si existe una relación entre al precio medio del restaurante y características como su localización, renta per cápita, tipo de comida etc.​")
        st.markdown("**¿Cuáles son nuestros objetivos específicos?**")
        st.write("- Objetivo 1")
        st.write("- Objetivo 2")
        st.write("- Objetivo 3")
        st.write("- Objetivo 4")
        st.write("- Objetivo 5")
    
    st.info("Alcance")
    if st.button("Informe detallado del alcance", use_container_width=True):
                webbrowser.open_new_tab("www.sincronity.com")
    st.info("Cronograma")
    st.image("img/cronograma.png", use_column_width=True)
    if st.button("Accede a nuestro cronograma", use_container_width=True):
                webbrowser.open_new_tab("www.sincronity.com")
elif selected == "Datos":
    
    col1, col2 = st.columns(2)
    with col1:
        container1 = st.container()
        container1.subheader("OBTENCIÓN DE DATOS")
        container1.image("img/webscrapping.png", use_column_width=True)
        tabla_webscrapping=pd.DataFrame({"BBDD":["Restaurantes","Población por Provincia","Salarios medios anuales"],"Obtención":["Scrapping THE FORK","INE","INE"],"Comentarios":["Python, Selenium,BeautifulSoup, Request, JSON","Sin datos faltantes","Datos faltantes"]})
        container1.table(tabla_webscrapping)

        col11, col12 = container1.columns(2)
        with col11:
            st.metric("Nº Restaurantes", "7562")
            if st.button("CÓDIGO DEL WEBSCRAPING Y DATOS", use_container_width=True):
                webbrowser.open_new_tab("www.sincronity.com")
        with col12:
            st.metric("Nº variables", "27") 
            if st.button("INFORME ADQUISICIÓN Y LIMPIEZA DE DATOS", use_container_width=True):
                webbrowser.open_new_tab("www.sincronity.com")

    with col2:
        container2 = st.container()
        container2.subheader("LIMPIEZA Y TRANSFORMACIÓN DE DATOS")
        container2.image("img/restaurant_analysis.png", use_column_width=True)
        container2.info("_Datos faltantes_")
        container2.info("_Datos anómalos_")
        container2.info("_Algún tipo de dato más?_")


elif selected == "AED":
    st.title("Análisis Univariante")

    st.title("Análisis Multivariante")



elif selected == "Conclusiones":
    st.title("Recordamos los objetivos y respondemos a cada uno de ellos")

elif selected == "Buscador":
    st.divider()
    #Análisis de la competencia de una sola provincia
    st.subheader("Analice a toda la competencia de su provincia")
    # st.info("ANALIZE A TODA LA COMPETENCIA DE SU PROVINCIA")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("Opciones de Filtro"):
            provincia_input= st.selectbox("Seleccione su provincia", sorted(data["Provincia"].unique()), index=6)
            filtro_michelin=st.radio("Restaurantes a analizar:", options=("Todos","Solo Estrellas Michelin","Descartar Estrellas Michelin"))
        if filtro_michelin=="Todos":
             data_filtro_michelin=data
        elif filtro_michelin=="Solo Estrellas Michelin":
            data_filtro_michelin=data[data["Michelin"]==True]
        elif filtro_michelin=="Descartar Estrellas Michelin":
            data_filtro_michelin=data[data["Michelin"]==False]
        if True:
            st.error("AQUI HAY UN ERROR MIRAR GUADALARAJA CON ESTRELLAS MICHELIN")

            print(chat_map(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input][["Longitude","Latitude"]], data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Longitude"].median(), data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Latitude"].median()))
        else:
            st.error("No existen restaurantes para estos filtros")


    with col2:
        st.warning("**DATOS DE INTERÉS**")
        col2_1, col2_2= st.columns(2)
        with col2_1:
            st.warning("**Cantidad de Restaurantes**")
            st.warning("**Estrellas Michelin**")
            st.warning("**Precio medio**")
            st.warning("**Precio mediano**")
            st.warning("**Desviación estándar precio**")
            st.warning("**Sistema reserva online**")
        with col2_2:
            cantidad_restaurantes_data=str(len(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]))
            st.warning(cantidad_restaurantes_data)
            try:
                st.warning(len(data[(data_filtro_michelin["Provincia"]==provincia_input) & (data_filtro_michelin["Michelin"]==True)]))
            except:
                st.warning("0")
            st.warning(str(round(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Average_Price"].mean(),2)) + "€")
            st.warning(str(round(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Average_Price"].median(),2)) + "€")
            st.warning(str(round(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Average_Price"].std(),2)) + "€")
            st.warning(str(len(data_filtro_michelin[(data_filtro_michelin["Provincia"]==provincia_input) & (data_filtro_michelin["Bookable"]==True)]))+"/"+cantidad_restaurantes_data)
    with col3:
        st.warning("**TIPO DE COMIDA**")
        tipos_comida_chart(data_filtro_michelin, provincia_input)
        
                

    st.divider()


    #Análisis de la competencia filtrando por sus datos
    st.subheader("Analice a toda la competencia de forma personalizada")
    # st.info("ANALIZE A TODA LA COMPETENCIA DE FORMA PERSONALIZADA")
    with st.form("my_form"):
        st.info("Analize su competencia mediante este buscador")
        slider_val = st.slider("Form slider", 0, 100, 50, 1)
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

st.image("img/footer.png", use_column_width=True)