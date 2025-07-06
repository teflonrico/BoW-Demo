import streamlit as st
import pandas as pd
import datetime

# Page config
st.set_page_config(page_title="Book of Work Tracker", layout="wide")

st.title("📘 Book of Work Tracker")

# Load or initialize session state
if 'work_items' not in st.session_state:
    st.session_state.work_items = []

# --- Input Form ---
st.sidebar.header("➕ Add New Work Item")
with st.sidebar.form("new_task_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Due Date", min_value=datetime.date.today())
    assignee = st.text_input("Assignee")
    category = st.selectbox("Category", ["Bug", "Feature", "Improvement", "Task", "Other"])
    submit = st.form_submit_button("Add Task")

    if submit and title:
        st.session_state.work_items.append({
            "ID": len(st.session_state.work_items) + 1,
            "Title": title,
            "Description": description,
            "Priority": priority,
            "Due Date": due_date.strftime("%Y-%m-%d"),
            "Assignee": assignee,
            "Category": category,
            "Status": "Open",
            "Created On": datetime.date.today().strftime("%Y-%m-%d")
        })
        st.success("Task added successfully!")

# --- Display Work Items ---
st.subheader("📋 Current Work Items")
if st.session_state.work_items:
    df = pd.DataFrame(st.session_state.work_items)
    df_display = df[["ID", "Title", "Priority", "Status", "Due Date", "Assignee", "Category"]]
    st.dataframe(df_display, use_container_width=True)
else:
    st.info("No work items added yet.")

# --- Optional: Task Status Updater ---
st.sidebar.header("✅ Update Task Status")
if st.session_state.work_items:
    task_ids = [f"{item['ID']}: {item['Title']}" for item in st.session_state.work_items]
    selected = st.sidebar.selectbox("Select Task", task_ids)
    new_status = st.sidebar.selectbox("New Status", ["Open", "In Progress", "Blocked", "Complete"])
    if st.sidebar.button("Update Status"):
        task_id = int(selected.split(":")[0])
        for item in st.session_state.work_items:
            if item['ID'] == task_id:
                item['Status'] = new_status
                st.sidebar.success("Status updated!")
                break
