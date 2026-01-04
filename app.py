import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit_lottie import st_lottie
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Spotify Insights",
    page_icon="🎧",
    layout="wide"
)

# ---------------- THEME / CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: white;
}
h1, h2, h3 {
    color: #1DB954;
}
.stMetric {
    background-color: #121212;
    border-radius: 14px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOTTIE LOADER ----------------
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_music = load_lottie(
    "https://assets10.lottiefiles.com/packages/lf20_touohxv0.json"
)

lottie_headphones = load_lottie(
    "https://assets3.lottiefiles.com/packages/lf20_2glqweqs.json"
)

# ---------------- HERO SECTION ----------------
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    <h1>Spotify Insights Dashboard</h1>
    <h4>🎶 Music • Data • Culture</h4>
    <p style="opacity:0.8">
    Discover how listeners engage, what genres dominate,
    and why playlists decide the charts.
    </p>
    """, unsafe_allow_html=True)

with col2:
    st_lottie(lottie_music, height=220)

st.divider()

# ---------------- LOAD DATA ----------------
df = pd.read_csv("spotify.csv")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🎛️ Filters")

genre_filter = st.sidebar.multiselect(
    "Select Genre",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()
)

market_filter = st.sidebar.selectbox(
    "Market",
    options=["All"] + list(df["Market"].unique())
)

filtered = df[df["Genre"].isin(genre_filter)]
if market_filter != "All":
    filtered = filtered[filtered["Market"] == market_filter]

# ---------------- KPIs ----------------
k1, k2, k3 = st.columns(3)

k1.metric("🎧 Total Plays", f"{filtered['Plays'].sum():,}")
k2.metric("💚 Total Likes", f"{filtered['Likes'].sum():,}")
k3.metric("📌 Playlist Adds", f"{filtered['Playlist_Adds'].sum():,}")

# ---------------- INSIGHTS ----------------
st.markdown("## 🔍 Key Insights")

insights = [
    "Pop dominates total plays — mainstream genres still rule streaming.",
    "Playlist adds directly boost plays — editorial power matters.",
    "Global tracks outperform local — reach changes everything.",
    "Hip-Hop shows strong loyalty via likes-to-play ratio.",
    "K-Pop proves fandom > volume — fewer songs, massive plays.",
    "Bollywood thrives locally — cultural connection wins.",
    "Alternative music has niche but high engagement.",
    "More likes strongly correlate with repeat streams.",
    "Artists with playlists grow faster than viral-only hits.",
    "Market filters completely change rankings — segmentation is key."
]

for i, insight in enumerate(insights, start=1):
    st.write(f"**{i}.** {insight}")

# ---------------- CHART LOADING EFFECT ----------------
with st.spinner("Tuning the beats... 🎶"):
    time.sleep(1)

# ---------------- CHARTS ----------------
st.markdown("## 📊 Visual Insights")

c1, c2 = st.columns(2)

# ---- Animated Horizontal Bar ----
with c1:
    fig1 = px.bar(
        filtered.sort_values("Plays"),
        x="Plays",
        y="Artist",
        orientation="h",
        color="Genre",
        animation_frame="Market",
        title="🎤 Artist Popularity (Animated by Market)",
        hover_data=["Song", "Likes", "Playlist_Adds"]
    )

    fig1.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ---- Pie Chart ----
with c2:
    fig2 = px.pie(
        filtered,
        values="Plays",
        names="Genre",
        title="🎧 Genre Share of Plays"
    )

    fig2.update_layout(
        paper_bgcolor="black",
        font_color="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---- Glow Scatter ----
fig3 = px.scatter(
    filtered,
    x="Likes",
    y="Plays",
    size="Playlist_Adds",
    color="Genre",
    hover_name="Song",
    hover_data=["Artist"],
    title="💚 Engagement Galaxy (Size = Playlist Adds)"
)

fig3.update_traces(
    marker=dict(
        line=dict(width=1, color="white"),
        opacity=0.85
    )
)

fig3.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white"
)

st.plotly_chart(fig3, use_container_width=True)

# ---- Radar Chart ----
genre_stats = filtered.groupby("Genre")[["Likes","Plays","Playlist_Adds"]].mean().reset_index()

fig4 = px.line_polar(
    genre_stats,
    r="Plays",
    theta="Genre",
    line_close=True,
    title="🎼 Genre Power Radar"
)

fig4.update_layout(
    polar=dict(bgcolor="black"),
    paper_bgcolor="black",
    font_color="white"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- FOOTER ----------------
st.divider()
st_lottie(lottie_headphones, height=120)
st.caption("Built with 💚 using Streamlit + Plotly | Spotify-inspired dashboard")
