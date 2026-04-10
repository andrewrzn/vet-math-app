import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Ветеринарная математика | МВА им. Скрябина",
    page_icon="🐾",
    layout="centered"
)

# Инициализация состояния сессии для хранения ответов (чтобы не тормозило)
if 'results' not in st.session_state:
    st.session_state.results = {}

# Стилизация интерфейса
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1e3a8a;
        color: white;
    }
    .formula-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .task-box {
        background-color: #f1f5f9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #e2e8f0;
    }
    .sidebar-logo {
        font-size: 24px;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок
st.title("🐾 Ветеринарная математика")
st.caption("Полный интерактивный курс по расчету дозировок для МВА им. К.И. Скрябина")

# Навигация
tab1, tab2, tab3 = st.tabs(["🧮 Калькулятор", "📖 Шпаргалка", "📝 Задачник (25 задач)"])

# --- ТАБ 1: КАЛЬКУЛЯТОР ---
with tab1:
    st.header("Умный помощник")
    st.write("Используй калькулятор, если запуталась в цифрах при решении задач.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Препарат")
        tab_m = st.number_input("Вес таблетки (мг)", value=20.0, key="calc_tab_m")
        tab_p = st.number_input("Активное вещество (%)", value=18.0, key="calc_tab_p")
    with col2:
        st.subheader("Пациент")
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
        <h4>1. Сколько лекарства в таблетке?</h4>
        <p><b>m = M × p</b> (где p — процент в долях, например 0.18)</p>
    </div>
    <div class="formula-card">
        <h4>2. Сколько лекарства нужно животному?</h4>
        <p><b>D = Вес × Дозировка</b></p>
    </div>
    <div class="formula-card">
        <h4>3. Сколько это в таблетках?</h4>
        <p><b>n = D / m</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💡 Важно: Если в задаче граммы (г), умножь их на 1000, чтобы получить миллиграммы (мг)!")

# --- ТАБ 3: ЗАДАЧНИК ---
with tab3:
    st.header("Тренажер: От простого к сложному")
    
    # Данные всех 25 задач
    all_tasks = [
        {"id": 1, "cat": "Базовый", "q": "Таблетка 100 мг, 10% витаминов. Сколько мг витаминов в таблетке?", "a": 10.0},
        {"id": 2, "cat": "Базовый", "q": "Собака 10 кг, доза 5 мг/кг. Какова общая доза (мг)?", "a": 50.0},
        {"id": 3, "cat": "Базовый", "q": "Нужно 20 мг, в таблетке 10 мг. Сколько таблеток дать?", "a": 2.0},
        {"id": 4, "cat": "Базовый", "q": "Ампула 5 мл, 20% вещества. Сколько мл чистого вещества?", "a": 1.0},
        {"id": 5, "cat": "Базовый", "q": "Таблетка 400 мг, 50% сахара. Сколько мг сахара?", "a": 200.0},
        {"id": 6, "cat": "Базовый", "q": "Доза 2 мг/кг, вес 3 кг, в таб 6 мг. Сколько таблеток?", "a": 1.0},
        {"id": 7, "cat": "Базовый", "q": "Животное 20 кг, нужно 40 мг. Сколько это мг на 1 кг?", "a": 2.0},
        {"id": 8, "cat": "Базовый", "q": "Упаковка 10 таб по 5 мг. Сколько всего мг в упаковке?", "a": 50.0},
        {"id": 9, "cat": "Практик", "q": "Таблетка 30 мг (15%); доза 1 мг/кг, вес 9 кг. Сколько таблеток?", "a": 2.0},
        {"id": 10, "cat": "Практик", "q": "Таблетка 50 мг (12%); доза 3 мг/кг, вес 4 кг. Сколько таблеток?", "a": 2.0},
        {"id": 11, "cat": "Практик", "q": "Ребёнок 6 кг; доза 2,5 мг/кг; таб 20 мг (15%). Сколько таблеток?", "a": 5.0},
        {"id": 12, "cat": "Практик", "q": "Сироп 5%, 1 мл = 1000 мг. Сколько мг вещества в 1 мл?", "a": 50.0},
        {"id": 13, "cat": "Практик", "q": "Щенок 2 кг; доза 4,5 мг/кг; таб 45 мг (20%). Сколько таблеток?", "a": 1.0},
        {"id": 14, "cat": "Практик", "q": "Телёнок 40 кг; нужно 0,8 мг/кг; таб 16 мг чистого вещества. Сколько таблеток?", "a": 2.0},
        {"id": 15, "cat": "Практик", "q": "В таб 10 мг вещества — это 5% массы. Сколько мг весит вся таблетка?", "a": 200.0},
        {"id": 16, "cat": "Практик", "q": "Кошка 4 кг, дали 0,5 таб (в целой 10 мг). Какая доза вышла (мг/кг)?", "a": 1.25},
        {"id": 17, "cat": "Практик", "q": "Даем 3 таб/сутки (в таб 2 мг) коту 3 кг. Какая доза (мг/кг)?", "a": 2.0},
        {"id": 18, "cat": "Эксперт", "q": "Доза 1.2 мг/кг (2 раза в день), вес 10 кг, таб 12 мг. Сколько таб в СУТКИ?", "a": 2.0},
        {"id": 19, "cat": "Эксперт", "q": "Таблетка 0.5 г, в ней 4% вещества. Сколько это мг?", "a": 20.0},
        {"id": 20, "cat": "Эксперт", "q": "Доза 1.35 мг/кг, вес 8 кг, таб 20 мг (18%). Сколько таблеток?", "a": 3.0},
        {"id": 21, "cat": "Эксперт", "q": "Раствор 10% (100 мг в 1 мл). Нужно 250 мг. Сколько мл набрать?", "a": 2.5},
        {"id": 22, "cat": "Эксперт", "q": "Кобыла 500 кг, доза 0.1 мг/кг, таб 25 мг. Сколько таблеток?", "a": 2.0},
        {"id": 23, "cat": "Эксперт", "q": "Таблетка 250 мг, в ней 0.05 г вещества. Какой % содержания?", "a": 20.0},
        {"id": 24, "cat": "Эксперт", "q": "Сутки: 10 мг/кг, вес 12 кг, 3 приёма, таб 20 мг. Сколько таб на ОДИН прием?", "a": 2.0},
        {"id": 25, "cat": "Эксперт", "q": "Препарат А: 200 мг (10%). Препарат Б: 100 мг (20%). Сколько мг в таб А?", "a": 20.0},
    ]

    # Сортировка по категориям
    for category in ["Базовый", "Практик", "Эксперт"]:
        st.subheader(f"Уровень: {category}")
        cat_tasks = [t for t in all_tasks if t["cat"] == category]
        
        for t in cat_tasks:
            task_id = t["id"]
            with st.expander(f"Задача №{task_id}"):
                st.write(t["q"])
                
                # Поле ввода
                ans = st.number_input("Твой ответ:", key=f"input_{task_id}", step=0.01)
                
                # Кнопка проверки
                if st.button("Проверить", key=f"btn_{task_id}"):
                    if abs(ans - t["a"]) < 0.001:
                        st.session_state.results[task_id] = True
                    else:
                        st.session_state.results[task_id] = False
                
                # Отображение результата из session_state (мгновенно)
                if task_id in st.session_state.results:
                    if st.session_state.results[task_id]:
                        st.success("🎉 Правильно!")
                    else:
                        st.error("Не совсем. Проверь расчеты!")

# Сайдбар (боковая панель)
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🎓 МВА им. Скрябина</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📈 Твой прогресс")
    
    solved_count = sum(1 for v in st.session_state.results.values() if v)
    total_count = len(all_tasks)
    
    st.write(f"Решено задач: **{solved_count}** из **{total_count}**")
    progress_bar = st.progress(solved_count / total_count)
    
    if solved_count == total_count:
        st.balloons()
        st.success("Великолепно! Ты готова к экзамену!")
    
    st.markdown("---")
    st.info("""
    **Совет:**
    Если ответ не проходит, убедись, что ты перевела граммы в миллиграммы!
    """)
