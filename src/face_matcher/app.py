import os
from pathlib import Path
from random import randint

import streamlit as st
import torch
from service_layer import registrator

torch.classes.__path__ = []


st.title("Система учета рабочего времени")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Фамилия Имя Отчество")
with col2:
    picture = st.camera_input("Фото", disabled=False)
if name and picture:
    index = randint(0, 100)
    registrator.registrate(index=index, name=name, bfile=picture.read())
    st.session_state.registration = "registration"
