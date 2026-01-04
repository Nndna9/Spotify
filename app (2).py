
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Spotify Dashboard",
    page_icon="🎧",
    layout="wide"
)

# --- THEME ---
st.markdown(
    """
    <style>
    body {background-color: #000000; color: white;}
    .stApp {background-color: #000000;}
    h1, h2, h3 {color: #1DB954;}
    </style>
    """, unsafe_allow_html=True
)

# --- ANIMATED INTRO ---
st.markdown(
    """
    <h1 style='text-align:center;'>🎵 Spotify Insights Dashboard</h1>
    <p style='text-align:center;'>✨ Data. Beats. Insights. ✨</p>
    """, unsafe_allow_html=True
)

df = pd.read_csv("spotify.csv")

# --- GLOBAL FILTERS ---
st.sidebar.header("🎚️ Filters")
genre = st.sidebar.multiselect("Genre", df["Genre"].unique(), df["Genre"].unique())
market = st.sidebar.selectbox("Market", ["All"] + list(df["Market"].unique()))

filtered = df[df["Genre"].isin(genre)]
if market != "All":
    filtered = filtered[filtered["Market"] == market]

# --- KPI METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Plays", f"{filtered['Plays'].sum():,}")
col2.metric("Total Likes", f"{filtered['Likes'].sum():,}")
col3.metric("Playlist Adds", f"{filtered['Playlist_Adds'].sum():,}")

st.markdown("### 🔍 Key Insights")

st.write("1️⃣ **Pop dominates plays**, proving mainstream genres still rule streaming culture.")
st.write("2️⃣ **High playlist adds strongly boost plays**, highlighting editorial power.")
st.write("3️⃣ **Global tracks outperform local**, showing wider audience reach.")
st.write("4️⃣ **The Weeknd leads in engagement**, blending pop with mass appeal.")
st.write("5️⃣ **Hip-Hop shows high loyalty**, with strong likes-to-plays ratio.")
st.write("6️⃣ **K-Pop has fewer songs but massive plays**, fandom power matters.")
st.write("7️⃣ **Bollywood performs best locally**, cultural relevance wins.")
st.write("8️⃣ **Alternative music has high engagement**, niche but loyal listeners.")
st.write("9️⃣ **More likes = more streams**, emotional connection drives replays.")
st.write("🔟 **Market filtering changes insights**, proving segmentation is crucial.")

# --- CHARTS ---
c1, c2 = st.columns(2)

with c1:
    fig1 = px.bar(
        filtered,
        x="Artist",
        y="Plays",
        color="Genre",
        title="🎤 Plays by Artist"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.pie(
        filtered,
        values="Plays",
        names="Genre",
        title="🎧 Genre Share of Plays"
    )
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(
    filtered,
    x="Likes",
    y="Plays",
    color="Genre",
    size="Playlist_Adds",
    title="💚 Likes vs Plays (Bigger = More Playlist Adds)",
    hover_data=["Artist", "Song"]
)

st.plotly_chart(fig3, use_container_width=True)
