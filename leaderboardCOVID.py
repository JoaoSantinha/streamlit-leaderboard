"covid27_les_ground_truth.json"
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import dicescoring
import numpy as np
import io


# from sklearn.metrics import (accuracy_score, auc, f1_score, precision_score, recall_score,
#                             mean_absolute_error, mean_squared_error, r2_score)
st.set_option('deprecation.showfileUploaderEncoding', False)

# funtions
def relative_time(t_diff):
    days, seconds = t_diff.days, t_diff.seconds
    if days > 0:
        return f"{days}d"
    else:
        hours = t_diff.seconds // 3600
        minutes = t_diff.seconds // 60
        if hours >0 : #hour
            return f"{hours}h"
        elif minutes >0:
            return f"{minutes}m"
        else:
            return f"{seconds}s"

def get_leaderboard_dataframe(csv_file = 'leaderboardCOVID.csv', greater_is_better = True):
    df_leaderboard = pd.read_csv('leaderboardCOVID.csv', header = None)
    df_leaderboard.columns = ['Username', 'Score', 'Submission Time']
    df_leaderboard['counter'] = 1
    df_leaderboard = df_leaderboard.groupby('Username').agg({"Score": "max",
                                                            "counter": "count",
                                                            "Submission Time": "max"})
    df_leaderboard = df_leaderboard.sort_values("Score", ascending = not greater_is_better)
    df_leaderboard = df_leaderboard.reset_index()
    df_leaderboard.columns = ['Username','Score', 'Entries', 'Last']
    df_leaderboard['Last'] = df_leaderboard['Last'].map(lambda x: relative_time(datetime.now() - datetime.strptime(x, "%Y%m%d_%H%M%S")))
    return df_leaderboard

# Title
st.title("Covid-19 Competition Leaderboard")

# Username Input
username = st.text_input("Username", value = "Joao", max_chars= 20,)
username = username.replace(",","") # for storing csv purpose
st.header(f"Hi {username} !!!")

# Check if master data has been registered:
master_files = os.listdir('master')
if ("covid27_les_ground_truth.json" not in master_files):
    st.text("Admin please insert ground truth data")
else:
    greater_is_better = True

    uploaded_file = st.file_uploader("Upload Submission json File", type='json')
    groud_truth_file = 'master/covid27_les_ground_truth.json'
    if st.button("SUBMIT"):
        if uploaded_file is None:
            st.text("UPLOAD FIRST")
        else:
            # save submission
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            json_uploaded_submission = json.load(stringio)
            datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
            datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_submission = f"submission/sub_{username}__{datetime_now}.json"
            with open(filename_submission, 'w') as outfile:
                json.dump(json_uploaded_submission, outfile)
            dice_scores_user = dicescoring.dice_list(groud_truth_file, uploaded_file)
            score = round(np.sum(np.asarray(dice_scores_user)) * 10)
            score = round(score,5)
            st.text(f"YOUR Dice socer: {score}")
            # save score
            with open("leaderboardCOVID.csv", "a+") as leaderboard_csv:
                leaderboard_csv.write(f"{username},{score},{datetime_now}\n")

    # Showing Leaderboard
    st.header("Leaderboard")
    if os.stat("leaderboardCOVID.csv").st_size == 0:
        st.text("NO SUBMISSION YET")
    else:
        df_leaderboard = get_leaderboard_dataframe(csv_file = 'leaderboardCOVID.csv', greater_is_better = greater_is_better)
        st.write(df_leaderboard)

# To register master data
if username == 'admin': # CHANGE HERE AS YOU WANT
    change_master_key = st.checkbox('Change Ground Truth File')

    if change_master_key:
        # Master Ground Truth
        uploaded_file_master = st.file_uploader("Upload Ground Truth File", type='json')
        if uploaded_file_master is not None:
            # Change the master dataset
            # 'master/via_project_9Dec2020_15h40m_Les_ground_truth.json'
            stringio = io.StringIO(uploaded_file_master.getvalue().decode("utf-8"))
            json_uploaded_submission_master = json.load(stringio)
            datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open('master/covid27_les_ground_truth.json', 'w') as outfile:
                json.dump(json_uploaded_submission_master, outfile)
