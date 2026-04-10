import streamlit as st
import requests
import time

# --- ИНИЦИАЛИЗАЦИЯ И НАСТРОЙКИ ---
st.set_page_config(page_title="Ветеринарная математика | МВА", page_icon="🐾")

# Получение ключа из Secrets
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if 'results' not in st.session_state:
    st.session_state.results = {}
if 'mentor_feedback' not in st.session_state:
    st.session_state.mentor_feedback = {}

# --- ФУНКЦИЯ МЕНТОРА ---
def call_gemini_mentor(task_text, user_answer, correct_answer):
    if not API_KEY:
        return "⚠️ Ошибка: API ключ не настроен в Secrets. Проверь формулу m = M * (p/100)!"
    
    prompt = f"Ученик решает: {task_text}. Правильно: {correct_answer}, введено: {user_answer}. Подбодри и дай наводку на формулу, не называя сам ответ."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        pass
    return "Не могу связаться с магией ИИ, но советую перепроверить перевод граммов в миллиграммы!"

# --- КОНТЕНТ ЗАДАЧ ---
all_tasks = [
    # БАЗОВЫЙ
    {"id": 1, "cat": "Базовый", "q": "Таблетка 100 мг, 10% активного вещества. Сколько это в мг?", "a": 10.0},
    {"id": 2, "cat": "Базовый", "q": "Собака 10 кг, доза 5 мг/кг. Какова общая доза в мг?", "a": 50.0},
    {"id": 3, "cat": "Базовый", "q": "Нужно 20 мг, в таблетке 10 мг. Сколько таблеток дать?", "a": 2.0},
    {"id": 4, "cat": "Базовый", "q": "Ампула 5 мл, 20% вещества. Сколько мл чистого вещества?", "a": 1.0},
    {"id": 5, "cat": "Базовый", "q": "Таблетка 400 мг, 50% сахара. Сколько мг сахара?", "a": 200.0},
    {"id": 6, "cat": "Базовый", "q": "Доза 2 мг/кг, вес 3 кг, в таб 6 мг чистого в-ва. Сколько таблеток?", "a": 1.0},
    {"id": 7, "cat": "Базовый", "q": "Животное 20 кг, нужно 40 мг. Сколько это мг на 1 кг?", "a": 2.0},
    {"id": 8, "cat": "Базовый", "q": "Упаковка 10 таб по 5 мг. Сколько всего мг в упаковке?", "a": 50.0},
    # ПРАКТИК
    {"id": 9, "cat": "Практик", "q": "Таблетка 30 мг (15%); доза 1 мг/кг, вес 9 кг. Сколько таблеток?", "a": 2.0},
    {"id": 10, "cat": "Практик", "q": "Таблетка 50 мг (12%); доза 3 мг/кг, вес 4 кг. Сколько таблеток?", "a": 2.0},
    {"id": 11, "cat": "Практик", "q": "Щенок 6 кг; доза 2,5 мг/кг; таб 20 мг (15%). Сколько таблеток?", "a": 5.0},
    {"id": 12, "cat": "Практик", "q": "Сироп 5%, 1 мл весит 1000 мг. Сколько мг в-ва в 1 мл?", "a": 50.0},
    {"id": 13, "cat": "Практик", "q": "Кот 2 кг; доза 4,5 мг/кг; таб 45 мг (20%). Сколько таблеток?", "a": 1.0},
    {"id": 14, "cat": "Практик", "q": "Телёнок 40 кг; нужно 0,8 мг/кг; таб 16 мг чистого в-ва. Сколько таблеток?", "a": 2.0},
    {"id": 15, "cat": "Практик", "q": "В таб 10 мг в-ва — это 5% массы. Сколько мг весит таблетка?", "a": 200.0},
    {"id": 16, "cat": "Практик", "q": "Кошка 4 кг, дали 0,5 таб (в целой 10 мг). Какая доза (мг/кг)?", "a": 1.25},
    {"id": 17, "cat": "Практик", "q": "Даем 3 таб/сутки (в таб 2 мг) коту 3 кг. Какая доза (мг/кг)?", "a": 2.0},
    # ЭКСПЕРТ
    {"id": 18, "cat": "Эксперт", "q": "Доза 1.2 мг/кг (2р в день), вес 10 кг, таб 12 мг. Сколько таб в СУТКИ?", "a": 2.0},
    {"id": 19, "cat": "Эксперт", "q": "Таблетка 0.5 г, в ней 4% вещества. Сколько это мг?", "a": 20.0},
    {"id": 20, "cat": "Эксперт", "q": "Доза 1.35 мг/кг, вес 8 кг, таб 20 мг (18%). Сколько таблеток?", "a": 3.0},
    {"id": 21, "cat": "Эксперт", "q": "Раствор 10% (100 мг/мл). Нужно 250 мг. Сколько мл набрать?", "a": 2.5},
    {"id": 22, "cat": "Эксперт", "q": "Кобыла 500 кг, доза 0.1 мг/кг, таб 25 мг чистого в-ва. Сколько таблеток?", "a": 2.0},
    {"id": 23, "cat": "Эксперт", "q": "Таблетка 250 мг, в ней 0.05 г вещества. Какой % содержания?", "a": 20.0},
    {"id": 24, "cat": "Эксперт", "q": "Сутки: 10 мг/кг, вес 12 кг, 3 приёма, таб 20 мг. Сколько таб на ОДИН прием?", "a": 2.0},
    {"id": 25, "cat": "Эксперт", "q": "Препарат А: 200 мг (10%). Препарат Б: 100 мг (20%). Сколько мг в таб А?", "a": 20.0},
]

# --- ИНТЕРФЕЙС ---
st.title("🐾 Академия им. Скрябина: Тренажер")
tab_calc, tab_learn, tab_tasks = st.tabs(["🧮 Помощник", "📖 Формулы", "📝 Задачи"])

with tab_tasks:
    for cat in ["Базовый", "Практик", "Эксперт"]:
        st.subheader(f"Уровень: {cat}")
        for t in [x for x in all_tasks if x["cat"] == cat]:
            with st.expander(f"Задача №{t['id']} {'✅' if st.session_state.results.get(t['id']) else ''}"):
                st.write(t["q"])
                ans = st.number_input("Ответ:", key=f"ans_{t['id']}", step=0.01)
                if st.button("Проверить", key=f"btn_{t['id']}"):
                    if abs(ans - t["a"]) < 0.01:
                        st.session_state.results[t["id"]] = True
                        st.session_state.mentor_feedback.pop(t["id"], None)
                        st.success("Верно!")
                    else:
                        st.session_state.results[t["id"]] = False
                        with st.spinner("Ментор пишет подсказку..."):
                            st.session_state.mentor_feedback[t["id"]] = call_gemini_mentor(t["q"], ans, t["a"])
                
                if t["id"] in st.session_state.mentor_feedback:
                    st.warning(f"🧙‍♂️ **Ментор:** {st.session_state.mentor_feedback[t['id']]}")

# Сайдбар
st.sidebar.title("📈 Прогресс")
solved = sum(1 for v in st.session_state.results.values() if v)
st.sidebar.write(f"Решено: {solved} из 25")
st.sidebar.progress(solved / 25)
