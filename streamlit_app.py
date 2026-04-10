import streamlit as st
import requests
import time

# Настройка страницы
st.set_page_config(
    page_title="Ветеринарная математика | МВА им. Скрябина",
    page_icon="🐾",
    layout="centered"
)

# API Конфигурация Gemini
API_KEY = ""  # Ключ будет подставлен средой выполнения
MODEL_ID = "gemini-2.5-flash-preview-09-2025"

def call_gemini_mentor(task_text, user_answer, correct_answer):
    """Вызов ИИ-Ментора для помощи ученику"""
    prompt = f"""
    Ты — добрый и мудрый ментор по ветеринарной математике в Академии им. Скрябина. 
    Ученик решает задачу: "{task_text}"
    Правильный ответ: {correct_answer}
    Ученик ввел: {user_answer}
    
    Твоя задача: НЕ ДАВАТЬ правильный ответ сразу. 
    1. Подбодри ученика.
    2. Наводящими вопросами или подсказкой по формуле помоги ему найти ошибку.
    3. Объясни логику (например, напомни про перевод процентов в доли или граммов в миллиграммы).
    Пиши кратко и дружелюбно.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": "Ты ветеринарный ментор. Помогаешь решать задачи на дозировки. Не даешь готовых ответов, ведешь к ним через подсказки."}]}
    }
    
    # Экспоненциальная задержка (retry logic)
    for delay in [1, 2, 4, 8, 16]:
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Хмм, что-то я задумался. Попробуй еще раз!")
            time.sleep(delay)
        except:
            time.sleep(delay)
    return "Извини, связь с ментором прервалась. Проверь формулу m = M * p!"

# Инициализация состояния сессии
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'mentor_feedback' not in st.session_state:
    st.session_state.mentor_feedback = {}

# Стилизация
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1e3a8a; color: white; }
    .formula-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .sidebar-logo { font-size: 24px; font-weight: bold; color: #1e3a8a; text-align: center; margin-bottom: 20px; }
    .mentor-box { background-color: #fff4e6; padding: 15px; border-radius: 10px; border-left: 5px solid #f59e0b; margin-top: 10px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# Заголовок
st.title("🐾 Ветеринарная математика")
st.caption("Тренажер с ИИ-Ментором для МВА им. К.И. Скрябина")

# Навигация
tab1, tab2, tab3 = st.tabs(["🧮 Калькулятор", "📖 Шпаргалка", "📝 Задачник (25 задач)"])

# --- ТАБ 1: КАЛЬКУЛЯТОР ---
with tab1:
    st.header("Умный помощник")
    col1, col2 = st.columns(2)
    with col1:
        tab_m = st.number_input("Вес таблетки (мг)", value=20.0, key="calc_tab_m")
        tab_p = st.number_input("Активное вещество (%)", value=18.0, key="calc_tab_p")
    with col2:
        anim_m = st.number_input("Вес животного (кг)", value=8.0, key="calc_anim_m")
        anim_d = st.number_input("Дозировка (мг/кг)", value=1.35, key="calc_anim_d")

    res_m = tab_m * (tab_p / 100)
    res_d = anim_m * anim_d
    res_n = res_d / res_m if res_m > 0 else 0
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("В 1 таблетке (мг)", f"{res_m:.2f}")
    c2.metric("Нужно всего (мг)", f"{res_d:.2f}")
    c3.metric("Итого таблеток", f"{res_n:.2f}")

# --- ТАБ 2: ШПАРГАЛКА ---
with tab2:
    st.header("Твои подсказки")
    st.markdown("""
    <div class="formula-card">
        <h4>1. Лекарство в таблетке: m = M × p</h4>
        <h4>2. Потребность животного: D = Вес × Дозировка</h4>
        <h4>3. Количество таблеток: n = D / m</h4>
    </div>
    """, unsafe_allow_html=True)

# --- ТАБ 3: ЗАДАЧНИК ---
with tab3:
    all_tasks = [
        {"id": 1, "cat": "Базовый", "q": "Таблетка 100 мг, 10% витаминов. Сколько мг витаминов в таблетке?", "a": 10.0},
        {"id": 2, "cat": "Базовый", "q": "Собака 10 кг, доза 5 мг/кг. Какова общая доза (мг)?", "a": 50.0},
        {"id": 3, "cat": "Базовый", "q": "Нужно 20 мг, в таблетке 10 мг. Сколько таблеток дать?", "a": 2.0},
        {"id": 9, "cat": "Практик", "q": "Таблетка 30 мг (15%); доза 1 мг/кг, вес 9 кг. Сколько таблеток?", "a": 2.0},
        {"id": 19, "cat": "Эксперт", "q": "Таблетка 0.5 г, в ней 4% вещества. Сколько это мг?", "a": 20.0},
        {"id": 20, "cat": "Эксперт", "q": "Доза 1.35 мг/кг, вес 8 кг, таб 20 мг (18%). Сколько таблеток?", "a": 3.0},
        # ... (здесь могут быть остальные задачи из вашего списка)
    ]

    for category in ["Базовый", "Практик", "Эксперт"]:
        st.subheader(f"Уровень: {category}")
        cat_tasks = [t for t in all_tasks if t["cat"] == category]
        
        for t in cat_tasks:
            tid = t["id"]
            with st.expander(f"Задача №{tid} {'✅' if st.session_state.results.get(tid) else ''}"):
                st.write(t["q"])
                u_ans = st.number_input("Твой ответ:", key=f"in_{tid}", step=0.01)
                
                col_btn1, col_btn2 = st.columns([1, 2])
                if col_btn1.button("Проверить", key=f"b_{tid}"):
                    if abs(u_ans - t["a"]) < 0.001:
                        st.session_state.results[tid] = True
                        st.session_state.mentor_feedback.pop(tid, None)
                        st.success("🎉 Правильно!")
                    else:
                        st.session_state.results[tid] = False
                        with st.spinner("Ментор изучает твой ответ..."):
                            feedback = call_gemini_mentor(t["q"], u_ans, t["a"])
                            st.session_state.mentor_feedback[tid] = feedback
                
                if tid in st.session_state.mentor_feedback:
                    st.markdown(f'<div class="mentor-box"><b>🧙‍♂️ Ментор:</b><br>{st.session_state.mentor_feedback[tid]}</div>', unsafe_allow_html=True)

# Сайдбар
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎓 МВА им. Скрябина</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📈 Прогресс")
    solved = sum(1 for v in st.session_state.results.values() if v)
    st.write(f"Решено: **{solved}**")
    st.progress(min(solved / 25, 1.0))
    if solved >= 5: st.success("Отличное начало!")
