import streamlit as st
import pandas as pd
import http.client
import json

# Function to fetch channel details using the channel ID
def fetch_channel_details_by_username(channel_id):
    conn = http.client.HTTPSConnection("yt-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "8e4656bd35msheb88b57c0446250p1e23d5jsna3fbcc47f295",
        'x-rapidapi-host': "yt-api.p.rapidapi.com"
    }

    # Make the API request using the channel ID
    conn.request("GET", f"/channel/search?id={channel_id}&query=cat", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # Decode the response and return JSON
    return json.loads(data.decode("utf-8"))

# Add custom CSS to style the app
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f5;
        }
        .main {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        h3 {
            color: #555;
        }
        .button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .channel-info {
            margin-top: 20px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #f9f9f9;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
st.title("YouTube Subscription Analyzer")
st.markdown('<div class="main">', unsafe_allow_html=True)

# File upload section
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Check if required columns exist
    if 'Channel Title' in df.columns and 'Channel Id' in df.columns:
        # Count the number of subscribed channels
        num_channels = df.shape[0]
        st.write(f"You are subscribed to **{num_channels}** channels.")

        # Create a dropdown for selecting channels
        channel_title_options = df['Channel Title'].unique()
        selected_channel = st.selectbox("Select a Channel", channel_title_options)

        if st.button("Know More", key="know_more"):
            # Get the Channel ID based on the selected channel title
            selected_channel_id = df[df['Channel Title'] == selected_channel]['Channel Id'].values[0]

            # Fetch channel details using the API
            channel_info = fetch_channel_details_by_username(selected_channel_id)

            # Display fetched channel information
            if channel_info and 'meta' in channel_info:
                meta_info = channel_info['meta']
                title = meta_info.get('title', 'N/A')
                description = meta_info.get('description', 'N/A')
                facebookProfileId = meta_info.get('facebookProfileId', 'N/A')
                subscriberCount = meta_info.get('subscriberCount', 'N/A')
                videosCount = meta_info.get('videosCount', 'N/A')

                st.markdown('<div class="channel-info">', unsafe_allow_html=True)
                st.write("### Channel Details:")
                st.write(f"**Title:** {title}")
                st.write(f"**Description:** {description}")
                st.write(f"**Facebook Profile ID:** {facebookProfileId}")
                st.write(f"**Subscriber Count:** {subscriberCount}")
                st.write(f"**Videos Count:** {videosCount}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Could not fetch channel details. Please check the channel ID.")
    else:
        st.error("The CSV file must contain 'Channel Title' and 'Channel Id' columns.")

st.markdown('</div>', unsafe_allow_html=True)