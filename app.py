import streamlit as st

st.set_page_config(page_title="Fitness & Diet Planner", layout="wide")

# --- СТРАНИЧНА ЛЕНТА: ДАННИ ---
st.sidebar.header("📋 Твоите параметри")
weight = st.sidebar.number_input("Тегло (кг):", 40.0, 200.0, 75.0)
height = st.sidebar.number_input("Ръст (см):", 120, 230, 175)
age = st.sidebar.number_input("Години:", 15, 90, 25)
gender = st.sidebar.radio("Пол:", ["Мъж", "Жена"])
activity = st.sidebar.selectbox("Активност:", ["Ниска", "Умерена", "Висока"])
goal = st.sidebar.selectbox("Цел:", ["Отслабване", "Поддържане", "Маса"])
training_pref = st.sidebar.radio("Тип тренировки:", ["Фитнес", "Калистеника"])

# --- ИЗЧИСЛЕНИЯ ---
# BMR (Mifflin-St Jeor)
if gender == "Мъж":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# TDEE
act_mult = {"Ниска": 1.2, "Умерена": 1.55, "Висока": 1.75}
tdee = bmr * act_mult[activity]

# Target Calories
if goal == "Отслабване":
    target_cal = tdee - 500
elif goal == "Маса":
    target_cal = tdee + 400
else:
    target_cal = tdee

# --- ГЛАВНО ТАБЛО ---
st.title("💪 Персонален План")

col1, col2, col3 = st.columns(3)
col1.metric("BMR (Базов метаболизъм)", f"{int(bmr)} kcal")
col2.metric("TDEE (Разход)", f"{int(tdee)} kcal")
col3.metric("Целеви калории", f"{int(target_cal)} kcal", delta=int(target_cal - tdee))

st.divider()

# --- ДИЕТА ---
st.header("🥗 Диетичен план")
p = (target_cal * 0.3) / 4
c = (target_cal * 0.45) / 4
f = (target_cal * 0.25) / 9

st.write(f"За постигане на целта (**{goal}**), се стреми към следните макроси:")
st.table({
    "Протеини (г)": [int(p)],
    "Въглехидрати (г)": [int(c)],
    "Мазнини (г)": [int(f)]
})

# --- ТРЕНИРОВКА ---
st.header(f"🏋️ Тренировъчен режим: {training_pref}")

if training_pref == "Фитнес":
    st.markdown("""
    - **Ден 1:** Гърди, Рамене, Трицепс (Бутащи)
    - **Ден 2:** Гръб, Бицепс (Дърпащи)
    - **Ден 3:** Крака и Корем
    - *Почивка и повторение*
    """)
else:
    st.markdown("""
    - **Ден 1:** Набирания, Кофички, Лицеви опори
    - **Ден 2:** Клякания, Напади, Повдигане на крака (корем)
    - **Ден 3:** Стойка на ръце, Планкове, Експлозивни движения
    - *Почивка и повторение*
    """)

st.info("Забележка: Данните са изчислени по стандартни формули. Слушай тялото си!")
