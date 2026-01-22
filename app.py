import streamlit as st
import asyncio
import os
import glob
from orchestrator import AgentOrchestrator
from utils.logger import logger
import logging

# Настройка логирования для Streamlit
class StreamlitLogger(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            if "✓" in msg:
                st.session_state.logs.append({"type": "success", "msg": msg})
            elif "✗" in msg or "Ошибка" in msg:
                st.session_state.logs.append({"type": "error", "msg": msg})
            elif "Шаг" in msg:
                st.session_state.logs.append({"type": "info", "msg": msg})
            else:
                st.session_state.logs.append({"type": "normal", "msg": msg})
        except Exception:
            self.handleError(record)

# Инициализация состояния
if "logs" not in st.session_state:
    st.session_state.logs = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AgentOrchestrator()

# Настройка страницы
st.set_page_config(
    page_title="Agent Orchestrator",
    page_icon="🤖",
    layout="wide"
)

# Подключение CSS
def load_css():
    css_file = "assets/style.css"
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --- Сайдбар: Настройки и Управление ---
with st.sidebar:
    st.markdown("## 🎛 Control Center")
    
    # Режим работы
    mode = st.radio(
        "Режим работы", 
        ["🤖 Auto Orchestration", "💬 Direct Chat"], 
        index=0,
        help="Auto: Координатор строит план. Direct: Общение с конкретным агентом."
    )
    
    # Селектор Агента (для Direct режима)
    selected_agent = None
    if mode == "💬 Direct Chat":
        if "orchestrator" in st.session_state:
            agent_names = list(st.session_state.orchestrator.list_agents().keys())
            if "coordinator" in agent_names: agent_names.remove("coordinator")
            selected_agent = st.selectbox("Выбор агента", agent_names)
            st.info(f"Вы общаетесь напрямую с **{selected_agent.capitalize()}**")

    st.markdown("---")

    # Управление сессиями
    with st.expander("💾 Память и Сессии", expanded=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("Сохранить", use_container_width=True):
                try:
                    os.makedirs("sessions", exist_ok=True)
                    session_file = f"sessions/session_{len(glob.glob('sessions/*')) + 1}.json"
                    st.session_state.orchestrator.save_session(session_file)
                    st.toast(f"Saved: {os.path.basename(session_file)}")
                except Exception as e:
                    st.error(str(e))
        
        with col_s2:
            session_files = glob.glob("sessions/*.json")
            if session_files:
                selected_sess = st.selectbox("Load", session_files, label_visibility="collapsed")
                if st.button("Загрузить", use_container_width=True):
                    try:
                        st.session_state.orchestrator.load_session(selected_sess)
                        st.toast("Session Loaded!")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            else:
                st.caption("Нет сохранений")

    # Настройки модели
    with st.expander("⚙️ Конфигурация", expanded=False):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        model = st.selectbox("Model", ["gemini-pro", "gemini-1.5-flash", "gemini-1.5-pro"])
        if st.button("Применить", type="primary", use_container_width=True):
            from utils.config import Config
            Config.TEMPERATURE = temperature
            Config.MODEL_NAME = model
            st.session_state.orchestrator = AgentOrchestrator()
            st.toast("Config Updated")

    # Файлы результатов
    st.markdown("### 📂 Результаты")
    result_files = glob.glob("results/*.md") if os.path.exists("results") else []
    result_files.sort(key=os.path.getmtime, reverse=True)
    if result_files:
        selected_file = st.selectbox("История", result_files, format_func=lambda x: os.path.basename(x))
        if selected_file:
            with open(selected_file, "r") as f:
                content = f.read()
            st.download_button("Скачать Markdown", content, file_name=os.path.basename(selected_file), mime="text/markdown", use_container_width=True)
            with st.popover("Просмотр"):
                st.markdown(content)

# --- ГЛАВНАЯ ОБЛАСТЬ ---

# Заголовок (если чат пуст)
if not st.session_state.messages:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("# 👋 Agent Orchestrator")
    st.markdown("### Ваша команда автономных AI-агентов")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Карточки быстрого запуска
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 20px; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; background: rgba(255,255,255,0.05);">
            <h3>🔍 Research</h3>
            <p>Глубокий поиск и анализ информации в интернете.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Исследовать крипторынок 2026", use_container_width=True):
            st.session_state.next_prompt = "Проведи исследование рынка криптовалют на 2026 год, выдели главные тренды"

    with col2:
        st.markdown("""
        <div style="padding: 20px; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; background: rgba(255,255,255,0.05);">
            <h3>💻 Code Audit</h3>
            <p>Анализ кода на безопасность и качество.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Проверить этот проект", use_container_width=True):
            st.session_state.next_prompt = "Проанализируй файлы в текущей директории на наличие ошибок архитектуры"

    with col3:
        st.markdown("""
        <div style="padding: 20px; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; background: rgba(255,255,255,0.05);">
            <h3>📝 Content</h3>
            <p>Написание статей, блогов и документации.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Написать статью про AI", use_container_width=True):
            st.session_state.next_prompt = "Напиши увлекательную статью про будущее AI агентов"

    st.markdown("---")
else:
    # Заголовок в режиме чата
    st.markdown(f"### {mode}")

# Отрисовка сообщений
for message in st.session_state.messages:
    role_icon = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=role_icon):
        if message.get("type") == "graph":
             st.graphviz_chart(message["content"])
        else:
            st.markdown(message["content"])

# --- Зона ввода ---
# Файл аплоадер над чатом
uploaded_file = st.file_uploader("Прикрепить файл контекста", type=['txt', 'py', 'md', 'json', 'pdf'], label_visibility="collapsed")
if uploaded_file:
    st.caption(f"📎 Прикреплен: {uploaded_file.name}")

# Поле чата
prompt_text = "Введите задачу для команды..." if mode == "🤖 Auto Orchestration" else f"Сообщение для {selected_agent}..."
prompt = st.chat_input(prompt_text, disabled=st.session_state.processing)

# Обработка Next Prompt (от кнопок)
if "next_prompt" in st.session_state and st.session_state.next_prompt:
    prompt = st.session_state.next_prompt
    st.session_state.next_prompt = None
    st.rerun()

if prompt:
    # Контекст файла
    file_context = ""
    if uploaded_file:
        try:
            # Читаем
            stringio = uploaded_file.getvalue().decode("utf-8")
            os.makedirs("uploads", exist_ok=True)
            temp_path = f"uploads/{uploaded_file.name}"
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(stringio)
            file_context = f"\n\n[ATTACHMENT]: {temp_path}"
        except Exception:
            file_context = "\n[Error reading file]"

    full_prompt = prompt + file_context
    
    # User Msg
    display_prompt = prompt + (f" (📎 {uploaded_file.name})" if uploaded_file else "")
    st.session_state.messages.append({"role": "user", "content": display_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(display_prompt)

    # Assistant Logic
    st.session_state.processing = True
    st.session_state.logs = []
    
    with st.chat_message("assistant", avatar="🤖"):
        # UI Elements init
        if mode == "🤖 Auto Orchestration":
            status = st.status("🚀 Orchestrator Starting...", expanded=True)
            log_area = status.empty()
        else:
            status = st.empty()
            log_area = st.empty()
            st.caption("Thinking...")

        # Async runner
        async def run():
            try:
                # Log Updater
                async def logs_loop():
                    last_i = 0
                    while st.session_state.processing:
                        if len(st.session_state.logs) > last_i:
                            if mode == "🤖 Auto Orchestration":
                                # Render console inside status
                                safe_logs = "".join([f'<div class="log-{l["type"]}">{l["msg"]}</div>' for l in st.session_state.logs])
                                log_area.markdown(f'<div class="log-console">{safe_logs}</div>', unsafe_allow_html=True)
                                status.update(label=f"⚡ {st.session_state.logs[-1]['msg']}")
                            last_i = len(st.session_state.logs)
                        await asyncio.sleep(0.1)
                
                asyncio.create_task(logs_loop())

                if mode == "🤖 Auto Orchestration":
                    res = await st.session_state.orchestrator.orchestrate_task(full_prompt, output_dir="results")
                    status.update(label="✅ Complete!", state="complete", expanded=False)
                    
                    # Construct Response
                    out = ""
                    # Plan
                    with st.expander("📋 Execution Plan"):
                        st.code(res.get('plan'), language='json')
                    out += f"**Plan Verified.**\n"
                    
                    # Steps
                    steps = res.get("steps", [])
                    if steps:
                        tabs = st.tabs([f"Step {s['step']}: {s['agent']}" for s in steps])
                        for i, s in enumerate(steps):
                            with tabs[i]:
                                if s.get('error'): st.error(s['error'])
                                else: st.markdown(s['result'])
                    
                    # Final
                    final = res.get("final_result", "")
                    if final:
                        st.markdown("### Result")
                        st.markdown(final)
                        out += f"\n\n{final}"
                        st.download_button("Save Result", final, "result.md")
                    
                    st.session_state.messages.append({"role": "assistant", "content": out})

                else: # Direct
                    agent = st.session_state.orchestrator.get_agent(selected_agent)
                    resp = await agent.execute(full_prompt)
                    st.markdown(resp)
                    st.session_state.messages.append({"role": "assistant", "content": resp})

            except Exception as e:
                st.error(str(e))
                if mode == "🤖 Auto Orchestration": status.update(state="error")
            finally:
                st.session_state.processing = False
        
        asyncio.run(run())
