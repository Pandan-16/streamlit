import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

#data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Raw data')
st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

#Exercise 
#1. Convert 2D map to 3D map using PyDeck
st.subheader('Convert 2D map to 3D map using PyDeck')
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=data['lat'].mean(),
            longitude=data['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)

#2. Use date input
# Date input
st.sidebar.header("Filter Options")
selected_date = st.sidebar.date_input(
    "Select a date",
    value=data[DATE_COLUMN].dt.date.min()
)

# Hour slider
hour_to_filter = st.sidebar.slider('Hour', 0, 23, 17)

# Filter by date + hour
filtered_data = data[
    (data[DATE_COLUMN].dt.date == selected_date) &
    (data[DATE_COLUMN].dt.hour == hour_to_filter)
]

st.subheader(f"3D Map of pickups on {selected_date} at {hour_to_filter}:00")

# Create HexagonLayer
layer = pdk.Layer(
    "HexagonLayer",
    data=filtered_data,
    get_position='[lon, lat]',
    auto_highlight=True,
    radius=100,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# Set map view
if not filtered_data.empty:
    view_state = pdk.ViewState(
        latitude=filtered_data['lat'].mean(),
        longitude=filtered_data['lon'].mean(),
        zoom=11,
        pitch=50,
    )

    # Show deck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Elevation: {elevationValue}"}
    )
    st.pydeck_chart(deck)
else:
    st.warning("No data available for this date and time.")


#3. Use Selectbox
import streamlit as st
import numpy as np
import pandas as pd

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

#4. Use plotly (any charts)
import streamlit as st
import pandas as pd
import numpy as np

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("Choose a datapoint color")
color = st.color_picker("Color", "#FF0000")
st.divider()
st.scatter_chart(st.session_state.df, x="x", y="y", color=color)


#5. Click a button to increase the number in the following message, "This page has run 24 times"
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")


