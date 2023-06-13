import pandas as pd
import streamlit as st
from wordcloud import WordCloud

# Carga los datos del archivo en un DataFrame
df = pd.read_csv('logs.csv')

# Convierte la columna de fechas en tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Obtiene el día de la semana para cada fecha
df['dia_semana'] = df['fecha'].dt.day_name()

# Realiza un gráfico comparando los días de la semana en que se realizaron operaciones usando la aplicación
st.subheader('Operaciones por día de la semana')
operaciones_por_dia = df['dia_semana'].value_counts()
orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
operaciones_por_dia = operaciones_por_dia.reindex(orden_dias)
st.bar_chart(operaciones_por_dia)

# Carga los datos del archivo de perfiles en otro DataFrame
df_perfiles = pd.read_json('datos/perfil.json')

# Relaciona el archivo de logs con el archivo de perfiles
df_completo = pd.merge(df, df_perfiles, on='usuario')

# Genera un gráfico que muestra los porcentajes de uso de la aplicación por género
st.subheader('Porcentaje de uso de la aplicación por género')
porcentaje_por_genero = df_completo['genero'].value_counts(normalize=True) * 100
st.pie_chart(porcentaje_por_genero)

# Genera un gráfico que refleja las cantidades de cada operación realizada
st.subheader('Cantidad de cada operación realizada')
cantidad_operaciones = df['operacion'].value_counts()
st.bar_chart(cantidad_operaciones)

# Genera un gráfico de barra apilado que muestra las cantidades de operaciones por nick
st.subheader('Cantidades de operaciones por nick')
cantidades_por_nick_operacion = df.groupby(['nick', 'operacion']).size().unstack()
st.bar_chart(cantidades_por_nick_operacion)

# Filtra las operaciones relacionadas con memes y collages
df_memes = df[df['operacion'] == 'generar_memes']
df_collages = df[df['operacion'] == 'generar_collages']

# Genera un ranking de las 5 imágenes más usadas para generar memes
ranking_memes = df_memes['imagen'].value_counts().head(5)
st.subheader('Ranking de imágenes más usadas para generar memes')
st.write(ranking_memes)

# Genera un ranking de las 5 imágenes más usadas para generar collages
ranking_collages = df_collages['imagen'].value_counts().head(5)
st.subheader('Ranking de imágenes más usadas para generar collages')
st.write(ranking_collages)

# Obtiene los textos de los collages y memes
textos_collages = ' '.join(df_collages['texto'].dropna())
textos_memes = ' '.join(df_memes['texto'].dropna())

# Crea la nube de palabras para los collages
wordcloud_collages = WordCloud().generate(textos_collages)
st.subheader('Nube de palabras - Collages')
st.image(wordcloud_collages.to_array())

# Crea la nube de palabras para los memes
wordcloud_memes = WordCloud().generate(textos_memes)
st.subheader('Nube de palabras - Memes')
st.image(wordcloud_memes.to_array())

# Filtra las operaciones de interés
operaciones_interes = ['Nueva imagen clasificada', 'Modificación de imagen previamente clasificada']
df_operaciones_interes = df[df['operacion'].isin(operaciones_interes)]

# Relaciona las operaciones de interés con los perfiles
df_operaciones_perfiles = pd.merge(df_operaciones_interes, df_perfiles, on='usuario')

# Genera un gráfico de torta con los porcentajes según género de las personas que realizaron las operaciones
st.subheader('Porcentaje según género de personas que realizaron operaciones de interés')
porcentaje_por_genero_operaciones = df_operaciones_perfiles['genero'].value_counts(normalize=True) * 100
st.pie_chart(porcentaje_por_genero_operaciones)