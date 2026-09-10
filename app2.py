import streamlit as st
import pandas as pd

st.title("NBA Player Points Dashboard")

df = pd.read_csv("players.csv")

st.subheader("NBA Player Data")
st.dataframe(df)

st.subheader("Filter by Team")
team_options = ["All Teams"] + sorted(df["Team"].unique().tolist())
selected_team = st.selectbox(
    "Choose a team:",
    team_options
)
if selected_team == "All Teams":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Team"] == selected_team]

st.subheader("Search for a Player")
search_player = st.text_input(
    "Enter player name:"
)
if search_player:
    filtered_df = filtered_df[
        filtered_df["Player"].str.contains(
            search_player,
            case=False,
            na=False
        )
    ]

st.subheader("Sort by Points")
sort_order = st.selectbox(
    "Choose sorting order:",
    ["Highest to Lowest", "Lowest to Highest"]
)
if sort_order == "Highest to Lowest":
    filtered_df = filtered_df.sort_values(
        by="Points",
        ascending=False
    )
else:
    filtered_df = filtered_df.sort_values(
        by="Points",
        ascending=True
    )

st.subheader("Filtered Results")
st.dataframe(
    filtered_df,
    use_container_width=True
)

st.write(f"Number of results: {len(filtered_df)}")
