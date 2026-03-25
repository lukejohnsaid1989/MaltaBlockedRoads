import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🚧 Malta Road Closures Map")

DATA_URL = "https://drive.google.com/uc?export=download&id=1ELRtKbteqWXh8GeYE4iysxQcSIJP9l_2"

@st.cache_data(ttl=300)
def load_data(url):
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data(DATA_URL)
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')

# --- Sidebar Date Filter ---
selected_dates = st.sidebar.multiselect(
    "Select Date(s) of Closures",
    options=df['date'].dt.date.unique(),
    default=df['date'].dt.date.unique()
)

df_filtered = df[df['date'].dt.date.isin(selected_dates)]

st.subheader(f"Showing {len(df_filtered)} closed roads")

# --- PyDeck Map ---
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    get_position='[lon, lat]',
    get_color='[255, 0, 0]',
    get_radius=20,  # smaller radius
    pickable=True
)

view_state = pdk.ViewState(
    latitude=35.8997,
    longitude=14.5146,
    zoom=11,
    pitch=0
)

# Correct tooltip syntax for column names with spaces
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Street:</b> {street} <br/> <b>Locality:</b> {locality} <br/> <b>Date:</b> {date_str}"
    }
)

st.pydeck_chart(r)
