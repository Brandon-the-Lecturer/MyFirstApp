import json
import streamlit as st



def main():
    st.title("NFL-Predictor")

    with open(file="data/nfl_data.json", mode="r") as raw_file:
        raw_data = json.load(raw_file)


    st.selectbox(label="Home Team", options=raw_data["teams"], index=0)
    st.selectbox(label="Away Team", options=raw_data["teams"], index=1)



    return 

if __name__ == "__main__":
    main()


