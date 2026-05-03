import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import random
import os

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="Fitness Pro 90", page_icon="🔥", layout="wide")

# --- БАЗА ДАННИ И ЛОГИКА ---
DB_FILE = "fitness_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    return pd.DataFrame(columns=["Date", "Weight", "Workout_Type", "Calories", "Completed"])

def calculate_streak(df):
    if df.empty: return 0
    dates = sorted(df[df['Completed'] == True]['Date'].unique(), reverse=True)
    if not dates: return 0
    
    streak = 0
    today = datetime.date.today()
    current_check = today
    
    # Проверка дали последната тренировка е днес или вчера
    if dates[0] < today - datetime.timedelta(days=1):
        return 0
        
    for date in dates:
        if date == current_check or date == current_check - datetime.timedelta(days=1):
            streak += 1
            current_check = date
        else:
            break
    return streak

# --- ЦИТАТИ ---
QUOTES = [
    "„Нищо не е приключило, докато не започнеш да се оправдаваш.“",
    "„Твоето тяло е единственото място, в което си длъжен да живееш.“",
    "„Силните хора не са се родили такива, те са се изградили в залата.“",
    "„Днес е денят, в който ставаш по-добра версия на себе си.“"
]

# --- ДАННИ ---
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# --- HEADER СЕКЦИЯ ---
st.title("🔥 90-Day Transformation Challenge")
st.markdown(f"### *{random.choice(QUOTES)}*")
st.divider()

# --- МЕТРИКИ (DUOLINGO STYLE) ---
streak_count = calculate_streak(st.session_state.data)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"### 🔥 {streak_count} Дни Streak")
    st.caption("Не прекъсвай веригата!")

with col2:
    total_days = len(st.session_state.data)
    st.markdown(f"### 📅 Ден {total_days}/90")
    st.progress(total_days / 90)

with col3:
    last_weight = st.session_state.data['Weight'].iloc[-1] if not st.session_state.data.empty else "--"
    st.markdown(f"### ⚖️ {last_weight} кг")
    st.caption("Последно тегло")

with col4:
    st.markdown("### 🏆 League")
    st.caption("Gold Division")

st.divider()

# --- ОСНОВНО МЕНЮ ---
tab1, tab2, tab3, tab4 = st.tabs(["⚡ AI План", "📝 Дневен Лог", "📊 Прогрес", "⚙️ Профил"])

# --- TAB 1: AI CALISTHENICS PLAN ---
with tab1:
    st.header("🤖 AI Персонализиран План")
    level = st.select_slider("Избери твоето ниво:", options=["Начинаещ", "Среден", "Напреднал"])
    
    plans = {
        "Начинаещ": ["Push-ups (3x10)", "Bodyweight Squats (3x15)", "Plank (3x30s)"],
        "Среден": ["Pull-ups (3x8)", "Diamond Push-ups (3x12)", "Lunges (3x20)"],
        "Напреднал": ["Muscle-ups (3x5)", "Pistol Squats (3x10)", "Hollow Body Hold (3x1min)"]
    }
    
    st.subheader(f"Програма за днес ({level}):")
    for ex in plans[level]:
        st.write(f"✅ {ex}")
    
    st.subheader("📹 Видео инструкции")
    video_cols = st.columns(2)
    video_cols[0].video("https://www.youtube.com/watch?v=iodWzQL7Zno") # Примерно видео
    video_cols[1].video("https://www.youtube.com/watch?v=mGvzVjuY8SY")

# --- TAB 2: LOGGING ---
with tab2:
    with st.form("daily_form"):
        st.subheader("Запиши днешните резултати")
        c1, c2 = st.columns(2)
        weight = c1.number_input("Тегло (кг)", 40.0, 150.0, step=0.1)
        workout = c2.selectbox("Тренировка", ["Calisthenics", "Home Cardio", "Yoga", "Rest"])
        
        calories = st.slider("Изгорени калории", 0, 1500, 300)
        completed = st.checkbox("Завърших тренировката успешно!", value=True)
        
        if st.form_submit_button("Запази деня"):
            new_data = pd.DataFrame([{
                "Date": datetime.date.today(),
                "Weight": weight,
                "Workout_Type": workout,
                "Calories": calories,
                "Completed": completed
            }])
            st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
            st.session_state.data.to_csv(DB_FILE, index=False)
            st.success("Браво! Streak-ът ти е в безопасност!")
            st.balloons()

# --- TAB 3: VISUAL PROGRESS ---
with tab3:
    if not st.session_state.data.empty:
        fig = px.line(st.session_state.data, x="Date", y="Weight", title="Тенденция на теглото", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap
        st.subheader("Активност през периода")
        activity = np.zeros((9, 10)) # 90 дни
        recorded_days = len(st.session_state.data)
        for i in range(recorded_days):
            activity[i // 10, i % 10] = 1
            
        fig_heat = px.imshow(activity, color_continuous_scale='Greens', labels=dict(color="Active"))
        st.plotly_chart(fig_heat)
    else:
        st.warning("Все още нямаш записи. Започни днес!")

# --- TAB 4: PROFILE ---
with tab4:
    st.header("Настройки на профила")
    st.text_input("Име")
    st.number_input("Целно тегло", 40, 150)
    if st.button("Изчисти всички данни"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.experimental_rerun()
