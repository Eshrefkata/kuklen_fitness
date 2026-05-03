import streamlit as st
import random
from PIL import Image
import datetime

# --- КОНФИГУРАЦИЯ НА СТРАНИЦАТА ---
st.set_page_config(page_title="Aylakci", page_icon="🧏‍♂️🫵", layout="wide")

# --- МОТИВАЦИОННИ ЦИТАТИ ---
quotes = [
    "“Ти не спираш, когато си уморен. Спираш, когато си готов!” – Дейвид Гогинс",
    "“Всичко е в главата. Ако не вярваш, че можеш, вече си загубил.” – Макс Верстапен",
    "“Бъди по-неудобен за себе си всеки ден.” – Дейвид Гогинс",
    "“Второто място е просто първото сред губещите.” – Макс Верстапен",
    "“Stay Hard!” – Дейвид Гогинс"
]

# --- ЗАГЛАВИЕ И ЦИТАТ ---
st.title("💪 Фитнес и калистеники")
st.subheader(random.choice(quotes))
st.divider()

# --- СТРАНИЧНА ЛЕНТА (SIDEBAR) - НАСТРОЙКИ ---
st.sidebar.header("⚙️ Лични настройки")
gender = st.sidebar.radio("Пол", ["Мъж", "Жена"])
weight = st.sidebar.number_input("Тегло (кг)", min_value=40, max_value=200, value=80)
height = st.sidebar.number_input("Ръст (см)", min_value=120, max_value=220, value=180)
goal = st.sidebar.selectbox("Цел", ["Отслабване", "Поддържане", "Мускулна маса"])
workout_type = st.sidebar.selectbox("Тип тренировка", ["Калистеника", "Фитнес зала", "Кардио"])


# --- ОСНОВНИ РАЗДЕЛИ ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🥗 Диета", 
    "🏋️ Тренировка", 
    "📸 Калориен скенер", 
    "📈 Прогрес", 
    "🤖 Чат с Гогинс"
])

# --- РАЗДЕЛ 1: ПЛАН ЗА ДИЕТА ---
with tab1:
    st.header("🍎 Твоят хранителен план")
    # Базова формула за BMR (Mifflin-St Jeor)
    bmr = 10 * weight + 6.25 * height - 5 * 25 # Приемаме средна възраст 25
    if gender == "Мъж": bmr += 5
    else: bmr -= 161
    
    st.metric("Дневен калориен прием (Base)", f"{int(bmr)} kcal")
    
    col1, col2, col3 = st.columns(3)
    col1.write("**Протеини**")
    col1.info(f"{weight * 2}г")
    col2.write("**Въглехидрати**")
    col2.info(f"{weight * 3}г")
    col3.write("**Мазнини**")
    col3.info(f"{weight * 0.8:.1f}г")

# --- РАЗДЕЛ 2: ТРЕНИРОВЪЧЕН ПЛАН ---
with tab2:
    st.header(f"📅 План: {workout_type}")
    if workout_type == "Калистеника":
        st.write("- **Понеделник:** Лицеви опори и кофички (5 серии по 20)")
        st.write("- **Вторник:** Клекове и напади (4 серии по 20)")
        st.write("- **Сряда:** Набирения (5 серии по 20)")
        st.write("- **Четвъртък:** Коремни преси (4 серии по макс)")
    else:
        st.write("Генериране на план за фитнес зала...")
        st.table({"Упражнение": ["Лежанка", "Мъртва тяга", "Клек"], "Серии": [4, 3, 4], "Повторения": ["8-10", "5", "10"]})

# --- РАЗДЕЛ 3: КАЛОРИЕН СКЕНЕР ---
with tab3:
    st.header("📸 Снимай храната си")
    img_file = st.camera_input("Направи снимка на продукта")
    if img_file:
        st.image(img_file)
        st.warning("⚠️ Интегрирайте Vision API (Gemini/OpenAI), за да анализирате реално калориите.")
        st.info("Прогноза (демо): ~250 kcal (Ябълка/Снак)")

# --- РАЗДЕЛ 4: СРАВНЕНИЕ НА ПРОГРЕСА ---
with tab4:
    st.header("📈 Преди и Сега")
    col_left, col_right = st.columns(2)
    
    with col_left:
        file_before = st.file_uploader("Снимка Преди", type=['jpg', 'png'])
        if file_before: st.image(file_before, caption="Преди")
        
    with col_right:
        file_after = st.file_uploader("Снимка Сега", type=['jpg', 'png'])
        if file_after: st.image(file_after, caption="Сега")

# --- РАЗДЕЛ 5: ВИРТУАЛЕН АСИСТЕНТ (ГОГИНС) ---
with tab5:
    st.header("🤖 Дейвид Гогинс Асистент")
    st.write("*„Не ме интересува дали си уморен. Ставай!“*")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Кажи нещо на Гогинс..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Симулиран отговор в стил Гогинс
            responses = [
                f"Защо се оплакваш? {prompt} не е извинение! STAY HARD!",
                "Ти си в комфортната си зона. Излез от там!",
                "Кой ще пренесе лодките?! ТИ ЛИ?!",
                "Болката е най-добрият учител. Не спирай!"
            ]
            response = random.choice(responses)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
