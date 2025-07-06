import streamlit as st
import pandas as pd
import datetime

# Page config
st.set_page_config(page_title="Book of Work Tracker", layout="wide")

st.title("📘 Book of Work Tracker")

# Load or initialize session state
if 'work_items' not in st.session_state:
    st.session_state.work_items = []

# --- CSV Save/Load ---
st.sidebar.header("💾 Data Management")
if st.sidebar.button("Save to CSV"):
    if st.session_state.work_items:
        df = pd.DataFrame(st.session_state.work_items)
        df.to_csv("work_items.csv", index=False)
        st.sidebar.success("Work items saved to work_items.csv")
    else:
        st.sidebar.info("No work items to save.")

if st.sidebar.button("Load from CSV"):
    try:
        df = pd.read_csv("work_items.csv")
        st.session_state.work_items = df.to_dict(orient="records")
        st.sidebar.success("Work items loaded from work_items.csv")
    except FileNotFoundError:
        st.sidebar.error("No CSV file found to load.")

# --- Input Form ---
st.sidebar.header("➕ Add New Work Item")
with st.sidebar.form("new_task_form"):
    work_request = st.text_input("Work Request")
    requestor = st.text_input("Requestor")
    department = st.text_input("Department")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    request_date = st.date_input("Request Date", min_value=datetime.date(2000, 1, 1))
    start_date = st.date_input("Start Date", min_value=datetime.date(2000, 1, 1))
    due_date = st.date_input("Due Date", min_value=datetime.date.today())
    assignee = st.selectbox("Assignee", ["Stephen", "Alphy"])
    category = st.selectbox("Category", ["Bug", "Feature", "Improvement", "Task", "Other"])
    submit = st.form_submit_button("Add Task")

    if submit and work_request:
        st.session_state.work_items.append({
            "ID": len(st.session_state.work_items) + 1,
            "Work Request": work_request,
            "Requestor": requestor,
            "Department": department,
            "Description": description,
            "Priority": priority,
            "Request Date": request_date.strftime("%Y-%m-%d"),
            "Start Date": start_date.strftime("%Y-%m-%d"),
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
    display_cols = ["ID", "Work Request", "Requestor", "Department", "Priority", "Request Date", "Start Date", "Status", "Due Date", "Assignee", "Category"]
    df_display = df[display_cols]
    st.dataframe(df_display, use_container_width=True)
else:
    st.info("No work items added yet.")

# --- Optional: Task Status Updater ---
st.sidebar.header("✅ Update Task Status")
if st.session_state.work_items:
    task_ids = [f"{item['ID']}: {item['Work Request']}" for item in st.session_state.work_items]
    selected = st.sidebar.selectbox("Select Task", task_ids)
    new_status = st.sidebar.selectbox("New Status", ["Open", "In Progress", "Blocked", "Complete"])
    if st.sidebar.button("Update Status"):
        task_id = int(selected.split(":")[0])
        for item in st.session_state.work_items:
            if item['ID'] == task_id:
                item['Status'] = new_status
                st.sidebar.success("Status updated!")
                break
