import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(page_title="Arya Institute Parent App", page_icon="🎓", layout="centered")

# Load Database from CSV File
DATA_FILE = "students_data.csv"


def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        st.error("⚠️ Database file (students_data.csv) not found!")
        return None


df_users = load_data()

# Session State for Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🎓 Arya Institute of Technology, Kukas (Jaipur)")
    st.subheader("Parent & Student Portal - Login")
    st.markdown("---")

    with st.form("login_form"):
        username_input = st.text_input("Username (Roll Number, e.g., IT54, IT57)").strip()
        password_input = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Login")

        if submit_btn:
            if df_users is not None and username_input in df_users['roll_no'].values:
                user_row = df_users[df_users['roll_no'] == username_input].iloc[0]
                if str(user_row['password']) == password_input:
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.success("Login Successful! Loading dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Invalid Password!")
            else:
                st.error("❌ Roll Number not found in Database!")

    st.info(
        "💡 **Demo Credentials:**\n- `IT54` / `password123` (Payal Mishra)\n- `IT57` / `mypassword` (Pooja Rayaka)\n- `IT59` / `pass123` (Puneet Prashar)")

# --- MAIN APP DASHBOARD ---
else:
    user_row = df_users[df_users['roll_no'] == st.session_state.username].iloc[0]

    # Header & Logout
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.title("🎓 Arya Institute of Technology")
        st.subheader(f"Welcome, Parent of {user_row['name']}")
    with col_h2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    st.markdown("---")

    # Student Profile Info
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Student Name:** {user_row['name']}")
        st.write(f"**Roll Number:** {user_row['roll_no']}")
    with c2:
        st.write(f"**Branch:** {user_row['branch']}")
        st.write(f"**Year:** {user_row['year']}")

    st.markdown("---")

    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Attendance", "📝 Exam Results (Out of 20)", "📅 Class Schedule", "📢 Notice & Fees"])

    # 1. Attendance Tab
    with tab1:
        st.header("Attendance Overview")
        total_c = int(user_row['total_classes'])
        present_c = int(user_row['present'])
        absent_c = int(user_row['absent'])
        pct = (present_c / total_c) * 100

        st.metric(label="Overall Attendance Percentage", value=f"{pct:.1f}%")
        st.progress(pct / 100)

        st.write(f"- **Total Classes Held:** {total_c}")
        st.write(f"- **Present Days:** {present_c}")
        st.write(f"- **Absent Days:** {absent_c}")

        if pct < 75:
            st.error("⚠️ Warning: Attendance is below 75% criteria!")
        else:
            st.info("✅ Attendance criteria fulfilled.")

    # 2. Results Tab
    with tab2:
        st.header("Mid-Term Exam Results (Out of 20)")
        marks_dict = {
            "Subject": [
                "Universal Human Values",
                "Civil Engineering",
                "Basic Mechanical Engineering",
                "Mathematics",
                "Chemistry",
                "C Programming"
            ],
            "Obtained Marks": [
                user_row['u_human_values'],
                user_row['civil_eng'],
                user_row['mech_eng'],
                user_row['maths'],
                user_row['chemistry'],
                user_row['c_prog']
            ],
            "Total Marks": [20, 20, 20, 20, 20, 20]
        }
        df_marks = pd.DataFrame(marks_dict)
        st.table(df_marks)

    # 3. Timetable Tab
    with tab3:
        st.header("Daily Class Schedule")
        schedule_data = {
            "Time": ["09:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:15 AM - 12:15 PM", "01:00 PM - 02:00 PM"],
            "Subject": ["Universal Human Values", "Mathematics", "C Programming", "Engineering Lab"],
            "Room": ["Room 101", "Room 102", "Lab 1", "Workshop"]
        }
        df_schedule = pd.DataFrame(schedule_data)
        st.dataframe(df_schedule, use_container_width=True)

    # 4. Notice Board Tab
    with tab4:
        st.header("College Announcements & Fee Status")
        st.info("📌 **Mid-Term Exams:** Starting from 15th of this month.")
        st.warning("💳 **Fee Reminder:** Please clear upcoming semester fees before the 10th.")
        st.success("✅ **Fee Status:** Previous semester fees fully paid.")