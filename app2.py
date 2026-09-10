import streamlit as st
import pandas as pd
import altair as alt




st.title("NBA Player Points Dashboard")

df = pd.read_csv("players.csv")


#Reset Button

if "selected_team" not in st.session_state:
    st.session_state.selected_team = "All Teams"
if "search_player" not in st.session_state:
    st.session_state.search_player = ""
if "sort_order" not in st.session_state:
    st.session_state.sort_order = "Highest to Lowest"

def reset_filters():
    st.session_state.selected_team = "All Teams"
    st.session_state.search_player = ""
    st.session_state.sort_order = "Highest to Lowest"

st.button("Reset Filters", on_click=reset_filters)


#Original CSV Data

st.subheader("NBA Player Data")
st.dataframe(df)


#Filter for Teams
st.subheader("Filter by Team")
team_options = ["All Teams"] + sorted(df["Team"].unique().tolist())
selected_team = st.selectbox(
    "Choose a team:",
    team_options,
    key="selected_team"
)
if selected_team == "All Teams":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Team"] == selected_team]



#Filter for Players
st.subheader("Search for a Player")
search_player = st.text_input(
    "Enter player name:",
    key="search_player"
)
if search_player:
    filtered_df = filtered_df[
        filtered_df["Player"].str.contains(
            search_player,
            case=False,
            na=False
        )
    ]


#Filter for Points
st.subheader("Sort by Points")
sort_order = st.selectbox(
    "Choose sorting order:",
    ["Highest to Lowest", "Lowest to Highest"],
    key="sort_order"
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


#Displays final filtered data
st.subheader("Filtered Results")
st.dataframe(
    filtered_df,
    use_container_width=True
)

#Uses metrics to track the filtered data for amount of players and the amount of points the players scored combined 
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(
        "Number of Players",
        len(filtered_df)
    )

with metric_col2:
    st.metric(
        "Total Points",
        filtered_df["Points"].sum()
    )


#Columns for Charts
chart_col1, chart_col2 = st.columns(2)

#Tracks how many times each point total was obtained
with chart_col1:
    st.subheader("Points Distribution")
    points_chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("Points", bin=True),
        y="count()",
        tooltip=["Points", "count()"]
    ).properties(
        width=400,
        height=300
    )
    st.altair_chart(points_chart, use_container_width=True)

#Shows each players point status compared to other players
with chart_col2:
    st.subheader("Top Players by Points")
    top_players_chart = alt.Chart(filtered_df).mark_circle().encode(
        x=alt.X("Player", sort="-y"),
        y=alt.Y("Points", scale=alt.Scale(domain=[0, 115])),
        tooltip=["Player", "Points"]
    ).properties(
        width=400,
        height=300
    )
    st.altair_chart(top_players_chart, use_container_width=True)

