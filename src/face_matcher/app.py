import os
from pathlib import Path
from random import randint

import streamlit as st
import torch
from service_layer import matcher, registrator

torch.classes.__path__ = []

if "verify" not in st.session_state:
    st.session_state.verify = False

st.title("Система учета рабочего времени")

verify = st.toggle("Регистрация / Верификация")
placeholder = st.empty()
if verify:
    reg_picture = None
    st.session_state.verify = True
    placeholder.empty()
else:
    ver_picture = None
    st.session_state.verify = False
    placeholder.empty()

if not st.session_state.verify:
    with placeholder.container():
        reg1, reg2 = st.columns(2)
        with reg1:
            name = st.text_input("Фамилия Имя Отчество")
        with reg2:
            reg_picture = st.camera_input("Фото", disabled=st.session_state.verify)
        if name and reg_picture:
            index = randint(0, 100)
            real = registrator.registrate(index=index, name=name, bfile=reg_picture.read())
            if not real:
                st.error("Поддельное фото!")

if st.session_state.verify:
    with placeholder.container():
        employees = registrator.get_employees()
        if employees:
            mat1, mat2 = st.columns(2)
            with mat1:
                employee_list = [employee.name for employee in employees]
                employee = st.selectbox("Выберите свое имя из списка", employee_list)
                employee_index = employee_list.index(employee)
                path = employees[employee_index].path
            with mat2:
                ver_picture = st.camera_input("Фото", disabled=not st.session_state.verify)
            if path and ver_picture:
                result = matcher.match(path, ver_picture.read())
                if result.fake:
                    st.error("Поддельное фото!")
                if result.access:
                    st.success("Допущен к работе!", icon="✅")
                else:
                    st.error("Не допущен к работе!", icon="🚨")
