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

# --- Sidebar Filters ---
selected_dates = st.sidebar.multiselect(
    "Select Date(s) of Closures",
    options=df['date'].dt.date.unique(),
    default=df['date'].dt.date.unique()
)

selected_localities = st.sidebar.multiselect(
    "Select Localities",
    options=df['locality'].unique(),
    default=df['locality'].unique()
)

# --- Filter DataFrame ---
df_filtered = df[
    df['date'].dt.date.isin(selected_dates) &
    df['locality'].isin(selected_localities)
].copy()

st.subheader(f"Showing {len(df_filtered)} closed roads")

# --- PyDeck Layers ---

# Optional: small transparent points
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    get_position='[lon, lat]',
    get_fill_color='[255, 0, 0, 80]',  # semi-transparent
    get_radius=10,
    pickable=True
)

# Text layer for street names
text_layer = pdk.Layer(
    "TextLayer",
    data=df_filtered,
    get_position='[lon, lat]',
    get_text='street name',  # exact column name
    get_size=16,
    get_color=[0, 0, 0],
    get_angle=0,
    get_text_anchor='"middle"',
    get_alignment_baseline='"bottom"'
)

# --- Map view ---
view_state = pdk.ViewState(
    latitude=35.8997,
    longitude=14.5146,
    zoom=11,
    pitch=0
)

deck = pdk.Deck(
    layers=[scatter_layer, text_layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Street:</b> {street} <br/> <b>Locality:</b> {locality} <br/> <b>Date:</b> {date_str}"
    },
    map_style='mapbox://styles/mapbox/light-v10',  # cleaner style
    height=700  # bigger map
)

st.pydeck_chart(deck, use_container_width=True)

