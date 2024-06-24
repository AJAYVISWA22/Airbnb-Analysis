import pandas as pd
import pymongo
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit_option_menu import option_menu
from PIL import Image

Air_icon=Image.open("Images/airbnb-logo.png")
airbnb_image1=Image.open("Images/add1.jpg")
airbnb_image2=Image.open("Images/add2.jpg")

df=pd.read_csv('TREATED_DATA.csv')


def map3d(filtered_df):
    # Extract latitude, longitude, and text labels for markers
    lat_values = filtered_df['Latitude'].tolist()
    lon_values = filtered_df['Longitude'].tolist()
    text_labels = [f"{Name} ({Country_code}) - ${Price}" for Name, Country_code, Price in zip(filtered_df['Name'], filtered_df['Country_code'], filtered_df['Price'])]

    # Create a 3D scatter plot on a geographic map
    fig = go.Figure(
        go.Scattergeo(
            lat=lat_values,
            lon=lon_values,
            text=text_labels,
            mode='markers',
        )
    )

    # Update marker size and line color
    fig.update_traces(marker_size=8, marker=dict(color='Red'), hoverinfo="text")

    # Update geos with additional parameters for showing ocean and countries
    fig.update_geos(
        projection_type="orthographic",
        showocean=True, oceancolor="LightBlue",
        showcountries=True, countrycolor="Black",
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="Lightgreen",
        showlakes=True, lakecolor="Blue",
    )

    # Update layout for the figure
    fig.update_layout(
        width=800, height=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)

def map3d_country(filtered_df, country, zoom_level=5):
    # Ensure 'Country' column exists and handle if it doesn't
    if 'Country' not in filtered_df.columns:
        st.error("The 'Country' column does not exist in the DataFrame.")
        return

    # Filter the DataFrame for the specified country or countries
    country_df = filtered_df[filtered_df['Country'].isin(country)]

    if country_df.empty:
        st.warning("No data available for the selected country/countries.")
        return

    # Extract latitude, longitude, and text labels for markers
    lat_values = country_df['Latitude'].tolist()
    lon_values = country_df['Longitude'].tolist()
    text_labels = [f"{Name} ({Country_code}) - ${Price}" for Name, Country_code, Price in zip(country_df['Name'], country_df['Country_code'], country_df['Price'])]

    # Define country settings for centering and zooming
    country_settings = {
        'United States': {'lat_range': [24, 50], 'lon_range': [-125, -66], 'center': {'lat': 37.0902, 'lon': -95.7129}},
        'Turkey': {'lat_range': [36, 42], 'lon_range': [26, 45], 'center': {'lat': 39.9334, 'lon': 32.8597}},
        'Hong Kong': {'lat_range': [22, 23], 'lon_range': [113, 115], 'center': {'lat': 22.3193, 'lon': 114.1694}},
        'Australia': {'lat_range': [-44, -10], 'lon_range': [112, 154], 'center': {'lat': -25.2744, 'lon': 133.7751}},
        'Portugal': {'lat_range': [36, 42], 'lon_range': [-10, -6], 'center': {'lat': 39.3999, 'lon': -8.2245}},
        'Brazil': {'lat_range': [-34, 6], 'lon_range': [-74, -34], 'center': {'lat': -14.235, 'lon': -51.9253}},
        'Canada': {'lat_range': [42, 83], 'lon_range': [-140, -52], 'center': {'lat': 56.1304, 'lon': -106.3468}},
        'Spain': {'lat_range': [35, 44], 'lon_range': [-10, 4], 'center': {'lat': 40.4637, 'lon': -3.7492}},
        'China': {'lat_range': [18, 54], 'lon_range': [73, 135], 'center': {'lat': 35.8617, 'lon': 104.1954}}
    }

    # Get the settings for the specified countries (using default if not listed)
    settings = country_settings.get(country[0], {
        'lat_range': [filtered_df['Latitude'].min(), filtered_df['Latitude'].max()],
        'lon_range': [filtered_df['Longitude'].min(), filtered_df['Longitude'].max()],
        'center': {'lat': filtered_df['Latitude'].mean(), 'lon': filtered_df['Longitude'].mean()}
    })

    # Calculate zoom level based on lat_values and lon_values
    lat_min, lat_max = min(lat_values), max(lat_values)
    lon_min, lon_max = min(lon_values), max(lon_values)

    settings['lat_range'] = [lat_min - zoom_level, lat_max + zoom_level]
    settings['lon_range'] = [lon_min - zoom_level, lon_max + zoom_level]

    # Create a 3D scatter plot on a geographic map
    fig = go.Figure(
        go.Scattergeo(
            lat=lat_values,
            lon=lon_values,
            text=text_labels,
            mode='markers',
        )
    )

    # Update marker size and line color
    fig.update_traces(marker_size=8, marker=dict(color='Red'), hoverinfo="text")

    # Update geos with additional parameters for focusing on the specified countries
    fig.update_geos(
        projection_type="orthographic",
        showocean=True, oceancolor="LightBlue",
        showcountries=True, countrycolor="Black",
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="LightGreen",
        showlakes=True, lakecolor="Blue",
        lataxis_range=settings['lat_range'],  # Latitude range for the specified countries
        lonaxis_range=settings['lon_range'],  # Longitude range for the specified countries
        center=settings['center']  # Centering the map on the specified countries
    )

    # Update layout for the figure
    fig.update_layout(
        width=800, height=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)





def for_home():
   # Main Title and Subtitle
    st.title("Welcome to Airbnb Analysis")
    st.subheader("Unlock insights from Airbnb data across the world.")

    # Introduction Text
    st.write("""
    Discover the trends and insights in the world of Airbnb. Analyze the most popular locations, pricing trends, and the availability of listings in various cities. Whether you are a host looking to optimize your listing or a traveler seeking the best destinations, our interactive visualizations provide the data you need.
    
    Our comprehensive dataset includes detailed information on listings, reviews, and host activities, offering a unique perspective on the dynamics of the Airbnb market.
    """)

    # Columns for Image and Video
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Airbnb: Your Home Away From Home")
        st.image(airbnb_image1)
        st.markdown("[EXPLORE MORE](https://www.airbnb.com/)", unsafe_allow_html=True)

    with col2:
        st.subheader("Discover Unique Stays")
        st.image(airbnb_image2)

    # Interactive Elements: Data Visualization Introduction
    st.write("## How Our Airbnb Data Visualization Works")
    st.write("""
    Our Airbnb Data Visualization platform allows you to explore various aspects of Airbnb listings. Delve into the data to understand pricing patterns, popular locations, and the availability of listings.
    """)

    # Selectbox for Interest Area
    st.write("### Select Your Interest Area")
    interest = st.selectbox("Choose an area to explore:", ["Listings", "Prices", "Locations"])

    if interest == "Listings":
        st.write("## Listing Insights")
        st.write("Explore detailed insights on Airbnb listings across different cities and neighborhoods.")
        # Add more detailed analysis or visualization code here

    elif interest == "Prices":
        st.write("## Price Insights")
        st.write("Discover the trends and insights about Airbnb pricing across various regions.")
        # Add more detailed analysis or visualization code here

    elif interest == "Locations":
        st.write("## Location Insights")
        st.write("Find out which locations are most popular among Airbnb users.")
        # Add more detailed analysis or visualization code here


def for_search():
    
    st.subheader("Airbnb: Your Home Away From Home")
    l_col,m_col,r_col=st.columns([1,2,1])
    
    with m_col:
        map3d(df)

    
    st.sidebar.header("Choose your filter: ")

    # Create for Country
    Country = st.sidebar.multiselect("Pick your Country", df["Country"].unique())
    if not Country:
        df2 = df.copy()
    else:
        df2 = df[df["Country"].isin(Country)]

    # Create for neighbourhood
    neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
    if not neighbourhood:
        df3 = df2.copy()
    else:
        df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

    if not Country and not neighbourhood:
        filtered_df = df
    elif not neighbourhood:
        filtered_df = df[df["Country"].isin(Country)]
    elif not Country:
        filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
    else:
        filtered_df = df3[df3["Country"].isin(Country) & df3["neighbourhood"].isin(neighbourhood)]



    Room_type_df = filtered_df.groupby(by=["Country", "Room_type"]).size().reset_index(name='Count')
    country_df = filtered_df.groupby(by=["Country"]).size().reset_index(name='Total Rooms')



    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Room_type_ViewData")
        fig = px.bar(Room_type_df, x="Room_type", y="Count", hover_data=["Country"], template="seaborn")
        
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader("Country_ViewData")
        fig = px.pie(country_df, values="Total Rooms", names="Country", hole=0.5)
        fig.update_traces(text=filtered_df["Country"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    cl1, cl2 = st.columns((2))
    with cl1:
        with st.expander("Country wise Room_type"):
            st.write(Room_type_df.style.background_gradient(cmap="Blues"))
            csv = Room_type_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Room_type.csv", mime="text/csv",
                            help='Click here to download the data as a CSV file')

    with cl2:
        with st.expander("Total rooms in Country"):
           
            st.write(country_df.style.background_gradient(cmap="Oranges"))
            csv = country_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Country.csv", mime="text/csv",
                            help='Click here to download the data as a CSV file')


    # Create a scatter plot
    data1 = px.scatter(filtered_df, x="Room_type", y="neighbourhood", color="Country")
    data1['layout'].update(title="Room_type in the Neighbourhood and Country wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="Room_type", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
    st.plotly_chart(data1, use_container_width=True)

    

def for_view():
    st.subheader("Discover Unique Stays")
    Country = st.sidebar.multiselect("Pick your Country", df["Country"].unique())

    if not Country:
        df2 = df.copy()
    else:
        df2 = df[df["Country"].isin(Country)]

    # Create for neighbourhood
    neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
   
    if not neighbourhood:
        df3 = df2.copy()
    else:
        df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

    Room_type = st.sidebar.multiselect("Pick the Room_type", df3["Room_type"].unique())
    if not Room_type:
        df4=df3.copy()
    else:
        df4=df3[df3["Room_type"].isin(Room_type)]


    if not Country and not neighbourhood and not Room_type:
        filtered_df = df
    elif not neighbourhood  and  not Room_type:
        filtered_df = df[df["Country"].isin(Country)]
    elif Country and neighbourhood and not Room_type:
        filtered_df = df3[df3["Country"].isin(Country) & df3["neighbourhood"].isin(neighbourhood)]
    elif Country and Room_type and not neighbourhood:
        filtered_df = df2[df2["Country"].isin(Country) & df2["Room_type"].isin(Room_type)]
    elif Country and neighbourhood and  Room_type:
        #filtered_df = df3[df3["Country"].isin(Country) & df3["neighbourhood"].isin(neighbourhood)]
        filtered_df=df4


    l_col,m_col,r_col=st.columns([1,2,1]) 
    with m_col:
        map3d_country(filtered_df,Country)

    
    Price = st.slider("Price Range", float(df4["Price"].min()), float(df4["Price"].max()), (float(df4["Price"].min()), float(df4["Price"].max())))

    filtered_df = filtered_df[(filtered_df['Price'] >= Price[0]) & (filtered_df['Price'] <= Price[1])]

    with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
        first_five_cols = filtered_df.iloc[:, :5]
        every_second_col = filtered_df.iloc[:, 5::2]
        price_column = filtered_df['Price']
        score_column = filtered_df["Review_scores"]

        selected_columns = pd.concat([first_five_cols, every_second_col,price_column,score_column], axis=1,).reset_index(drop=True)
        selected_columns = selected_columns.sort_values(by="Review_scores", ascending=False)

        selected_columns2 =selected_columns.style.background_gradient(cmap="Oranges").format({
            "Total_bedrooms": "{:.0f}",
            "Security_deposit": "{:.2f}",
            "Extra_people": "{:.0f}",
            "Price": "{:.2f}",
            })
        
        st.write(selected_columns2)



    for index, row in selected_columns.iterrows():
        col1, col2 = st.columns(2)
        
        # Display image URL in col1
        with col1:
        

            response = requests.get(row['image_url'])
            if response.status_code == 200:
                st.write("Images") #, use_column_width=True)
            else:
                st.error("Image not found ")   
          


            st.image(row['image_url'], use_column_width=True)
        
        # Display details in col2
        with col2:
            st.subheader(f"{row['Id']} - Review Scores: {selected_columns.loc[index, 'Review_scores']}")
            st.subheader(row['Name'])
            #st.write(f"Listing URL: {row['Listing_url']}")
            st.write(f"Description: {row['Description']}")
            st.write(f"House Rules: {row['House_rules']}")
            #st.write(f"Property Type: {row['Property_type']}")
            st.write(f"Room Type: {row['Room_type']}")
            #st.write(f"Bed Type: {row['Bed_type']}")
            st.write(f"Min Nights: {row['Min_nights']}")
            #st.write(f"Max Nights: {row['Max_nights']}")
            st.write(f"Cancellation Policy: {row['Cancellation_policy']}")
            #st.write(f"Accommodates: {row['Accomodates']}")
            #st.write(f"Total Bedrooms: {row['Total_bedrooms']}")
            #st.write(f"Total Beds: {row['Total_beds']}")
            st.write(f"Availability 365: {row['Availability_365']}")
            st.write(f"Price: {row['Price']}")
            st.write(f"Security Deposit: {row['Security_deposit']}")
            #st.write(f"Cleaning Fee: {row['Cleaning_fee']}")
            #st.write(f"Extra People: {row['Extra_people']}")
            
            
            st.divider()  





def menu_select(SELECT):
    if SELECT == "Home":
        for_home()
    if SELECT == "Search":
        for_search()
    if SELECT == "View":
        for_view()



def streamlit_app():
    st.set_page_config(page_title='Airbnb Analysis',page_icon=Air_icon,layout='wide')
    st.title(':red[ Airbnb Analysis ]')


    SELECT = option_menu(
    menu_title=None,
    options=["Home","Search", "View"],
    icons=["house", "search",  "toggles"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "black", "size": "cover"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", 
                    "--hover-color": "#FF5A5F", "color": "#FF5A5F","font-weight": "bold"},
        "nav-link-selected": {"background-color": "#FF5A5F", "color": "white"}
    } 
    )
    menu_select(SELECT)


streamlit_app()


