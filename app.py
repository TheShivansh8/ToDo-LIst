import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="To-Do App", layout="centered")
st.title("✅ To-Do List with Progress Tracker")

# --- Initialize session state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Add Task ---
st.header("➕ Add a Task")
with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input("Task Name")
    deadline = st.date_input("Deadline (optional)", value=None)
    reminder_time = st.time_input("Reminder Time (optional)", value=None)
    submitted = st.form_submit_button("Add Task")

    if submitted and task_name:
        st.session_state.tasks.append({
            "task": task_name,
            "done": False,
            "deadline": str(deadline) if deadline else "",
            "reminder": str(reminder_time) if reminder_time else ""
        })
        st.success(f"Task '{task_name}' added!")

# --- Show Tasks ---
st.header("📋 Your Tasks")
if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.05, 0.6, 0.15, 0.2])
        done = cols[0].checkbox("", value=task["done"], key=f"done_{i}")
        st.session_state.tasks[i]["done"] = done
        cols[1].write(task["task"])
        cols[2].write(task["deadline"] if task["deadline"] else "-")
        cols[3].write(task["reminder"] if task["reminder"] else "-")

    # --- Progress Bar ---
    total = len(st.session_state.tasks)
    completed = sum(1 for t in st.session_state.tasks if t["done"])
    percent = int((completed / total) * 100)
    st.progress(percent)
    st.write(f"✅ {completed}/{total} tasks completed ({percent}%)")
    st.write(f"⏳ {total - completed} tasks pending")

else:
    st.info("No tasks yet. Add one above!")

# --- Future: Alert System (Telegram/Email integration) ---
st.sidebar.header("🔔 Reminder System (Prototype)")
st.sidebar.info("Currently reminders are stored with the task. Future version can integrate with Telegram/Email APIs.")
