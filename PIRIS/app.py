import streamlit as st
import pandas as pd
from datetime import datetime
from database import init_db, add_account, check_account, get_account, check_username_exists, check_passport_number_exists, check_id_number_exists, get_all_accounts

def app():
    init_db()
    st.title("Банковская Система")

    menu = ["Регистрация", "Вход", "Поиск пользователя", "Список пользователей"]
    choice = st.sidebar.selectbox("Меню", menu)

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if choice == "Регистрация":
        st.subheader("Регистрация нового пользователя")
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type='password')
        surname = st.text_input("Фамилия")
        name = st.text_input("Имя")
        patronymic = st.text_input("Отчество")
        birth_date = st.date_input("Дата рождения",min_value=datetime(1800,1,1), value=datetime(2024,1,1))
        gender = st.selectbox("Пол", ["Мужской", "Женский"])
        passport_series = st.text_input("Серия паспорта")
        passport_number = st.text_input("Номер паспорта")
        passport_issued_by = st.text_input("Кем выдан паспорт")
        passport_issue_date = st.date_input("Дата выдачи паспорта",min_value=datetime(1800,1,1), value=datetime(2024,1,1))
        id_number = st.text_input("Идентификационный номер")
        birth_place = st.text_input("Место рождения")
        registration_city = st.selectbox("Город фактического проживания",["Минск","Гродно","Могилев","Брест","Витебск"])
        current_address = st.text_input("Текущий адрес проживания")
        phone_home = st.text_input("Телефон Домашний")
        phone_mobile = st.text_input("Телефон Мобильный")
        email = st.text_input("Email")
        residencecity = st.selectbox("Город прописки",["Минск","Гродно","Могилев","Брест","Витебск"])
        residenceaddress = st.text_input("Адресс прописки")
        marital_status = st.selectbox("Семейное положение", ["Холост (не замужем)", "Женат (замужем)", "Разведен (разведена)", "Вдовец (вдова)"]) 
        citizenship = st.selectbox("Гражданство",["Беларусь","Российская Федерация","Узбекистан"])
        disability = st.selectbox("Инвалидность",["Нет","Да"])
        pensioner = st.checkbox("Пенсионер")
        if st.button("Зарегистрироваться"):
            if check_username_exists(username):
                st.error("Имя пользователя уже существует")
            elif check_passport_number_exists(passport_number):
                st.error("Номер паспорта уже существует")
            elif check_id_number_exists(id_number):
                st.error("Идентификационный номер уже существует")
            elif not all([username, password, surname, name, patronymic, passport_series, passport_number, passport_issued_by, id_number, birth_place, registration_city, current_address, phone_home, phone_mobile, email, citizenship]):
                st.error("Все поля должны быть заполнены")
            elif any(not item.isalpha() for item in [surname, name, patronymic]):
                st.error("Фамилия, имя и отчество должны содержать только буквы")
            else:
                add_account(username, password, surname, patronymic, birth_date, gender, passport_series, passport_number, passport_issued_by, passport_issue_date, id_number, birth_place, registration_city, current_address, phone_home, phone_mobile, email, residencecity, residenceaddress, marital_status, citizenship, disability, pensioner)
                st.success("Аккаунт успешно зарегистрирован")

    elif choice == "Вход":
        if st.session_state["logged_in"]:
            st.subheader("Личный кабинет")
            account = get_account(st.session_state["username"])
            st.write(f"Имя пользователя: {account[0]}")
            st.write(f"Фамилия: {account[2]}")
            st.write(f"Имя: {account[3]}")
            st.write(f"Отчество: {account[4]}")
            st.write(f"Дата рождения: {account[5]}")
            st.write(f"Пол: {account[6]}")
            st.write(f"Серия паспорта: {account[7]}")
            st.write(f"Номер паспорта: {account[8]}")
            st.write(f"Кем выдан паспорт: {account[9]}")
            st.write(f"Дата выдачи паспорта: {account[10]}")
            st.write(f"Идентификационный номер: {account[11]}")
            st.write(f"Место рождения: {account[12]}")
            st.write(f"Город фактического проживания: {account[13]}")
            st.write(f"Текущий адрес проживания: {account[14]}")
            st.write(f"Телефон домашний: {account[15]}")
            st.write(f"Телефон мобильный: {account[16]}")
            st.write(f"Email: {account[17]}")
            st.write(f"Город прописки: {account[18]}")
            st.write(f"Адресс прописки: {account[19]}")
            st.write(f"Семейное положение: {account[20]}")
            st.write(f"Гражданство: {account[21]}")
            st.write(f"Инвалидность: {account[22]}")
            st.write(f"Пенсионер: {account[23]}")

            if st.button("Выйти"):
                st.session_state["logged_in"] = False
        else:
            st.subheader("Вход в систему")
            username = st.text_input("Имя пользователя")
            password = st.text_input("Пароль", type='password')
            if st.button("Войти"):
                if check_account(username, password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success("Успешный вход в систему")
                else:
                    st.error("Неверное имя пользователя или пароль")

    elif choice == "Поиск аккаунта":
        st.subheader("Поиск пользователя")
        username = st.text_input("Имя пользователя")
        if st.button("Поиск"):
            account = get_account(username)
            if account:
                st.write(f"Пользователь найден: {account[0]}")
            else:
                st.error("Пользователь не найден")

    elif choice == "Список пользователей":
        st.subheader("Список пользователей")
        accounts = get_all_accounts()
        for account in accounts:
            st.write(account[0])
            

if __name__ == "__main__":
    app()
