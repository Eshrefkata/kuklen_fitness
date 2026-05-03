import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import random
import os

# --- CONFIG ---
st.set_page_config(page_title="Fitness Pro 90", page_icon="💪", layout="wide")

# Custom CSS за модерен вид
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 15px; border: 1px solid #3e4250; }
    .exercise-card { 
        background-color: #262730; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #FF4B4B;
        margin-bottom: 20px;
    }
    .quote-box {
        font-style: italic;
        color: #9EA0A5;
        text-align: center;
        padding: 10px;
        border-bottom: 1px solid #3e4250;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
DB_FILE = "fitness_data_v2.csv"

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    return pd.DataFrame(columns=["Date", "Weight", "Workout", "Cals", "Done"])

def get_streak(df):
    if df.empty: return 0
    dates = sorted(df[df['Done'] == True]['Date'].unique(), reverse=True)
    if not dates or dates[0] < datetime.date.today() - datetime.timedelta(days=1): return 0
    streak = 0
    curr = dates[0]
    for d in dates:
        if d == curr or d == curr - datetime.timedelta(days=1):
            streak += 1
            curr = d
        else: break
    return streak

# --- UI HEADER ---
st.title("🏆 Fitness Pro 90")
quotes = ["„Единствената лоша тренировка е тази, която не се е състояла.“", 
          "„Успехът е сумата от малки усилия, повтаряни ден след ден.“"]
st.markdown(f"<div class='quote-box'>{random.choice(quotes)}</div>", unsafe_allow_html=True)

if 'db' not in st.session_state:
    st.session_state.db = load_data()

# --- DUOLINGO STYLE METRICS ---
m1, m2, m3, m4 = st.columns(4)
current_streak = get_streak(st.session_state.db)
m1.metric("🔥 STREAK", f"{current_streak} ДНИ")
m2.metric("📅 ПРОГРЕС", f"{len(st.session_state.db)}/90 Дни")
m3.metric("⚖️ ТЕГЛО", f"{st.session_state.db['Weight'].iloc[-1] if not st.session_state.db.empty else '--'} кг")
m4.metric("⚡ НИВО", "Калистеника")

st.divider()

# --- MAIN NAVIGATION ---
tabs = st.tabs(["🚀 Днешна Тренировка", "📊 Анализи", "📂 База Данни", "⚙️ Настройки"])

# --- TAB 1: AI PLAN & VIDEOS ---
with tabs[0]:
    st.header("🤖 Твоят AI План за Днес")
    lvl = st.select_slider("Ниво на трудност:", options=["Начинаещ", "Напреднал"])
    
    # Структурирана библиотека с упражнения
    workouts = {
        "Начинаещ": [
            {"name": "Лицеви опори (Push-ups)", "reps": "3 серии x 10", "vid": "https://www.youtube.com/watch?v=iodWzQL7Zno"},
            {"name": "Клякания (Squats)", "reps": "3 серии x 15", "vid": "https://www.youtube.com/watch?v=mGvzVjuY8SY"},
            {"name": "Планк (Plank)", "reps": "3 серии x 30 сек", "vid": "https://www.youtube.com/watch?v=ASdvN_XEl_c"}
        ],
        "Напреднал": [
            {"name": "Набирания (Pull-ups)", "reps": "4 серии x 8", "vid": "https://www.youtube.com/watch?v=eGo4IYlbE5g"},
            {"name": "Диамантени опори", "reps": "3 серии x 12", "vid": "https://www.youtube.com/watch?v=6dZHZ0_RPhw"},
            {"name": "L-sit Hold", "reps": "3 серии x 15 сек", "vid": "https://www.youtube.com/watch?v=IuZGoU6KSt4"}
        ]
    }

    # Показване на упражненията в карти с видео
    for ex in workouts[lvl]:
        with st.container():
            col_info, col_vid = st.columns([1, 1.5])
            with col_info:
                st.markdown(f"""<div class='exercise-card'>
                    <h3>{ex['name']}</h3>
                    <p><b>Цел:</b> {ex['reps']}</p>
                </div>""", unsafe_allow_html=True)
                st.write("Прочети инструкциите под видеото за правилна форма.")
            with col_vid:
                st.video(ex['vid'])
            st.divider()

# --- TAB 2: LOGGING & PROGRESS ---
with tabs[1]:
    col_log, col_chart = st.columns([1, 2])
    
    with col_log:
        st.subheader("📝 Лог на деня")
        with st.form("log_form", clear_on_submit=True):
            w_val = st.number_input("Тегло днес", 40.0, 150.0, step=0.1)
            type_val = st.selectbox("Активност", ["Калистеника", "Кардио", "Почивка"])
            cal_val = st.number_input("Калории", 0, 1000, 250)
            is_done = st.checkbox("Завършена тренировка", value=True)
            if st.form_submit_button("Запиши"):
                new_row = pd.DataFrame([{"Date": datetime.date.today(), "Weight": w_val, "Workout": type_val, "Cals": cal_val, "Done": is_done}])
                st.session_state.db = pd.concat([st.session_state.db, new_row], ignore_index=True)
                st.session_state.db.to_csv(DB_FILE, index=False)
                st.balloons()
                st.rerun()

    with col_chart:
        st.subheader("📈 Графика на теглото")
        if not st.session_state.db.empty:
            fig = px.area(st.session_state.db, x="Date", y="Weight", color_discrete_sequence=['#FF4B4B'])
            st.plotly_chart(fig, use_container_width=True)

# --- TAB 3: DATA VIEW ---
with tabs[2]:
    st.subheader("📁 История на всички записи")
    st.dataframe(st.session_state.db.sort_values("Date", ascending=False), use_container_width=True)
    
    # Heatmap visualization
    st.subheader("🔥 Календар на активността")
    if not st.session_state.db.empty:
        # Simple dot-map of activity
        days = ["Пон", "Вт", "Ср", "Чет", "Пет", "Съб", "Нед"]
        activity_data = [1 if i < len(st.session_state.db) else 0 for i in range(90)]
        # Тук може да се добави по-сложен Heatmap, ако има дати за всички 90 дни

# --- TAB 4: SETTINGS ---
with tabs[3]:
    st.header("⚙️ Управление на профила")
    if st.button("🚨 ИЗТРИЙ ЦЕЛИЯ ПРОГРЕС", help="Внимавай! Това ще изтрие CSV файла."):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.session_state.db = load_data()
            st.rerun()

# --- DISCLAIMER ---
st.caption("⚠️ Консултирайте се с лекар преди започване на интензивна тренировъчна програма.")
