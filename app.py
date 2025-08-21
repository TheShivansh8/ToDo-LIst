import streamlit as st
import pandas as pd
import json
from datetime import datetime, date

st.set_page_config(page_title="To-Do App", layout="wide")
st.title("✅ Advanced To-Do List with Progress & Deadlines")

# --- Initialize session state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Utility functions ---
def save_tasks(filename="tasks.json"):
    with open(filename, "w") as f:
        json.dump(st.session_state.tasks, f)

def load_tasks(file):
    data = json.load(file)
    st.session_state.tasks = data

# --- Add Task ---
st.header("➕ Add a Task")
with st.form("task_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    with col1:
        task_name = st.text_input("Task Name")
    with col2:
        deadline = st.date_input("Deadline", value=None)
    with col3:
        reminder_time = st.time_input("Reminder Time (optional)", value=None)
    with col4:
        category = st.selectbox("Category", ["General", "Work", "Study", "Personal", "Other"])
    
    submitted = st.form_submit_button("Add Task")

    if submitted and task_name:
        st.session_state.tasks.append({
            "task": task_name,
            "done": False,
            "deadline": str(deadline) if deadline else "",
            "reminder": str(reminder_time) if reminder_time else "",
            "category": category
        })
        st.success(f"Task '{task_name}' added!")

# --- Show Tasks ---
st.header("📋 Your Tasks")
today = date.today()

if st.session_state.tasks:
    overdue_count, due_today_count = 0, 0

    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.05, 0.35, 0.15, 0.15, 0.15, 0.15])

        # Checkbox for completion
        done = cols[0].checkbox("", value=task["done"], key=f"done_{i}")
        st.session_state.tasks[i]["done"] = done

        # Deadline check
        task_deadline = None
        if task["deadline"]:
            try:
                task_deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
            except:
                pass

        # Task label formatting
        task_label = task["task"]
        if done:
            task_label = f"~~{task_label}~~ ✅"
        elif task_deadline:
            if task_deadline < today:
                task_label = f"🔴 **{task_label}**"
                overdue_count += 1
            elif task_deadline == today:
                task_label = f"🟡 **{task_label}**"
                due_today_count += 1
            else:
                task_label = f"**{task_label}**"

        # Display row
        cols[1].markdown(task_label)
        cols[2].write(f"📅 {task['deadline']}" if task['deadline'] else "-")
        cols[3].write(f"⏰ {task['reminder']}" if task['reminder'] else "-")
        cols[4].write(f"🏷 {task['category']}")
        if cols[5].button("🗑 Delete", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()

    # --- Stats ---
    total = len(st.session_state.tasks)
    completed = sum(1 for t in st.session_state.tasks if t["done"])
    pending = total - completed
    overdue = overdue_count
    due_today = due_today_count

    percent_completed = round((completed / total) * 100, 1) if total else 0
    percent_pending = round((pending / total) * 100, 1) if total else 0
    percent_overdue = round((overdue / total) * 100, 1) if total else 0

    # --- Progress Overview ---
    st.subheader("📊 Progress Dashboard")
    st.progress(int(percent_completed))
    st.success(f"✅ Completed: {completed}/{total} ({percent_completed}%)")
    st.warning(f"⏳ Pending: {pending}/{total} ({percent_pending}%)")
    if overdue > 0:
        st.error(f"🚨 Overdue: {overdue} ({percent_overdue}%)")
    if due_today > 0:
        st.info(f"📌 Due Today: {due_today}")

    # --- Clear Completed Button ---
    if st.button("🧹 Clear All Completed"):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
        st.experimental_rerun()

else:
    st.info("No tasks yet. Add one above!")

# --- Sidebar ---
st.sidebar.header("📂 Task Management")
uploaded = st.sidebar.file_uploader("Import Tasks (JSON)", type=["json"])
if uploaded:
    load_tasks(uploaded)
    st.sidebar.success("Tasks imported successfully!")
    st.experimental_rerun()

if st.sidebar.button("💾 Export Tasks"):
    save_tasks()
    with open("tasks.json", "rb") as f:
        st.sidebar.download_button("Download tasks.json", f, file_name="tasks.json")

st.sidebar.header("📌 Summary")
if st.session_state.tasks:
    st.sidebar.write(f"✅ Completed: {completed}")
    st.sidebar.write(f"⏳ Pending: {pending}")
    st.sidebar.write(f"🚨 Overdue: {overdue}")
    st.sidebar.write(f"📌 Due Today: {due_today}")
else:
    st.sidebar.info("No tasks available.")

