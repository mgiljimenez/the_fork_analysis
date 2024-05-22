import streamlit as st
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype)
import numpy as np
from sklearn.linear_model import LinearRegression


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
    # Filtrar los datos según la provincia y contar los tipos de comida
    data_graph_cir = data[data["Provincia"] == provincia_input].value_counts('Tipo_comida').head(5).reset_index(name='count')
    if provincia_input == 'GENERAL':
        fig = px.pie(data.value_counts('Tipo_comida').head(5).reset_index(name='count'), values='count', names='Tipo_comida', 
                 title='5 tipos de comida más populares',
                 width=500, height=400)
    # Crear el gráfico de pastel
    else:
        fig = px.pie(data_graph_cir, values='count', names='Tipo_comida', 
                 title=f'5 tipos de comida más populares en {provincia_input.capitalize()}',
                 width=500, height=400)
    
    # Actualizar el layout del gráfico
    fig.update_layout(
        title={
            'y': 0.95,  # Posición vertical del título
            'x': 0.5,   # Posición horizontal del título (centrado)
            'xanchor': 'center',  # Anclaje horizontal del título
            'yanchor': 'top'      # Anclaje vertical del título
        },
        legend={
            'orientation': 'h',  # Hacer la leyenda horizontal
            'y': -0.2,  # Posición vertical de la leyenda
            'x': 0.5,   # Posición horizontal de la leyenda (centrado)
            'xanchor': 'center',  # Anclaje horizontal de la leyenda
            'yanchor': 'top'      # Anclaje vertical de la leyenda
        },
        width=400,  # Ancho del gráfico
    )
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

colores_comunidades = {
    'Andalucia': 'blue',
    'Aragon': 'orange',
    'Asturias': 'green',
    'Baleares': 'red',
    'Canarias': 'purple',
    'Cantabria': 'brown',
    'Castilla La Mancha': 'pink',
    'Castilla y Leon': 'gray',
    'Cataluña': 'olive',
    'Ceuta y Melilla': 'cyan',
    'Comunidad Valenciana': 'lightcoral',
    'Extremadura': 'gold',
    'Galicia': 'lightseagreen',
    'La Rioja': 'lightpink',
    'Madrid': 'lightskyblue',
    'Murcia': 'mediumorchid',
    'Navarra': 'mediumspringgreen',
    'Pais Vasco': 'orangered',
    'Region de Murcia': 'royalblue',
    'Spain': 'salmon'}
class aed:
    def __init__(self, data):
         self.data=data
    def histograma_reservas_ultima_semana(self): 
        # Crear el histograma con Plotly Express
        fig = px.histogram(self.data, 
                        x='Reservas_last_week', 
                        nbins=150,  # Establecer el número de bines a 50
                        title='Histograma de Frecuencias de Reservas de la Última Semana',
                        labels={'Reservas_last_week': 'Reservas de la Última Semana'},
                        opacity=0.7, # Hacer el histograma un poco transparente
                        color_discrete_sequence=['orange'], # Cambiar el color de las barras
                        template='plotly_white',
                        width=500) # Cambiar el tema del gráfico

        # Ajustar los límites de los ejes x e y
        fig.update_xaxes(range=[0, 300]) 
        fig.update_yaxes(title='Frecuencia')

        # Calcular la mediana y la media
        median_reservas = self.data['Reservas_last_week'].median()
        mean_reservas = self.data['Reservas_last_week'].mean()

        # Agregar una línea vertical para la media
        #fig.add_vline(x=mean_reservas, line_dash="dash", line_color="red", annotation_text=f'Media={mean_reservas:.2f}')

        # Agregar una línea vertical para la mediana
        fig.add_vline(x=median_reservas, line_dash="dash", line_color="green", annotation_text=f'Mediana={median_reservas:.2f}')

        # Mostrar el histograma
        st.plotly_chart(fig)
    def histograma_precio_medio(self): 
        fig = px.histogram(self.data, 
                        x='Average_Price', 
                        nbins=50, 
                        title='Histograma de Frecuencias del Precio Promedio',
                        labels={'Average_Price': 'Precio Promedio'},
                        opacity=0.7, # Hacer el histograma un poco transparente
                        color_discrete_sequence=['blue'], # Cambiar el color de las barras
                        template='plotly_white',
                        width=500) # Cambiar el tema del gráfico

        # Ajustar los límites de los ejes x e y
        fig.update_xaxes(range=[0, self.data['Average_Price'].max()*1.1]) 
        fig.update_yaxes(title='Frecuencia')

        # Calcular la mediana
        median_price = self.data['Average_Price'].median()

        # Agregar una línea vertical para la media
        mean_price = self.data['Average_Price'].mean()
        #fig.add_vline(x=mean_price, line_dash="dash", line_color="red", annotation_text=f'Media={mean_price:.2f}')

        # Agregar una línea vertical para la mediana
        fig.add_vline(x=median_price, line_dash="dash", line_color="green", annotation_text=f'Mediana={median_price:.2f}')

        # Mostrar el histograma
        st.plotly_chart(fig)
    def histograma_calificacion_comida(self):
        # Calcular la mediana de 'Food_rating'
        median_food_rating = self.data['Food_rating'].median()

        # Crear el histograma con Plotly Express
        fig = px.histogram(self.data, 
                        x='Food_rating', 
                        nbins=50, 
                        title='Histograma de Frecuencias de Calificación de Comida',
                        labels={'Food_rating': 'Calificación de Comida'},
                        opacity=0.7, # Hacer el histograma un poco transparente
                        color_discrete_sequence=['purple'], # Cambiar el color de las barras
                        template='plotly_white',
                        width=500) # Cambiar el tema del gráfico

        # Ajustar los límites de los ejes x e y
        fig.update_xaxes(range=[0, self.data['Food_rating'].max()*1.1]) 
        fig.update_yaxes(title='Frecuencia')

        # Agregar una línea vertical para la mediana
        fig.add_vline(x=median_food_rating, line_dash="dash", line_color="green", annotation_text=f'Mediana={median_food_rating:.2f}')

        # Mostrar el histograma
        st.plotly_chart(fig)
    def bar_comunidad_autonoma_salario_medio(self, colores_comunidades=colores_comunidades):
        salario_medio_por_autonomia = self.data.groupby('comunidad_autonoma')['Salario Medio Anual'].mean().reset_index().sort_values(by= 'Salario Medio Anual', ascending= False)

        salario_medio_por_autonomia['comunidad_autonoma'] = ' '+ salario_medio_por_autonomia['comunidad_autonoma'].str.title()

        # Crear el histograma con Plotly Express
        fig = px.bar(salario_medio_por_autonomia, 
                    x='comunidad_autonoma', 
                    y='Salario Medio Anual', 
                    title='Salario Medio Anual por Comunidad Autónoma',
                    labels={'Salario Medio Anual': 'Salario Medio Anual (€)', 'comunidad_autonoma': 'Comunidad Autónoma '},
                    color='comunidad_autonoma',  # Colorear por comunidad autónoma
                    color_discrete_map = colores_comunidades,
                    template='plotly_white')  # Cambiar el tema del gráfico

        # Ajustar el diseño del gráfico
        fig.update_layout(xaxis_title='Comunidad Autónoma',
                        yaxis_title='Salario Medio Anual (€)',
                        yaxis_tickformat='.3s', width=500)  # Establecer el formato de los ticks del eje y

        # Mostrar el histograma
        st.plotly_chart(fig)
    def bar_comunidad_autonoma_precio_medio(self, colores_comunidades=colores_comunidades):
        # Agrupar los datos por 'comunidad_autonoma' y calcular el precio promedio en cada comunidad
        precio_promedio_por_autonomia = self.data.groupby('comunidad_autonoma')['Average_Price'].mean().reset_index().sort_values(by= 'Average_Price', ascending=False)
        # Crear el histograma con Plotly Express y especificar los colores con el diccionario
        fig = px.bar(precio_promedio_por_autonomia, 
                    x='comunidad_autonoma', 
                    y='Average_Price', 
                    title='Precio Promedio por Comunidad Autónoma',
                    labels={'Average_Price': 'Precio Promedio (€)', 'comunidad_autonoma': 'Comunidad Autónoma'},
                    color='comunidad_autonoma',  # Colorear por comunidad autónoma
                    color_discrete_map=colores_comunidades,  # Usar el diccionario de colores
                    template='plotly_white')  # Cambiar el tema del gráfico

        # Ajustar el diseño del gráfico
        fig.update_layout(xaxis_title='Comunidad Autónoma',
                        yaxis_title='Precio Promedio (€)', width=500) 

        # Mostrar el histograma
        st.plotly_chart(fig)
    def bar_precio_medio_tipo_comida_descendente(self):
        # Calcular el precio medio por cada tipo de comida
        precio_medio_por_tipo_comida = self.data.groupby('Tipo_comida')['Average_Price'].mean().reset_index().sort_values(by='Average_Price', ascending=False).head(15)
        # Crear el histograma con Plotly Express
        fig = px.bar(precio_medio_por_tipo_comida, 
                    x='Tipo_comida', 
                    y='Average_Price', 
                    title='Precio Medio por Tipo de Comida Descendente',
                    labels={'Average_Price': 'Precio Medio (€) ', 'Tipo_comida': 'Tipo de comida'},
                    color='Tipo_comida',  # Colorear por tipo de comida
                    template='plotly_white',
                    width=500)  # Cambiar el tema del gráfico
        # Ajustar el diseño del gráfico
        fig.update_layout(xaxis_title='Tipo de Comida',
                        yaxis_title='Precio Medio (€)',
                        yaxis_tickformat='.1f',
                        showlegend= False, width=500)
        # fig.update_xaxes(range= [-0.5, 15.5])
        # Mostrar el histograma
        st.plotly_chart(fig)
    def bar_precio_medio_tipo_comida_ascendente(self):
        # Calcular el precio medio por cada tipo de comida
        precio_medio_por_tipo_comida = self.data.groupby('Tipo_comida')['Average_Price'].mean().reset_index().sort_values(by='Average_Price', ascending=True).head(15)

        # Crear el histograma con Plotly Express
        fig = px.bar(precio_medio_por_tipo_comida, 
                    x='Tipo_comida', 
                    y='Average_Price', 
                    title='Precio Medio por Tipo de Comida Ascendente',
                    labels={'Average_Price': 'Precio Medio (€) ', 'Tipo_comida': 'Tipo de comida'},
                    color='Tipo_comida',  # Colorear por tipo de comida
                    template='plotly_white',
                    width=500)  # Cambiar el tema del gráfico

        # Ajustar el diseño del gráfico
        fig.update_layout(xaxis_title='Tipo de Comida',
                        yaxis_title='Precio Medio (€)',
                        yaxis_tickformat='.1f',
                        showlegend= False)
        # fig.update_xaxes(range= [-0.5, 15.5])

        # Mostrar el histograma
        st.plotly_chart(fig)

    def pie_michelin(self):
        fig = px.pie(self.data, 
                    names='Michelin', 
                    color_discrete_sequence=['blue', 'orange'],
                    )

        # Configurar el título centrado
        fig.update_layout(title_text='Distribución de Michelin', title_x=0.49, width=500)


        # Mostrar el diagrama de sectores
        st.plotly_chart(fig)

    def pie_reservable(self):
        # Crear el diagrama de sectores con Plotly
        fig = px.pie(self.data, 
                    names='Bookable',
                    labels= {'Bookable': 'Reservable'}, 
                    color_discrete_sequence=['lightseagreen', 'pink'])

        # Configurar el título centrado
        fig.update_layout(title_text='Distribución de reservable', title_x=0.49, width=500)

        # Mostrar el diagrama de sectores
        st.plotly_chart(fig)

    def histograma_metodos_pago(self):
        # Crear el diagrama de sectores con Plotly
        fig = px.histogram(self.data, 
                            x='Cantidad_metodos_pago',  
                            title='Histograma de Frecuencias de métodos de pago',
                            labels={'Cantidad_metodos_pago': 'Métodos de pago'},
                            opacity=0.7, # Hacer el histograma un poco transparente
                            # color_discrete_sequence=['purple'], # Cambiar el color de las barras
                            template='plotly_white') # Cambiar el tema del gráfico


        # Configurar el título centrado
        fig.update_layout(title_text='Distribución de métodos de pago', title_x=0.49, bargap= 0.1, width=500)

        # Mostrar el diagrama de sectores
        st.plotly_chart(fig)

    def histograma_numero_fotos(self):
        fig = px.histogram(self.data, 
                            x='Numero_fotos',  
                            title='Histograma de Frecuencias de número de fotos',
                            nbins= 75,
                            labels={'Numero_fotos': 'Número de fotos'},
                            opacity=0.7, # Hacer el histograma un poco transparente
                            # color_discrete_sequence=['purple'], # Cambiar el color de las barras
                            template='plotly_white') # Cambiar el tema del gráfico


        # Configurar el título centrado
        fig.update_layout(title_text='Distribución de numero de fotos', title_x=0.49, width=500)

        # Mostrar el diagrama de sectores
        st.plotly_chart(fig)
    def correlacion_precio_medio_salario_medio(self):
        # Primero, calculamos la media de los precios medios por provincia
        media_precios_por_provincia = self.data.groupby('Provincia')['Average_Price'].mean()
        # Luego, calculamos el salario medio anual por provincia
        salario_medio_por_provincia = self.data.groupby('Provincia')['Salario Medio Anual'].mean()
        # Finalmente, calculamos la correlación entre estas dos series de datos
        return media_precios_por_provincia.corr(salario_medio_por_provincia)
    # Crear el gráfico de dispersión con Plotly Express
    def scatter_poblacion_restaurantes_provincia(self):
        data= self.data.copy()
        data['Cantidad_Restaurantes'] = data['Provincia'].map(dict(data['Provincia'].value_counts()))
        model = LinearRegression().fit(data[['Poblacion']], data['Cantidad_Restaurantes'])
        x_values= np.linspace(0, 7000000, 10000)
        y_values = model.coef_*x_values + model.intercept_

        data['Cantidad_Restaurantes'] = data.groupby('Provincia')['Provincia'].transform('count')

        fig = px.scatter(data, x='Poblacion', y='Cantidad_Restaurantes', color='Provincia', 
                    hover_name='Provincia', title='Cantidad de Restaurantes por Población por Provincia', trendline= 'expanding', width=500)
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', name='Recta', line={'width': 1, 'color': 'black'}))

    # Añadir etiquetas a los ejes
        fig.update_layout(xaxis_title='Población',
                        
                    yaxis_title='Cantidad de Restaurantes por Provincia')

    # Mostrar el gráfico
        st.plotly_chart(fig)

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a UI on top of a dataframe to let viewers filter columns

        Args:
            df (pd.DataFrame): Original dataframe

        Returns:
            pd.DataFrame: Filtered dataframe
        """
        modify = st.checkbox("Añade nuevos filtros personalizados")

        if not modify:
            return df

        df = df.copy()

        # Try to convert datetimes into a standard format (datetime, no timezone)
        df_columns = df.columns
        for col in df_columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

        modification_container = st.container()

        with modification_container:
            to_filter_columns = st.multiselect("Filtrar por las siguientes columnas", df_columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                left.write("↳")
                # Treat columns with < 10 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    try:
                        user_cat_input = right.multiselect(
                            f"Valores para: {column}",
                            df[column].unique(),
                            default=list(df[column].unique()),
                        )
                        df = df[df[column].isin(user_cat_input)]
                    except:
                        st.write(f"Error al filtrar por {column}")
                elif is_numeric_dtype(df[column]):
                    try:
                        _min = float(df[column].min())
                        _max = float(df[column].max())
                        step = (_max - _min) / 100
                        user_num_input = right.slider(
                            f"Valores para: {column}",
                            _min,
                            _max,
                            (_min, _max),
                            step=step,
                        )
                        df = df[df[column].between(*user_num_input)]
                    except:
                        st.write(f"Error al filtrar por {column}")
                elif is_datetime64_any_dtype(df[column]):
                    try:
                        user_date_input = right.date_input(
                            f"Valores para: {column}",
                            value=(
                                df[column].min(),
                                df[column].max(),
                            ),
                        )
                        if len(user_date_input) == 2:
                            user_date_input = tuple(map(pd.to_datetime, user_date_input))
                            start_date, end_date = user_date_input
                            df = df.loc[df[column].between(start_date, end_date)]
                    except:
                        st.write(f"Error al filtrar por {column}")
                else:
                    try:
                        user_text_input = right.text_input(
                            f"Substring or regex in {column}",
                        )
                        if user_text_input:
                            df = df[df[column].str.contains(user_text_input)]
                    except:
                        st.write(f"Error al filtrar por {column}")

        return df



def corr_bar(data):
    numeric_columns = data.select_dtypes(include=['float64', 'int64'])
    correlation_series = numeric_columns.corr()["Average_Price"].abs().sort_values(ascending=False).drop("Average_Price")
    
    # Creamos un DataFrame con los resultados
    correlation_df = pd.DataFrame(correlation_series, columns=["Average_Price"])
    # Creamos el gráfico de barras horizontales con Plotly Express
    fig = px.bar(correlation_df, x=correlation_df.index, y="Average_Price", orientation="v",
                title="Correlación con Precio medio")
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.6)
    # Mostramos el gráfico en Streamlit
    st.plotly_chart(fig)

