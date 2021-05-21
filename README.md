# streamlit-leaderboard for PokeRad (SIIM Hackathon 2021)
Make simple and competition leaderboard using streamlit in one file of code!

# Why this is "simple" ?
1. Insert name, upload file, see the result
2. For admin of competition do not need to change the code
3. Does not use a database, just store data inside the text file
4. No password what so ever, even for submit the result, just put username

# How to Use as User
1. Go to the website (usually http://localhost:8501/)
2. insert username
3. Upload and submit
4. See your score and position in leaderboard

# How to Use as Admin
1. Install required packages
2. Run `streamlit run leaderboardTB.py`  for TB Leaderboard
3. Run `streamlit run leaderboardCOVID.py`  for Covid19 Leaderboard

# Setting Ground Truth Data
1. Change username into `admin` (or what ever you desire, can change it inside `leaderboard`)
2. Check the "checkbox" `Change Ground Truth File`
3. Upload `json` file for master data
4. Select index column and target column name
5. click `CHANGE` button
