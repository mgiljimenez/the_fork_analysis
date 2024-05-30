import streamlit as st
from streamlit_option_menu import option_menu
# ###from streamlit_pandas_profiling import st_profile_report
import pandas as pd
#### import numpy as np
#### import pydeck as pdk
from webconfig.webconfig import chat_map,tipos_comida_chart, aed, filter_dataframe, corr_bar
import webbrowser
import joblib


data=pd.read_csv("datos/data_restaurantes_definitivo.csv", sep=";", encoding="utf-8")

st.set_page_config(
    page_title="Proyecto Restaurantes",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

image, col_menu = st.columns((0.2,0.8))
with image:
    st.image("webconfig/img/logo_the_fork_trans.png", width=200, clamp=False)
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

with col_menu:
    selected = option_menu(None, ["Inicio","Datos","AED", "Conclusión", 'Buscador','Modelo IA'], 
        icons=['house','database-down' ,'graph-up', "folder2-open", 'search','app-indicator'], 
        menu_icon="cast", default_index=0, orientation="horizontal")

###############
#PAGINA INICIO#
###############
if selected == "Inicio":
    # st.info("Algún mensaje de Bienvenida???")
    col1, col2=st.columns(2)
    with col1:
        container1 = st.container(border=True)
        container1.info("Nuestro Equipo")
        container1.image("webconfig/img/componentes_grupo.png", use_column_width=True, clamp=False)
        video_file = open('webconfig/img/video_presentacion.mp4', 'rb')
        video_bytes = video_file.read()

        container1.video(video_bytes)

    with col2:
        container2 = st.container(border=True)
        container2.info("Nuestro Objetivo")
        col21, col22=st.columns(2)
        with col21:
            container2.markdown("**¿Cuál es nuestro objetivo principal?**")
            container2.write("Comprobar si existe una relación entre al precio medio del restaurante y características como su localización, renta per cápita, tipo de comida etc.")
        # container2.divider()
        with col22:
            container2.markdown("**¿Cuáles son nuestros objetivos específicos?**")
            container2.write("- Conseguir Base de Datos de precio medio por restaurante con un mínimo de 5000 datos")
            container2.write("- Conseguir Base de Datos demográfica por provincias en España​")
            container2.write("- Analizar qué características influyen más en el precio medio de un restaurante.")
            container2.write("- Desarrollar un buscador de restaurantes dadas ciertas características del restaurante")
            container2.write("- Integrar todo el AED, Conclusiones y Soluciones tecnológicas en una única página web​")
    
    # container3 = st.container(border=True)
    st.info("ALCANCE")
    coltext, colimg = st.columns([0.7,0.3])
    with coltext:
        container4=st.container(border=True)
        col3, col4=container4.columns([0.3,0.7])
        with col3:
            st.subheader("Misión",anchor=False)
        with col4:
            st.write("- Analizar las características que influyen en el precio medio de un restaurante.")
            st.write("- Aportar una solución tecnológica a empresarios en el sector hostelería.")
        container5=st.container(border=True)
        col5, col6=container5.columns([0.3,0.7])
        with col5:
            st.subheader("Requisitos",anchor=False)
        with col6:
            st.write("- AED detallado (Statgraphics y Python), Control de versiones git, No Powerpoint")
        container6=st.container(border=True)
        col7, col8=container6.columns([0.3,0.7])
        with col7:
            st.subheader("Restricciones",anchor=False)
        with col8:
            st.write("- Entrega en junio")
            st.write("- Encontrar base de datos con mínimo 5000 restaurantes")
        container7=st.container(border=True)
        col9, col10=container7.columns([0.3,0.7])
        with col9:
            st.subheader("Supuesto inicial",anchor=False)
        with col10:
            st.write("- Información en The Fork: Actualizada y verídica (sin conflicto de intereses)")
        container8=st.container(border=True)
        col11, col12=container8.columns([0.3,0.7])
        with col11:
            st.subheader("Entregables",anchor=False)
        with col12:
            st.write("- Informe del alcance, cronograma, Informe adquisición y limpieza, Informe AED")
            st.write("- Web y Repositorio: webscraping, limpieza de datos, código de la web")
        container9=st.container(border=True)
        col13, col14=container9.columns([0.3,0.7])
        with col13:
            st.subheader("Límites",anchor=False)
        with col14:
            st.write("- No entramos en analizar platos ni menús")
            st.write("- La web sugerirá un precio medio para un restaurante, pero no el tipo de comida o localización del mismo")
        container10=st.container(border=True)
        col15, col16=container10.columns([0.3,0.7])
        with col15:
            st.subheader("Criterios de éxito",anchor=False)
        with col16:
            st.write("- El AED confirma si existe o no una relación con el precio medio del restaurante")
            st.write("- La solución tecnológica es útil para los empresarios en el sector hostelería")
    with colimg:
        st.image("webconfig/img/restaurant_vertical.jpg", use_column_width=True, clamp=False)
        st.link_button("ACCEDE A MÁS INFORMACIÓN DETALLADA ACERCA DEL ALCANCE", "https://github.com/mgiljimenez/the_fork_analysis", use_container_width=True)
    with st.expander("CRONOGRAMA DEL PROYECTO"):
        st.subheader("Cronograma",anchor=False)
        st.image("webconfig/img/cronograma.png", use_column_width=True, clamp=False)
        st.link_button("Accede a nuestro cronograma","https://github.com/mgiljimenez/the_fork_analysis", use_container_width=True)
##############
#PAGINA DATOS#
##############
elif selected == "Datos":
    col1, col2 = st.columns(2)
    with col1:
        container1 = st.container(border=True)
        container1.subheader("OBTENCIÓN DE DATOS",anchor=False)
        container1.image("webconfig/img/webscrapping.png", use_column_width=True, clamp=False)
        tabla_webscrapping=pd.DataFrame({"BBDD":["Restaurantes","Población por Provincia","Salarios medios anuales"],"Fuente":["Scrapping THE FORK","INE","INE"],"Comentarios":["Python, Selenium,BeautifulSoup, Request, JSON","Sin datos faltantes","Datos faltantes"]})
        container1.table(tabla_webscrapping)
        container3=st.container(border=True)
        col11, col12 = container3.columns(2)
        with col11:
            st.metric("Nº Restaurantes", len(data))
        with col12:
            st.metric("Nº variables", len(data.columns)-1) 
        container3.link_button("ACCEDE AL CÓDGIDO WEBSCRAPING E INFORME DE ADQUISICIÓN Y LIMPIEZA DE DATOS","https://github.com/mgiljimenez/the_fork_analysis", use_container_width=True)
        container3=st.container(border=True)
        container3.subheader("¿Cuáles son nuestras variables?",anchor=False)
        listar_variables=list(data.columns).copy()
        listar_variables.pop(0)
        variable_select=container3.selectbox("Variable", listar_variables)
        col_data1, col_data2=container3.columns(2)
        with col_data1:
            st.write(f"Cantidad de nulos: {data[variable_select].isnull().sum()}")
        with col_data2:
            st.write("Tipo de variable: " + type(data[variable_select][0]).__name__)
        container3.write(" ")
        container3.write(" ")

    with col2:
        container2 = st.container(border=True)
        container2.subheader("LIMPIEZA Y TRANSFORMACIÓN DE DATOS",anchor=False)
        container2.image("webconfig/img/restaurant_analysis.png", use_column_width=True,clamp=False)
        container2.info("_Datos faltantes_")
        container2.write("- **Rate_distinction:** Nulos con significado: No tratado")
        container2.write("- **Precio_medio:** Imputados a mano con búsqueda manual en Google")
        container2.write("- **Tipo_comida:** Imputados a mano con búsqueda manual en Google")
        container2.write("- **Salarios medios:** Faltantes de Navarra y País Vasco: Imputados con otra fuente")
        container2.write("- **Asalariados:** Eliminamos variable por no encontrar fuente fiable")
        container2.info("_Datos anómalos_")
        container2.write("- **Provincia:** Encontramos nombre de pueblos: Recodificación a provincia a mano")
        container2.write("- **Precio_medio:** Menores a 6€ : Eliminados")
        container2.info("_Recodificación de variables_")
        container2.write("- **Rate_distinction:** Recodificación de categórica a cuantitativa discreta")
        container2.write("- **Michelin:** Recodificación de string (True/False) a Booleano")
        container2.write("- **Comunidad autónoma:** Creación de variable a partir de provincia")

############
#PAGINA AED#
############
elif selected == "AED":
    datos_aed=aed(data)
    st.title("Análisis Univariante",anchor=False)
    container0=st.container(border=True)
    col0, col00=container0.columns(2)
    with col0:
        datos_aed.histograma_reservas_ultima_semana()
        with st.expander("Información detallada"):
            st.write("- Una de las variables **más dispersas**")
            st.write("- **Coeficiente de variación=** 229%")
            st.write("- **Rango=** 1133")
            st.write("- **Asimetría positiva**")
            st.write("- **Valores atípicos** = 1133")
            st.write("- **Curtosis** = 1014 (forma leptocúrtica)")

    with col00:
        datos_aed.pie_reservable()
        
    container_medio=st.container(border=True)
    col_medio1, col_medio2=container_medio.columns(2)
    with col_medio1:
        datos_aed.histograma_precio_medio()
        with st.expander("Información detallada"):
            st.write("- **Eliminamos** los restaurantes con precio medio < 6€")
            st.write("- Precio medio: Dispesión alta: **Rango 307 €**")
            st.write("- **Asimetria positiva**")
            st.write("- **Mediana** = 6€")
            st.write("- **Curtosis** = 632 (forma leptocúrtica)")
        

    with col_medio2:
        datos_aed.pie_michelin()

    container1=st.container(border=True)
    col1, col2= container1.columns(2)
    with col1:
        datos_aed.histograma_numero_fotos()
    with col2:
        datos_aed.histograma_metodos_pago()


    container2=st.container(border=True)
    col3, col4= container2.columns(2)
    with col3:
        datos_aed.histograma_calificacion_comida()
        with st.expander("Información detallada"):
            st.write("- Rango de valores **no extenso** (4-10)")
            st.write("- **Asimetría negativa**")
    with col4:
        datos_aed.scatter_poblacion_restaurantes_provincia()
        with st.expander("Información detallada"):
            st.write("- Este gráfico de puntos recoge los datos de la cantidad de restaurantes por provincias")
            st.write("- La línea de tendencia muestra que estas variables siguen una relación proporcional y totalmente lineal, es decir, cuanta más población hay en una provincia, más cantidad de restaurantes posee.")

    container3=st.container(border=True)
    col5, col6= container3.columns(2)
    with col5:
        datos_aed.bar_comunidad_autonoma_salario_medio()
    with col6:
        datos_aed.bar_comunidad_autonoma_precio_medio() 
    

    st.title("Análisis Multivariante",anchor=False)

    container_t_comida=st.container(border=True)
    container_t_comida.subheader("Tipo de comida según la comunidad",anchor=False)
    col_t1, col_t2=container_t_comida.columns([0.2,0.8])
    with col_t1:
        #Tabla con la relación de Lugar-Bandera
        data_banderas=pd.read_csv("webconfig/data/banderas.csv", sep=";") 
        st.dataframe(data_banderas,column_config={
            "BANDERA": st.column_config.ImageColumn(
                "BANDERA", help="Streamlit app preview screenshots"
            )}, hide_index=True, use_container_width=True)
    with col_t2:
        #Tabla con la relación Comunidad-Origen de la comida
        data_comida=pd.read_csv("webconfig/data/comida_consumida.csv", sep=";")
        st.dataframe(data_comida,column_config={
            "COMIDA MÁS CONSUMIDA 1": st.column_config.ImageColumn(
                "COMIDA MÁS CONSUMIDA 1", help="Streamlit app preview screenshots"
            ),"COMIDA MÁS CONSUMIDA 2": st.column_config.ImageColumn(
                "COMIDA MÁS CONSUMIDA 2", help="Streamlit app preview screenshots"
            ),"COMIDA MENOS CONSUMIDA 1": st.column_config.ImageColumn(
                "COMIDA MENOS CONSUMIDA 1", help="Streamlit app preview screenshots"
            ),"COMIDA MENOS CONSUMIDA 2": st.column_config.ImageColumn(
                "COMIDA MENOS CONSUMIDA 2", help="Streamlit app preview screenshots"
            )}, hide_index=True, use_container_width=True)
        st.image("webconfig/img/footer.png", use_column_width=True, clamp=False)
    
    col_comida1, col_comida2=st.columns(2)
    with col_comida1:
        datos_aed.bar_precio_medio_tipo_comida_descendente()
    with col_comida2:
        datos_aed.bar_precio_medio_tipo_comida_ascendente()
    data_pearson=pd.read_csv("webconfig/data/correlacion_pearson.csv", sep=";")
    def color_pearson(value):
        if float(value) >= 0.75:
            color = 'background-color: lightgreen'
        elif float(value) >= 0.43:
            color = 'background-color: yellow'
        else:
            color = 'background-color: #FFCCCC'
        return color
    #Tabla de la correlación de Pearson
    styled_df = data_pearson.style.applymap(color_pearson, subset=['Correlación de Pearson']).format({'Correlación de Pearson': '{:.2f}'})
    st.dataframe(styled_df, use_container_width=True)
    container_pearson=st.container(border=True)
    colfrase, colnum=container_pearson.columns([0.85,0.15])
    with colfrase:
        st.write("**¿Poca correlación entre salario medio por comunidad y precio medio del restaurante?**")
        st.write("Este dato nos sorprendió mucho, y al investigarlo a fondo, nos dimos cuenta de que se debía a que los salarios eran uno por cada provincia (49 únicos) y los precios medios eran uno por restaurante (7650 únicos), por lo que no eran comparables. Para comprobar si realmente existía relación, calculamos este comparando los salarios medios con la media de precios por cada provincia. Y entonces observamos una correlación de 0.43 (14 veces más!!) que se adecuaba más a lo que nos esperábamos.")
    with colnum:
        st.metric(label="Correlación", value=round(datos_aed.correlacion_precio_medio_salario_medio(),3), delta="1400%")

    st.link_button("Accede a más información detallada del AED","https://github.com/mgiljimenez/the_fork_analysis", use_container_width=True)


###################
#PAGINA CONCLUSIÓN#
###################
elif selected == "Conclusión":
    st.image("webconfig/img/conclusion.png", use_column_width=True)


#################
#PAGINA BUSCADOR#
#################
elif selected == "Buscador":

    container1 = st.container(border=True)
    #Análisis de la competencia de una sola provincia
    container1.subheader("Analice a toda la competencia de su provincia",anchor=False)
    col1, col2, col3 = container1.columns(3)
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
        try: 
            chat_map(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input][["Longitude","Latitude"]], data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Longitude"].median(), data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Latitude"].median())
        except:
            st.error("No existen restaurantes para estos filtros")

    with col2:
        st.warning("**DATOS DE INTERÉS**")
        col2_1, col2_2= st.columns(2)
        with col2_1:
            st.warning("**Nº Restaurantes**")
            st.warning("**Estrellas Michelin**")
            st.warning("**Precio medio**")
            st.warning("**Precio mediano**")
            st.warning("**Desviación precio**")
            st.warning("**Sistema reserva online**")
        with col2_2:
            cantidad_restaurantes_data=str(len(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]))
            st.warning(cantidad_restaurantes_data)
            try:
                st.warning(len(data[(data_filtro_michelin["Provincia"]==provincia_input) & (data_filtro_michelin["Michelin"]==True)]))
            except:
                st.warning("Filtrado")
            st.warning(str(round(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Average_Price"].mean(),2)) + "€")
            st.warning(str(round(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Average_Price"].median(),2)) + "€")
            st.warning(str(round(data_filtro_michelin[data_filtro_michelin["Provincia"]==provincia_input]["Average_Price"].std(),2)) + "€")
            st.warning(str(len(data_filtro_michelin[(data_filtro_michelin["Provincia"]==provincia_input) & (data_filtro_michelin["Bookable"]==True)]))+"/"+cantidad_restaurantes_data)
    with col3:
        st.warning("**TIPO DE COMIDA**")
        tipos_comida_chart(data_filtro_michelin, provincia_input)




    #Análisis de la competencia filtrando por sus datos
    st.subheader("Analice a toda la competencia de forma personalizada",anchor=False)
    data_filtered_personalizado=filter_dataframe(data)

    container2 = st.container(border=True)
    col4, col5, col6 = container2.columns(3)
    with col4:
        try: 
            chat_map(data_filtered_personalizado[["Longitude","Latitude"]], data_filtered_personalizado["Longitude"].median(), data_filtered_personalizado["Latitude"].median())
        except:
            st.error("No existen restaurantes para estos filtros")

    with col5:
        st.warning("**DATOS DE INTERÉS**")
        col3_1, col3_2= st.columns(2)
        with col3_1:
            st.warning("**Nº Restaurantes**")
            st.warning("**Estrellas Michelin**")
            st.warning("**Precio medio**")
            st.warning("**Precio mediano**")
            st.warning("**Desviación precio**")
            st.warning("**Sistema reserva online**")
        with col3_2:
            cantidad_restaurantes_data=str(len(data_filtered_personalizado))
            st.warning(cantidad_restaurantes_data)
            st.warning(len(data_filtered_personalizado[data_filtered_personalizado["Michelin"]==True]))
            st.warning(str(round(data_filtered_personalizado["Average_Price"].mean(),2)) + "€")
            st.warning(str(round(data_filtered_personalizado["Average_Price"].median(),2)) + "€")
            st.warning(str(round(data_filtered_personalizado["Average_Price"].std(),2)) + "€")
            st.warning(str(len(data_filtered_personalizado[data_filtro_michelin["Bookable"]==True]))+"/"+cantidad_restaurantes_data)
    with col6:
        st.warning("**TIPO DE COMIDA**")
        tipos_comida_chart(data_filtered_personalizado, "GENERAL")
    with container2.expander("Mostrar correlación de datos actuales"):
        corr_bar(data_filtered_personalizado)
    with st.expander("Mostrar datos actuales"):
        st.dataframe(data_filtered_personalizado.drop(columns=["Unnamed: 0"]))

##################
#PAGINA MODELO IA#
##################
elif selected == "Modelo IA":
    st.error("ESTA PÁGINA ESTÁ TODAVÍA EN DESARROLLO")
    with st.form("form_prediccion"):
        st.info("¿Cuánto debería pagar un cliente de media en su restaurante?")
        col1, col2, col3 = st.columns(3)
        with col1:
            provincia_in=st.selectbox("Provincia", sorted(['madrid', 'barcelona', 'valencia', 'sevilla', 'malaga', 'alicante',
                            'islas baleares']))
            tipo_comida_in=st.selectbox("Tipo de comida", sorted(['Colombian', 'Fusion', 'Asian', 'Mexican', 'Japanese',
                        'Mediterranean', 'Indian', 'American', 'Moroccan', 'Spanish',
                        'International', 'French', 'Brazilian', 'Steakhouse', 'Peruvian',
                        'Vegetarian', 'Italian', 'Traditional cuisine', 'From Canarias',
                        'From galicia', 'Pizzeria', 'Armenian', 'Middle Eastern', 'German',
                        'Argentinian', 'Crêperie', 'Meat Cuisine', 'Basque', 'Hawaiian',
                        'Thai', 'Venezuelan', 'From Madrid', 'Lebanese', 'Arrocería',
                        'Chinese', 'South American', 'Afghan', 'Ecuadorian', 'Cuban',
                        'Cantonese', 'From Asturias', 'Iranian', 'Grilled', 'Vietnamese',
                        'Caribbean', 'Persian', 'andalucian', 'Nepalese', 'Seafood',
                        'Ethiopian', 'European', 'Eastern Europe', 'Romanian', 'Del Norte',
                        'Turkish', 'From Valence', 'Greek', 'Abruzzese', 'Korean',
                        'From Castille', 'African', 'Varied', 'Indonesian', 'Traditional',
                        'International food', 'Portuguese', 'Catalan', 'Vegan cuisine',
                        'Picadas', 'Local', 'Tibetan', 'Afternoon Tea', 'Franco-Belgian',
                        'Dutch', 'Syrian', 'From the Pyrenees', 'Siciliano', 'British',
                        'Swiss', 'Pakistani', 'Alsatian', 'Chilean', 'Belgian',
                        'Uruguayan', 'Emiliano', 'Traditionala', 'From Murcia', 'Regional']))
            michelin_in=st.radio("Es Michelin", options=[True, False])
            sistema_reserva_in=st.radio("Sistema de reserva online", options=[True, False])
            afiliado_in=st.radio("Afiliado a The Fork", options=[True, False])
            
        with col2:
            reservas_semana_in=st.number_input("Reservas última semana", min_value=0)
            calidad_comida_in=st.slider("Calidad de comida", min_value=0.0, max_value=10.0)
            calidad_servicio_in=st.slider("Calidad del servicio", min_value=0.0, max_value=10.0)
            calidad_ambiente_in=st.slider("Calidad del ambiente", min_value=0.0, max_value=10.0)
            distincion_in=st.selectbox("Restaurante con distinción", [None,1.0,2.0,3.0])

        with col3:
            num_premios_in=st.number_input("Número de premios", min_value=0)
            num_comentarios_in=st.number_input("Número de comentarios", min_value=0)
            num_resena_in=st.number_input("Número de reseñas", min_value=0)
            num_foto_in=st.number_input("Número de fotos online", min_value=0)
            num_metodo_pago_in=st.number_input("Cantidad métodos de pago", min_value=0)


        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit", use_container_width=True)
        if submitted:
            dic_sal_pob={"madrid":[26721,6751251],"barcelona":[24243,5714730],"valencia":[20069,2589312],"sevilla":[17710,1947852],"malaga":[17390,1695651],"alicante":[17139,1881762],"islas baleares":[19834,1173008]}
            data_to_predict={"Bookable": [sistema_reserva_in],"Cantidad_metodos_pago":[num_metodo_pago_in],
            "Reservas_last_week":[reservas_semana_in],"Numero_fotos":[num_foto_in],"Is_Affiliated":[afiliado_in],
            "Numero_awards":[num_premios_in],"Review_count":[float(num_comentarios_in)],"Rating_count":[float(num_resena_in)],
            "Food_rating":[calidad_comida_in],"Service_rating":[calidad_servicio_in],"Ambience_rating":[calidad_ambiente_in],
            "Provincia":[provincia_in],"Poblacion": [dic_sal_pob[provincia_in][1]],"Salario Medio Anual": [dic_sal_pob[provincia_in][0]],
            "Michelin numérico":[michelin_in],"Rate_Distinction_numérico":[distincion_in],"Tipo_comida":[tipo_comida_in]}

            data_to_predict_df = pd.DataFrame(data_to_predict)
            model=joblib.load("models/model_cities/random_forest_model.pkl")
            result=model.predict(data_to_predict_df)
            st.info(f"Precio medio recomendado: {round(result[0],2)}€")
