# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:26:35 2026

@author: german
"""

# ============================================================
# ATLAS DEMOGRÁFICO DE GUADALAJARA
# ============================================================

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium

from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
from io import BytesIO

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Atlas Demográfico Guadalajara",
    page_icon="📊",
    layout="wide"
)

st.image(
    "assets/logo_daep.png",
    width=150
)

# ============================================================
# CARGA DE DATOS
# ============================================================

#primero normalizamos los datos

 
def normalizar_texto(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto)

    texto = texto.upper().strip()

    texto = (
        unicodedata.normalize(
            "NFKD",
            texto
        )
        .encode(
            "ASCII",
            "ignore"
        )
        .decode("utf-8")
    )

    texto = " ".join(texto.split())

    return texto



@st.cache_data
def cargar_datos():

    colonias = gpd.read_file(
        "capas/colonias.geojson"
    )

    comunidades = gpd.read_file(
        "capas/comunidades.geojson"
    )

    distritos = gpd.read_file(
        "capas/distritos.geojson"
    )

    indicadores = pd.read_csv(
        "output/indicadores_colonias_catalogado.csv"
    )

    return (
        colonias,
        comunidades,
        distritos,
        indicadores
    )


(
    gdf_colonias,
    gdf_comunidades,
    gdf_distritos,
    indicadores
) = cargar_datos()


# ============================================================
# NORMALIZAR NOMBRES DE COLONIAS
# ============================================================
import unicodedata


gdf_colonias["colonia_norm2"] = (
    gdf_colonias["NOMBRE2"]
    .apply(normalizar_texto)
)

indicadores["colonia_norm2"] = (
    indicadores["Colonia"]
    .apply(normalizar_texto)
)

equivalencias = {

"5 DE MAYO PRIMERA SECCIAN": "5 DE MAYO PRIMERA SECCION",
"5 DE MAYO SEGUNDA SECCIAN": "5 DE MAYO SEGUNDA SECCION",
"AGUSTIN YAAEZ": "AGUSTIN YANEZ",
"ALDAMA TETLAN PRIMERA SECCIAN": "ALDAMA TETLAN PRIMERA SECCION",
"ALDAMA TETLAN SEGUNDA SECCIAN": "ALDAMA TETLAN SEGUNDA SECCION",
"AMPLIACIAN DEL SUR": "AMPLIACION DEL SUR",
"AMPLIACIAN PROVINCIA": "AMPLIACION PROVINCIA",
"AMPLIACIAN TALPITA": "AMPLIACION TALPITA",
"ARCOS VALLARTA SEGUNDA SECCIAN": "ARCOS VALLARTA SEGUNDA SECCION",
"ATLAS SEGUNDA SECCIAN": "ATLAS SEGUNDA SECCION",
"BALCONES DE OBLATOS PRIMERA SECCIAN": "BALCONES DE OBLATOS PRIMERA SECCION",
"BALCONES DE OBLATOS SEGUNDA SECCIAN": "BALCONES DE OBLATOS SEGUNDA SECCION",
"BARAJAS VILLASEAOR": "BARAJAS VILLASENOR",
"BATALLAN DE SAN PATRICIO": "BATALLON DE SAN PATRICIO",
"BLANCO Y CUELLAR PRIMERA SECCIAN": "BLANCO Y CUELLAR PRIMERA SECCION",
"BLANCO Y CUELLAR SEGUNDA SECCIAN": "BLANCO Y CUELLAR SEGUNDA SECCION",
"BLANCO Y CUELLAR TERCERA SECCIAN": "BLANCO Y CUELLAR TERCERA SECCION",
"CAPILLA DE JESAS": "CAPILLA DE JESUS",
"CIRCUNVALACIAN BELISARIO": "CIRCUNVALACION BELISARIO",
"CIRCUNVALACIAN GUEVARA": "CIRCUNVALACION GUEVARA",
"CIRCUNVALACIAN METRO": "CIRCUNVALACION METRO",
"CIRCUNVALACIAN OBLATOS": "CIRCUNVALACION OBLATOS",
"CIRCUNVALACIAN OBLATOS ZONA 4": "CIRCUNVALACION OBLATOS ZONA 4",
"CIRCUNVALACIAN SARCOFAGO": "CIRCUNVALACION SARCOFAGO",
"CIRCUNVALACIAN VALLARTA": "CIRCUNVALACION VALLARTA",
"DEL FRESNO PRIMERA SECCIAN": "DEL FRESNO PRIMERA SECCION",
"DEL FRESNO SEGUNDA SECCIAN": "DEL FRESNO SEGUNDA SECCION",
"ECHEVERRIA PRIMERA SECCIAN": "ECHEVERRIA PRIMERA SECCION",
"ECHEVERRIA SEGUNDA SECCIAN": "ECHEVERRIA SEGUNDA SECCION",
"ECHEVERRIA TERCERA SECCIAN": "ECHEVERRIA TERCERA SECCION",
"HELIODORO HERNANDEZ PRIMERA SECCIAN": "HELIODORO HERNANDEZ PRIMERA SECCION",
"HELIODORO HERNANDEZ SEGUNDA SECCIAN": "HELIODORO HERNANDEZ SEGUNDA SECCION",
"HUENTITAAN EL BAJO PRIMERA SECCIAN": "HUENTITAN EL BAJO PRIMERA SECCION",
"HUENTITAN EL BAJO SEGUNDA SECCIAN": "HUENTITAN EL BAJO SEGUNDA SECCION",
"INDUSTRIAL PRIMERA SECCIAN": "INDUSTRIAL PRIMERA SECCION",
"INDUSTRIAL SEGUNDA SECCIAN": "INDUSTRIAL SEGUNDA SECCION",
"INDUSTRIAL TERCERA SECCIAN": "INDUSTRIAL TERCERA SECCION",
"INSURGENTES PRIMERA SECCIAN": "INSURGENTES PRIMERA SECCION",
"INSURGENTES SEGUNDA SECCIAN": "INSURGENTES SEGUNDA SECCION",
"INSURGENTES TERCERA SECCIAN": "INSURGENTES TERCERA SECCION",
"JARDINES DE LA CRUZ PRIMERA SECCIAN": "JARDINES DE LA CRUZ PRIMERA SECCION",
"JARDINES DE LA CRUZ SEGUNDA SECCIAN": "JARDINES DE LA CRUZ SEGUNDA SECCION",
"JARDINES DEL COUNTRY SEGUNDA SECCIAN": "JARDINES DEL COUNTRY SEGUNDA SECCION",
"JARDINES DEL COUNTRY TERCERA SECCIAN": "JARDINES DEL COUNTRY TERCERA SECCION",
"LAGOS DE ORIENTE PRIMERA SECCIAN": "LAGOS DE ORIENTE PRIMERA SECCION",
"LAGOS DE ORIENTE SEGUNDA SSECCIAN": "LAGOS DE ORIENTE SEGUNDA SSECCION",
"LOMAS DE OBLATOS PRIMERA SECCIAN": "LOMAS DE OBLATOS PRIMERA SECCION",
"LOMAS DE OBLATOS SEGUNDA SECCIAN": "LOMAS DE OBLATOS SEGUNDA SECCION",
"LOMAS DE REVOLUCIAN": "LOMAS DE REVOLUCION",
"LOMAS DEL PARAISO CUARTA SECCIAN": "LOMAS DEL PARAISO CUARTA SECCION",
"LOMAS DEL PARAISO PRIMERA SECCIAN": "LOMAS DEL PARAISO PRIMERA SECCION",
"LOMAS DEL PARAISO QUINTA SECCIAN": "LOMAS DEL PARAISO QUINTA SECCION",
"LOMAS DEL PARAISO SEGUNDA SECCIAN": "LOMAS DEL PARAISO SEGUNDA SECCION",
"LOMAS DEL PARAISO TERCERA SECCIAN": "LOMAS DEL PARAISO TERCERA SECCION",
"MIRAVALLE CUARTA SECCIAN": "MIRAVALLE CUARTA SECCION",
"MIRAVALLE NOVENA SECCIAN": "MIRAVALLE NOVENA SECCION",
"MIRAVALLE OCTAVA SECCIAN": "MIRAVALLE OCTAVA SECCION",
"MIRAVALLE PRIMERA SECCIAN": "MIRAVALLE PRIMERA SECCION",
"MIRAVALLE SEGUNDA SECCIAN": "MIRAVALLE SEGUNDA SECCION",
"MIRAVALLE SEXTA SECCIAN": "MIRAVALLE SEXTA SECCION",
"MIRAVALLE TERCERA SECCIAN": "MIRAVALLE TERCERA SECCION",
"NIAOS HEROES": "NINOS HEROES",
"NUEVA ESPAAA": "NUEVA ESPANA",
"OBLATOS PRIMERA SECCIAN": "OBLATOS PRIMERA SECCION",
"OBLATOS SEGUNDA SECCIAN": "OBLATOS SEGUNDA SECCION",
"OBLATOS TERCERA SECCIAN": "OBLATOS TERCERA SECCION",
"PANORAMICA PRIMERA SECCIAN": "PANORAMICA PRIMERA SECCION",
"PANORAMICA SEGUNDA SECCIAN": "PANORAMICA SEGUNDA SECCION",
"PROVIDENCIA CUARTA SECCIAN": "PROVIDENCIA CUARTA SECCION",
"PROVIDENCIA QUINTA SECCIAN": "PROVIDENCIA QUINTA SECCION",
"PROVIDENCIA SEGUNDA SECCIAN": "PROVIDENCIA SEGUNDA SECCION",
"PROVIDENCIA TERCERA SECCIAN": "PROVIDENCIA TERCERA SECCION",
"RANCHO NUEVO PRIMERA SECCIAN": "RANCHO NUEVO PRIMERA SECCION",
"RANCHO NUEVO SEGUNDA SECCIAN": "RANCHO NUEVO SEGUNDA SECCION",
"ROJAS LADRAN DE GUEVARA": "ROJAS LADRON DE GUEVARA",
"SAN ANDRES CUARTA SECCIAN": "SAN ANDRES CUARTA SECCION",
"SAN ANDRES PRIMERA SECCIAN": "SAN ANDRES PRIMERA SECCION",
"SAN FELIPE PRIMERA SECCIAN": "SAN FELIPE PRIMERA SECCION",
"SAN FELIPE SEGUNDA SECCIAN": "SAN FELIPE SEGUNDA SECCION",
"SAN JOSE RIO VERDE PRIMERA SECCIAN": "SAN JOSE RIO VERDE PRIMERA SECCION",
"SAN JOSE RIO VERDE SEGUNDA SECCIAN": "SAN JOSE RIO VERDE SEGUNDA SECCION",
"SAN MIGUEL DE HUENTITAN PRIMERA SECCIAN": "SAN MIGUEL DE HUENTITAN PRIMERA SECCION",
"SAN MIGUEL DE HUENTITAN SEGUNDA SECCIAN": "SAN MIGUEL DE HUENTITAN SEGUNDA SECCION",
"SAN MIGUEL DE HUENTITAN TERCERA SECCIAN": "SAN MIGUEL DE HUENTITAN TERCERA SECCION",
"SANTA CECILIA PRIMERA SECCIAN": "SANTA CECILIA PRIMERA SECCION",
"SANTA CECILIA SEGUNDA SECCIAN": "SANTA CECILIA SEGUNDA SECCION",
"SANTA CECILIA TERCERA SECCIAN": "SANTA CECILIA TERCERA SECCION",
"SANTA MONICA PRIMERA SECCIAN": "SANTA MONICA PRIMERA SECCION",
"SANTA MONICA SEGUNDA SECCIAN": "SANTA MONICA SEGUNDA SECCION",
"SANTUARIO SEGUNDA SECCIAN": "SANTUARIO SEGUNDA SECCION",
"VALENTIN GAMEZ FARIAS": "VALENTIN GOMEZ FARIAS",
"VILLASEAOR": "VILLASENOR",
"JARDAN DE LOS HISTORIADORES": "JARDIN DE LOS HISTORIADORES",
"JARDAN DE LOS POETAS": "JARDIN DE LOS POETAS",
"AGUSTAN YAAEZ": "AGUSTIN YANEZ",
"JARDAN DE LOS ESCRITORES": "JARDIN DE LOS ESCRITORES",
"VALENTAN GAMEZ FARAAS": "VALENTIN GOMEZ FARIAS",
"POPULAR SAN MARTAN": "POPULAR SAN MARTIN"
}

gdf_colonias["colonia_norm2"] = (
    gdf_colonias["colonia_norm2"]
    .replace(equivalencias)
)



# ============================================================
# UNIÓN DE DATOS
# ============================================================

gdf = gdf_colonias.merge(
    indicadores,
    on="colonia_norm2",
    how="left"
)

gdf["distrito"] = (
    gdf["distrito"]
    .astype(str)
    .str.strip()
)


# ============================================================
# VARIABLES DISPONIBLES
# ============================================================

variables = [
    c for c in indicadores.columns
    if c not in [
        "Colonia",
        "nombre2",
        "colonia_norm2",
        "comunidad",
        "distrito"
    ]
]

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Filtros geográficos")


# ============================================================
# FILTRO DISTRITO
# ============================================================

lista_distritos = sorted(
    gdf["distrito"]
    .dropna()
    .astype(str)
    .unique()
)

distrito = st.sidebar.selectbox(
    "Distrito",
    ["Todos"] + lista_distritos
)

# ============================================================
# FILTRAR PARA COMUNIDADES
# ============================================================

df_temp = gdf.copy()

if distrito != "Todos":
    df_temp = df_temp[
        df_temp["distrito"] == distrito
    ]

# ============================================================
# FILTRO COMUNIDAD
# ============================================================

lista_comunidades = sorted(
    df_temp["comunidad"]
    .dropna()
    .astype(str)
    .unique()
)

comunidad = st.sidebar.selectbox(
    "Comunidad",
    ["Todas"] + lista_comunidades
)

# ============================================================
# FILTRAR PARA COLONIAS
# ============================================================

if comunidad != "Todas":
    df_temp = df_temp[
        df_temp["comunidad"] == comunidad
    ]

# ============================================================
# FILTRO COLONIA
# ============================================================

lista_colonias = sorted(
    df_temp["Colonia"]
    .dropna()
    .astype(str)
    .unique()
)

colonia_seleccionada = st.sidebar.selectbox(
    "Colonia",
    ["Todas"] + lista_colonias
)

# ============================================================
# APLICAR FILTROS
# ============================================================

gdf_filtrado = gdf.copy()

if distrito != "Todos":
    gdf_filtrado = gdf_filtrado[
        gdf_filtrado["distrito"] == distrito
    ]

if comunidad != "Todas":
    gdf_filtrado = gdf_filtrado[
        gdf_filtrado["comunidad"] == comunidad
    ]

if colonia_seleccionada != "Todas":
    gdf_filtrado = gdf_filtrado[
        gdf_filtrado["Colonia"] == colonia_seleccionada
    ]


# ============================================================
# DASHBOARD
# ============================================================

st.title("📊 Atlas Demográfico de Guadalajara")

busqueda = "Todo Guadalajara"

if comunidad != "Todas":
    busqueda = f"Comunidad: {comunidad}"

if distrito != "Todos":
    busqueda = f"Distrito: {distrito}"

if colonia_seleccionada != "Todas":
    busqueda = f"Colonia: {colonia_seleccionada}"

st.markdown(
    f"### Búsqueda por: **{busqueda}**"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Colonias",
    gdf_filtrado["Colonia"].nunique()
)

col2.metric(
    "Población",
    f"{gdf_filtrado['POBTOT'].sum():,.0f}"
)

col3.metric(
    "Hogares",
    f"{gdf_filtrado['TOTHOG'].sum():,.0f}"
)

col4.metric(
    "Viviendas",
    f"{gdf_filtrado['VIVTOT'].sum():,.0f}"
)

st.markdown("---")

variable = st.selectbox(
    "Indicador para visualizar en el mapa",
    variables
)

# ============================================================
# MAPA
# ============================================================

m = folium.Map(
    location=[20.6736, -103.344],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# ============================================================
# COROPLETA
# ============================================================

folium.Choropleth(
    geo_data=gdf_filtrado,
    data=gdf_filtrado,
    columns=[
        "Colonia",
        variable
    ],
    key_on="feature.properties.Colonia",
    fill_color="YlGnBu",
    fill_opacity=0.55,
    line_opacity=0.2,
    legend_name=variable,
    nan_fill_color="lightgray"
).add_to(m)


# ============================================================
# POPUPS
# ============================================================
# ============================================================
# TOOLTIP Y POPUP INTERACTIVO
# ============================================================

#folium.GeoJson(
#    gdf_filtrado,
#    name="Colonias",
#    style_function=lambda feature: {
#        "fillOpacity": 0,
#        "weight": 0,
#        "color": "transparent"
#    },
#    tooltip=folium.GeoJsonTooltip(
#        fields=["Colonia"],
#        aliases=["Colonia:"],
#        sticky=True
#    ),
#    popup=folium.features.GeoJsonPopup(
#        fields=[
#            "Colonia",
#            "comunidad",
#            "POBTOT"
#        ],
#        aliases=[
#            "Colonia",
#            "Comunidad",
#            "Población total"
#        ],
#        localize=True,
#        labels=True
#    )
#).add_to(m)

# ============================================================
# COMUNIDADES
# ============================================================

folium.GeoJson(
    gdf_comunidades,
    name="Comunidades",
    style_function=lambda x: {
        "fillOpacity":0,
        "color":"green",
        "weight":3
    }
).add_to(m)

# ============================================================
# DISTRITOS
# ============================================================

folium.GeoJson(
    gdf_distritos,
    name="Distritos",
    style_function=lambda x: {
        "fillOpacity":0,
        "color":"orange",
        "weight":3
    }
).add_to(m)

# ============================================================
# CONTROL DE CAPAS
# ============================================================

folium.LayerControl().add_to(m)

# ============================================================
# MOSTRAR MAPA
# ============================================================

st_folium(
    m,
    use_container_width=True,
    height=750
)


# ============================================================
# DATOS POR COLONIA
# ============================================================
st.subheader("Consulta independiente por colonia")

colonia_consulta = st.selectbox(
    "Seleccione una colonia",
    sorted(
        gdf["Colonia"]
        .dropna()
        .unique()
    )
)

datos_colonia = gdf[
    gdf["Colonia"] == colonia_consulta
]

if len(datos_colonia) > 0:

    fila = datos_colonia.iloc[0]

    tabla = pd.DataFrame({

        "Indicador":[
            "Población total",
            "Mujeres",
            "Hombres",
            "Población con discapacidad",
            "Población económicamente activa",
            "Población sin servicios de salud",
            "Hogares",
            "Viviendas"
        ],

        "Valor":[
            fila["POBTOT"],
            fila["POBFEM"],
            fila["POBMAS"],
            fila["PCON_DISC"],
            fila["PEA"],
            fila["PSINDER"],
            fila["TOTHOG"],
            fila["VIVTOT"]
        ]

    })

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True
    )



# ============================================================
# EXPORTAR EXCEL
# ============================================================

st.subheader(
    "Descarga de información filtrada"
)

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    exportar = pd.DataFrame(
        gdf_filtrado.drop(
            columns="geometry",
            errors="ignore"
            )
        )

    exportar.to_excel(
        writer,
        index=False,
        sheet_name="Datos"
        )

st.download_button(
    label="📥 Descargar Excel",
    data=excel_buffer.getvalue(),
    file_name="atlas_demografico_filtrado.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument"
        ".spreadsheetml.sheet"
    )
)

st.markdown("---")

st.subheader("Notas metodológicas")

st.markdown("""
**Fuente:** Censo de Población y Vivienda 2020, INEGI.

La información presentada corresponde a una reconstrucción territorial a nivel de colonia para el municipio de Guadalajara. Los datos censales fueron agregados a partir de unidades geográficas de menor escala mediante procedimientos de correspondencia espacial entre manzanas censales y polígonos de colonias.

Las cifras deben utilizarse con fines de análisis territorial y planeación. Debido a los procesos de agregación espacial y redistribución geográfica, algunos totales pueden diferir ligeramente de los publicados por INEGI para otras unidades territoriales.

Esta herramienta fue desarrollada por la Dirección de Análisis Estratégico y Prospectiva del Gobierno de Guadalajara.
""")


col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "assets/logo_daep.png",
        width=350
    )