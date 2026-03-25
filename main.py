import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🚧 Malta Road Closures Map")

# --- Google Drive CSV URL ---
DATA_URL = "https://drive.google.com/uc?export=download&id=1ELRtKbteqWXh8GeYE4iysxQcSIJP9l_2"

# --- Load Data with caching ---
@st.cache_data(ttl=300)  # cache for 5 minutes
def load_data(url):
    df = pd.read_csv(url)
    # Ensure date is datetime type
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data(DATA_URL)

# --- Sidebar: Date Filter ---
selected_dates = st.sidebar.multiselect(
    "Select Date(s) of Closures",
    options=df['date'].dt.date.unique(),
    default=df['date'].dt.date.unique()
)

# Filter the DataFrame
df_filtered = df[df['date'].dt.date.isin(selected_dates)]

st.subheader(f"Showing {len(df_filtered)} closed roads")

# --- PyDeck Interactive Map ---
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    get_position='[lon, lat]',
    get_color='[255, 0, 0]',
    get_radius=50,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=35.8997,
    longitude=14.5146,
    zoom=11,
    pitch=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{street name}\n{Locality}\nDate: {date}"}
)

st.pydeck_chart(r)
