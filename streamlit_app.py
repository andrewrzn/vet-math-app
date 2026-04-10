import streamlit as st
import requests
import time

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Ветеринарная математика | МВА", page_icon="🐾", layout="wide")

# API Конфигурация (используем внутренний прокси среды)
API_KEY = "" 
MODEL_ID = "gemini-2.5-flash-preview-09-2025"

def call_gemini_mentor(task_text, user_answer, correct_answer):
    """Вызов настоящего ИИ-Ментора"""
    prompt = f"""
    Ты — добрый преподаватель математики в ветеринарной академии. 
    Задача: {task_text}
    Правильный ответ: {correct_answer}
    Ученик ввел: {user_answer}
    
    Твоя роль: 
    1. Если ответ близок, но неточен, укажи на округление.
    2. Если ответ сильно отличается, предположи ошибку (забыл перевести мг в г, не учел проценты, ошибся в дозировке на вес).
    3. НЕ ПИШИ ПРАВИЛЬНЫЙ ОТВЕТ. Дай только наводку.
    Пиши коротко (2-3 предложения).
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": "Ты - ветеринарный ментор. Помогаешь решать задачи, не выдавая сразу ответ."}]}
    }
    
    for delay in [1, 2, 3]:
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            time.sleep(delay)
        except:
            continue
    return "Похоже, в расчетах есть неточность. Проверь еще раз размерности (мг, кг, %)!"

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ ---
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'mentor_feedback' not in st.session_state:
    st.session_state.mentor_feedback = {}

# --- ДАННЫЕ (ВСЕ ЗАДАЧИ ИЗ PDF И ВАШИ ПРЕДЫДУЩИЕ) ---
all_tasks = [
    # Список дополнен задачами из PDF
    {"id": 1, "cat": "Вступительные", "q": "Задача №1 (Таблетки): Таблетка 20 мг, 18% активного в-ва. Ребенку нужно 1.35 мг/кг. Вес 8 кг. Сколько таблеток в сутки?", "a": 3.0},
    {"id": 2, "cat": "Вступительные", "q": "Задача №5 (Бегун): Бегун пробежал 450 м за 50 секунд. Найдите среднюю скорость в км/ч.", "a": 32.4},
    {"id": 3, "cat": "Вступительные", "q": "Задача №11 (Уравнение): Решите 2^(3+x) = 0.4 * 5^(3+x).", "a": -2.0},
    {"id": 4, "cat": "Вступительные", "q": "Задача №12 (Сплавы): Сплав 1 (10% никеля), Сплав 2 (35%). Получили 225 кг (25%). На сколько кг масса первого меньше массы второго?", "a": 45.0},
    {"id": 5, "cat": "Вступительные", "q": "Задача №15 (Уравнение): 6^(x+1) - 2*6^x = 144.", "a": 2.0},
    {"id": 6, "cat": "Вступительные", "q": "Задача №13 (Вероятность): Больные (5%), Тест+ у больных (0.9), Ложно+ (0.01). Вероятность того, что тест положительный?", "a": 0.0545},
    {"id": 7, "cat": "Базовый", "q": "Собака 10 кг, доза 5 мг/кг. Какова общая доза (мг)?", "a": 50.0},
    {"id": 8, "cat": "Базовый", "q": "Таблетка 100 мг, 10% активного вещества. Сколько это в мг?", "a": 10.0},
    {"id": 9, "cat": "Практик", "q": "Таблетка 30 мг (15%); доза 1 мг/кг, вес 9 кг. Сколько таблеток?", "a": 2.0},
    {"id": 10, "cat": "Эксперт", "q": "Таблетка 0.5 г, в ней 4% вещества. Сколько это мг?", "a": 20.0},
]

# --- ИНТЕРФЕЙС ---
st.title("🐾 Тренажер МВА им. Скрябина")
st.markdown("---")

col_main, col_side = st.columns([3, 1])

with col_side:
    st.subheader("📊 Прогресс")
    solved = sum(1 for v in st.session_state.results.values() if v)
    st.write(f"Решено задач: {solved} / {len(all_tasks)}")
    st.progress(solved / len(all_tasks))
    
    st.info("💡 **Совет:** Если не получается, жми 'Проверить' еще раз, Ментор даст новую подсказку!")

with col_main:
    tabs = st.tabs(["📝 Задачи", "🧮 Калькулятор", "ℹ️ Помощь"])
    
    with tabs[0]:
        for category in sorted(list(set(t["cat"] for t in all_tasks))):
            st.header(f"Уровень: {category}")
            cat_tasks = [t for t in all_tasks if t["cat"] == category]
            
            for t in cat_tasks:
                tid = t["id"]
                with st.expander(f"Задача №{tid} {'✅' if st.session_state.results.get(tid) else ''}"):
                    st.write(f"**{t['q']}**")
                    u_ans = st.number_input("Твой ответ:", key=f"in_{tid}", format="%.4f")
                    
                    if st.button("Проверить", key=f"btn_{tid}"):
                        if abs(u_ans - t["a"]) < 0.001:
                            st.session_state.results[tid] = True
                            st.session_state.mentor_feedback.pop(tid, None)
                            st.success("🎉 Верно! Молодец!")
                        else:
                            st.session_state.results[tid] = False
                            with st.spinner("Ментор анализирует ошибку..."):
                                feedback = call_gemini_mentor(t["q"], u_ans, t["a"])
                                st.session_state.mentor_feedback[tid] = feedback
                    
                    if tid in st.session_state.mentor_feedback:
                        st.markdown(f"""
                        <div style="background-color: #fff4e6; padding: 15px; border-left: 5px solid #ffa94d; border-radius: 5px;">
                            <b>🧙‍♂️ Ментор:</b><br>{st.session_state.mentor_feedback[tid]}
                        </div>
                        """, unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("Быстрый расчет дозировок")
        v1 = st.number_input("Вес животного (кг)", value=1.0)
        v2 = st.number_input("Дозировка (мг/кг)", value=1.0)
        st.write(f"Нужно препарата: **{v1*v2} мг**")

    with tabs[2]:
        st.write("Используйте точку как разделитель. Округляйте до сотых, если не указано иное.")
