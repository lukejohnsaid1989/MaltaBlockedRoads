import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🚧 Malta Road Closures Map")

# --- Data ---
DATA_URL = "https://drive.google.com/uc?export=download&id=1ELRtKbteqWXh8GeYE4iysxQcSIJP9l_2"

@st.cache_data(ttl=300)
def load_data(url):
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
    return df

df = load_data(DATA_URL)

# --- Sidebar Date Filter ---
selected_dates = st.sidebar.multiselect(
    "Select Date(s) of Closures",
    options=df['date'].dt.date.unique(),
    default=df['date'].dt.date.unique()
)

# Filter DataFrame by selected dates
df_filtered = df[df['date'].dt.date.isin(selected_dates)].copy()

st.subheader(f"Showing {len(df_filtered)} closed roads")

# --- Village Zoom Selector ---
village_options = ['All'] + list(df['locality'].unique())
selected_village = st.sidebar.selectbox("Zoom to Village", options=village_options)

if selected_village != 'All':
    village_data = df_filtered[df_filtered['locality'] == selected_village]
    if not village_data.empty:
        center_lat = village_data['lat'].mean()
        center_lon = village_data['lon'].mean()
        zoom_level = 13
    else:
        center_lat = 35.8997
        center_lon = 14.5146
        zoom_level = 11
else:
    center_lat = 35.8997
    center_lon = 14.5146
    zoom_level = 11

# --- PyDeck Layer (semi-transparent circles only) ---
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    get_position='[lon, lat]',
    get_fill_color='[255, 0, 0, 80]',  # semi-transparent red
    get_radius=40,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=zoom_level,
    pitch=0
)

deck = pdk.Deck(
    layers=[scatter_layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Street:</b> {street} <br/> <b>Locality:</b> {locality} <br/> <b>Date:</b> {date_str}"
    },
    height=700,
    map_style=None
)

st.pydeck_chart(deck, use_container_width=True)
