import json
import streamlit as st
import pandas as pd

def provide_raw_data():
    with open(file="data/nfl_data.json", mode="r") as raw_file:
        raw_data = json.load(raw_file)
    
    with st.expander(label="Raw Data"):
        st.json(raw_data)
    
    return raw_data


def provide_derived_data(df: pd.DataFrame) -> None:
    with st.expander(label="Insights"):

        st.subheader("Home Insights")
        home_stats = df.groupby("team")[["points_scored", "points_allowed"]].mean()
        home_stats["team"] = home_stats.index
        home_stats.sort_values("points_scored", ascending=False, inplace=True)
        home_stats.reset_index(drop=True, inplace=True)
        home_stats.index += 1
        st.write(home_stats)
    
        st.subheader("Away Insights")
        away_stats = df.groupby("opponent")[["points_scored", "points_allowed"]].mean()
        away_stats["team"] = away_stats.index
        away_stats.sort_values("points_scored", ascending=False, inplace=True)
        away_stats.reset_index(drop=True, inplace=True)
        away_stats.index += 1
        st.write(away_stats)
    


    return

def main():
    st.title("NFL-Predictor")

    with open(file="data/nfl_data.json", mode="r") as raw_file:
        raw_data = json.load(raw_file)

    raw_data_df = pd.DataFrame(raw_data["games"])

    st.selectbox(label="Home Team", options=raw_data["teams"], index=0)
    st.selectbox(label="Away Team", options=raw_data["teams"], index=1)

    # Level 1
    provide_raw_data(data=raw_data)

    # Level 2
    provide_derived_data(df=raw_data_df)




    return 

if __name__ == "__main__":
    main()


