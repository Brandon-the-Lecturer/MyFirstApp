import json
import streamlit as st
import pandas as pd

def provide_raw_data(path):
    with open(file=path, mode="r") as raw_file:
        raw_data = json.load(raw_file)
    
    raw_data_df = pd.DataFrame(raw_data["games"])

    st.selectbox(label="Home Team", options=raw_data["teams"], index=0)
    st.selectbox(label="Away Team", options=raw_data["teams"], index=1)
    
    with st.expander(label="Raw Data"):
        st.json(raw_data)
    
    return raw_data_df


def provide_derived_data(raw_data):
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
    
    return home_stats, away_stats


def provide_algorithm(raw_data_df):
    with st.expander("Algorithm for Home Advantage"):
        st.markdown("""
                    **Heimvorteil sind +3 Punkte im Handicap**  
                    *(Modellierte Annahme)*
                    
                    ---

                    Erklärung:
            
                    Die Schätzung des Heimvorteils in der NFL auf ungefähr 2,5 bis 3 Punkte pro Spiel basiert auf einer Kombination von historischen Daten, Studien und Erfahrungen von Sportanalysten. Es ist wichtig zu beachten, dass dies eine allgemeine Schätzung ist und keine exakte wissenschaftliche Berechnung darstellt. Hier sind einige der Quellen und Grundlagen, auf denen diese Schätzung basiert:

                    - **Historische Daten:** Durch die Analyse von jahrzehntelangen NFL-Spielprotokollen können Sportanalysten Muster erkennen, die darauf hinweisen, dass Teams, die zu Hause spielen, tendenziell bessere Ergebnisse erzielen als bei Auswärtsspielen. Dies kann als Ausgangspunkt für die Schätzung des Heimvorteils dienen.

                    - **Akademische Studien:** Es gibt einige akademische Studien und wissenschaftliche Arbeiten, die den Heimvorteil im Sport, einschließlich der NFL, untersuchen. Diese Studien nutzen statistische Methoden, um den Heimvorteil zu quantifizieren. Obwohl die Ergebnisse variieren können, zeigen viele dieser Studien einen Heimvorteil von etwa 2,5 bis 3 Punkten pro Spiel.

                    - **Erfahrung von Sportanalysten:** Sportexperten und Analysten, die die NFL und andere Sportligen abdecken, bringen ihre Erfahrung und Einsichten in die Schätzung des Heimvorteils ein. Dies kann auf beobachteten Mustern und ihrer Kenntnis der Dynamik von Heim- und Auswärtsspielen basieren.
                    """)
        
        prepared_data_df = raw_data_df.copy()

        condition_1 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] > 3
        condition_2 = raw_data_df["points_scored"] - raw_data_df["points_allowed"] < 0

        prepared_data_df["true wins"] = condition_1 | condition_2
        
        st.write(prepared_data_df)
    return 

def main():

    st.title("NFL-Predictor")

    path = "data/nfl_data.json"

    # Level 1
    raw_data_df = provide_raw_data(path=path)

    # Level 2
    home_stats, away_stats = provide_derived_data(raw_data=raw_data)

    # Level 3
    provide_algorithm(raw_data_df=raw_data_df)


    return 

if __name__ == "__main__":
    main()


