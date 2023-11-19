import json
import requests
import streamlit as st
import pandas as pd

URL = "http://127.0.0.1:8000"
ENDPOINT_DATA = URL + "/data"


def provide_raw_data():
    response = requests.get(url=ENDPOINT_DATA)
    raw_data = response.json()

    with st.expander(label="Raw Data"):
        st.json(raw_data)

    return


def provide_derived_data(raw_data_df):
    raw_data_df = pd.DataFrame(raw_data["games"])

    with st.expander(label="Insights"):
        st.subheader("Home Insights")
        home_stats = raw_data_df.groupby("team")[
            ["points_scored", "points_allowed"]
        ].mean()
        home_stats["team"] = home_stats.index
        home_stats.sort_values("points_scored", ascending=False, inplace=True)
        home_stats.reset_index(drop=True, inplace=True)
        home_stats.index += 1
        st.write(home_stats)

        st.subheader("Away Insights")
        away_stats = raw_data_df.groupby("opponent")[
            ["points_scored", "points_allowed"]
        ].mean()
        away_stats["team"] = away_stats.index
        away_stats.sort_values("points_scored", ascending=False, inplace=True)
        away_stats.reset_index(drop=True, inplace=True)
        away_stats.index += 1
        st.write(away_stats)

    return home_stats, away_stats


def provide_algorithm(raw_data_df):
    with st.expander("Algorithm for Home Advantage"):
        st.markdown(
            """
                    **Heimvorteil sind +3 Punkte im Handicap**  
                    *(Modellierte Annahme)*
                    
                    ---

                    Erklärung:
            
                    Die Schätzung des Heimvorteils in der NFL auf ungefähr 2,5 bis 3 Punkte pro Spiel basiert auf einer Kombination von historischen Daten, Studien und Erfahrungen von Sportanalysten. Es ist wichtig zu beachten, dass dies eine allgemeine Schätzung ist und keine exakte wissenschaftliche Berechnung darstellt. Hier sind einige der Quellen und Grundlagen, auf denen diese Schätzung basiert:

                    - **Historische Daten:** Durch die Analyse von jahrzehntelangen NFL-Spielprotokollen können Sportanalysten Muster erkennen, die darauf hinweisen, dass Teams, die zu Hause spielen, tendenziell bessere Ergebnisse erzielen als bei Auswärtsspielen. Dies kann als Ausgangspunkt für die Schätzung des Heimvorteils dienen.

                    - **Akademische Studien:** Es gibt einige akademische Studien und wissenschaftliche Arbeiten, die den Heimvorteil im Sport, einschließlich der NFL, untersuchen. Diese Studien nutzen statistische Methoden, um den Heimvorteil zu quantifizieren. Obwohl die Ergebnisse variieren können, zeigen viele dieser Studien einen Heimvorteil von etwa 2,5 bis 3 Punkten pro Spiel.

                    - **Erfahrung von Sportanalysten:** Sportexperten und Analysten, die die NFL und andere Sportligen abdecken, bringen ihre Erfahrung und Einsichten in die Schätzung des Heimvorteils ein. Dies kann auf beobachteten Mustern und ihrer Kenntnis der Dynamik von Heim- und Auswärtsspielen basieren.
                    """
        )

        prepared_data_df = raw_data_df.copy()

        condition_1 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] > 3
        condition_2 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] < 0

        prepared_data_df["true wins"] = condition_1 | condition_2

        st.write(prepared_data_df)
    return


def provide_decision_support(home_stats, away_stats, home_team, away_team):
    with st.expander("Metrics for Decision"):
        first_col, second_col = st.columns(2)
        home_scoring_rank = home_stats[home_stats.team == home_team].index[0]
        home_scoring_mean = home_stats[home_stats["team"] == home_team][
            "points_scored"
        ].values[0]
        first_col.metric(label="Home Scoring Mean", value=home_scoring_mean)

        away_scoring_rank = away_stats[away_stats.team == away_team].index[0]
        away_scoring_mean = away_stats[away_stats["team"] == away_team][
            "points_scored"
        ].values[0]
        second_col.metric(label="Away Scoring Mean", value=away_scoring_mean)

        home_allowed_rank = home_stats[home_stats.team == home_team].index[0]
        home_allowed_mean = home_stats[home_stats["team"] == home_team][
            "points_allowed"
        ].values[0]
        first_col.metric(label="Home Allowed Mean", value=home_allowed_mean)

        away_allowed_rank = away_stats[away_stats.team == away_team].index[0]
        away_allowed_mean = away_stats[away_stats["team"] == away_team][
            "points_allowed"
        ].values[0]
        second_col.metric(label="Away Allowed Mean", value=away_allowed_mean)

    return home_scoring_mean, home_allowed_mean, away_scoring_mean, away_allowed_mean


def provide_automated_decision(
    home_scoring_mean,
    home_allowed_mean,
    away_scoring_mean,
    away_allowed_mean,
    home_team,
    away_team,
):
    with st.expander("Prediction"):
        home_pred = (home_scoring_mean + away_allowed_mean) / 2
        away_pred = (away_scoring_mean + home_allowed_mean) / 2

        spread_pred = home_pred - away_pred

        if spread_pred > 0:
            winner = home_team
            spread_pred *= -1

        else:
            winner = away_team
            spread_pred = spread_pred

        st.success(f"{winner} wins with a handicap of {spread_pred} points.")


def main():
    st.title("NFL-Predictor")

    # Level 1
    provide_raw_data()

    # # Level 2
    # home_stats, away_stats = provide_derived_data(raw_data_df=raw_data_df)

    # # Level 3
    # provide_algorithm(raw_data_df=raw_data_df)

    # # Level 4
    # (
    #     home_scoring_mean,
    #     home_allowed_mean,
    #     away_scoring_mean,
    #     away_allowed_mean,
    # ) = provide_decision_support(home_stats, away_stats, home_team, away_team)

    # # Level 5
    # provide_automated_decision(
    #     home_scoring_mean,
    #     home_allowed_mean,
    #     away_scoring_mean,
    #     away_allowed_mean,
    #     home_team,
    #     away_team,
    # )
    return


if __name__ == "__main__":
    main()
