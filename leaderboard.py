import streamlit as st
import pandas as pd
import json
import os

import leaderboardtb
import leaderboardcovid
import streamlit as st
from PIL import Image


PAGES = {
    "TB": leaderboardtb,
    "COVID-19": leaderboardcovid
}

image = Image.open('PokeRad.png')
st.sidebar.image(image)
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

st.sidebar.title("About")
st.sidebar.info(
    """
    PokéRad was developed during 2021 SIIM Hackaton.
    
    Team: Pedro V. Staziaki, Stacy O’Connor, Jane Dimperio, Lillian Spear, Michael Do, Lucas Folio, Marcelo O. Coelho, Eduardo Farina.
    
    Mentor: Les Folio.
    
    Domain expert: Brad Genereaux.
    
    Code-heros: João Santinha, Diego Angulo, Marcelo O. Coelho, Mike Ciancibello, Sivaramakrishnan Rajaraman.
    
    This app was developed and is maintained by João Santinha.
"""
)
