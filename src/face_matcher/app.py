import os
from pathlib import Path
from random import randint

import streamlit as st
import torch
from service_layer import registrator

torch.classes.__path__ = []

if "verify" not in st.session_state:
    st.session_state.verify = False

st.title("Система учета рабочего времени")

verify = st.toggle("Регистрация / Верификация")
if verify:
    st.session_state.verify = True
else:
    st.session_state.verify = False

if not st.session_state.verify:
    with st.container():
        reg1, reg2 = st.columns(2)
        with reg1:
            name = st.text_input("Фамилия Имя Отчество")
        with reg2:
            picture = st.camera_input("Фото", disabled=False)
        if name and picture:
            index = randint(0, 100)
            real = registrator.registrate(index=index, name=name, bfile=picture.read())
            if not real:
                st.write("Fake Photo")

if st.session_state.verify:
    with st.container():
        employees = registrator.get_employees()
        if employees:
            mat1, mat2 = st.columns(2)
            with mat1:
                employee_list = [employee.name for employee in employees]
                employee = st.selectbox("Выберите свое имя из списка", employee_list)
                employee_index = employee_list.index(employee)
                employee_path = employees[employee_index].path
                st.write(employee_path)
            with mat2:
                picture = st.camera_input("Фото", disabled=False)
