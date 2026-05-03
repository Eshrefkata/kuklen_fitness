import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import random
import os

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="90-Day Fitness Challenge", layout="wide")

# Файл за база данни
DB_FILE = "workout_log.csv"

# Мотивационни цитати
QUOTES = [
    "„Тялото постига това, в което вярва умът.“",
    "„Дисциплината е да правиш това, което трябва, дори когато не искаш.“",
    "„Твоят единствен лимит си ти самият.“",
    "„Не спирай, когато си уморен. Спри, когато си готов.“",
    "„Успехът започва извън зоната ти на комфорт.“"
]

# --- ФУНКЦИИ ЗА ДАННИ ---
def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    return pd.DataFrame(columns=["Date", "Weight", "Workout_Type", "Duration", "Calories", "Protein", "Water"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# --- ИЗЧИСЛЕНИЯ ---
def calculate_bmr(weight, height, age, gender):
    # Формула на Mifflin-St Jeor
    if gender == "Мъж":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# --- ДИЗАЙН И СТРУКТУРА ---
st.title("🏆 90-дневно Фитнес Предизвикателство")
st.info(random.choice(QUOTES))

# Зареждане на текущи данни
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# --- SIDEBAR: ПРОФИЛ ---
with st.sidebar:
    st.header("👤 Потребителски профил")
    age = st.number_input("Години", 14, 100, 25)
    gender = st.radio("Пол", ["Мъж", "Жена"])
    weight_now = st.number_input("Текущо тегло (кг)", 40.0, 200.0, 75.0)
    height = st.number_input("Ръст (см)", 100, 250, 175)
    
    bmr = calculate_bmr(weight_now, height, age, gender)
    tdee = bmr * 1.2 # Базово ниво на активност
    
    st.divider()
    st.metric("BMR (Основна обмяна)", f"{int(bmr)} kcal")
    st.metric("Дневен калориен нужд", f"{int(tdee)} kcal")

# --- ГОРЕН ПАНЕЛ: МЕТРИКИ ---
col1, col2, col3 = st.columns(3)
total_days = len(st.session_state.data['Date'].unique())
remaining_days = max(0, 90 - total_days)
total_cals = st.session_state.data['Calories'].sum()

col1.metric("Текущо тегло", f"{weight_now} кг")
col2.metric("Оставащи дни", f"{remaining_days} / 90")
col3.metric("Изгорени калории (Общо)", f"{int(total_cals)} kcal")

st.divider()

# --- МОДУЛИ: ДНЕВЕН ЛОГ ---
tab1, tab2, tab3 = st.tabs(["📝 Дневен Лог", "📈 Прогрес", "🔥 Heatmap"])

with tab1:
    with st.form("log_form"):
        date_col, type_col = st.columns(2)
        log_date = date_col.date_input("Дата", datetime.date.today())
        workout_type = type_col.selectbox("Тип тренировка", ["Почивка", "Силова", "Кардио", "Йога"])
        
        dur_col, cal_col = st.columns(2)
        duration = dur_col.number_input("Продължителност (мин)", 0, 300, 45)
        calories = cal_col.number_input("Изгорени калории", 0, 2000, 300)
        
        weight_log = st.number_input("Тегло днес (кг)", 40.0, 200.0, weight_now)
        
        p_col, w_col = st.columns(2)
        protein = p_col.checkbox("Приет достатъчно протеин?")
        water = w_col.number_input("Вода (литри)", 0.0, 10.0, 2.0)
        
        submit = st.form_submit_button("Запази записа")
        
        if submit:
            new_entry = {
                "Date": log_date, "Weight": weight_log, "Workout_Type": workout_type,
                "Duration": duration, "Calories": calories, "Protein": protein, "Water": water
            }
            # Обновяване на данните (премахване на дубликат за същата дата)
            df = st.session_state.data
            df = df[df['Date'] != log_date]
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            st.session_state.data = df
            save_data(df)
            st.success("Данните са запазени!")

# --- МОДУЛИ: ТРАКЕР НА ТЕГЛОТО ---
with tab2:
    if not st.session_state.data.empty:
        df_sorted = st.session_state.data.sort_values("Date")
        fig = px.line(df_sorted, x="Date", y="Weight", title="Промяна в теглото",
                      markers=True, line_shape="spline", color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Няма въведени данни за визуализация.")

# --- МОДУЛИ: HEATMAP ПРОГРЕС ---
with tab3:
    st.subheader("Визуален прогрес (90 дни)")
    
    # Генериране на 90-дневна мрежа
    grid_data = []
    types_map = {"Почивка": 0, "Йога": 1, "Кардио": 2, "Силова": 3}
    
    # Попълване на масива за 10 реда х 9 колони
    for i in range(90):
        # Тук симулираме проверка дали има тренировка за ден i от началото
        # В реално приложение ще се сравнява с датата на стартиране
        grid_data.append(random.randint(0, 3)) # Демонстрационни данни
        
    heatmap_array = np.array(grid_data).reshape(9, 10)
    fig_heat = px.imshow(heatmap_array,
                        labels=dict(color="Интензивност"),
                        x=[f"Ден {i+1}" for i in range(10)],
                        y=[f"Седм {i+1}" for i in range(9)],
                        color_continuous_scale="Viridis")
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("0: Почивка | 1: Йога | 2: Кардио | 3: Силова")

# --- ИСТОРИЯ ---
st.subheader("📜 История на тренировките")
st.dataframe(st.session_state.data.sort_values("Date", ascending=False), use_container_width=True)
