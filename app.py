# 🎓 Student Life Tracker — Aesthetic Version (Complete app.py)


import streamlit as st
import pandas as pd
import os
import datetime

st.set_page_config(
    page_title="Student Life Tracker",
    page_icon="🎓",
    layout="wide"
)

# ================= Aesthetic CSS =================

st.markdown("""
<style>

.main {
    background-color: #f6f8fc;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#667eea,#764ba2);
    color:white;
}

section[data-testid="stSidebar"] * {
    color:white !important;
}

.metric-card {
    padding:20px;
    border-radius:15px;
    color:white;
    box-shadow:0 5px 20px rgba(0,0,0,0.1);
}

.stButton>button {
    border-radius:10px;
    background: linear-gradient(135deg,#667eea,#764ba2);
    color:white;
    border:none;
}

h1, h2, h3 {
    color:#2c3e50;
}

</style>
""", unsafe_allow_html=True)

# ================= Title =================

st.title("🎓 Student Life Tracker")
st.caption("Track your studies, productivity, expenses & goals in one place")

# ================= Sidebar =================

st.sidebar.title("Navigation")

option = st.sidebar.selectbox(
    "Choose Section",
    ["Dashboard","Study Tracker","Expense Tracker","Productivity Tracker","To-Do List","Calendar"]
)

# ================= Dashboard =================

if option == "Dashboard":

    st.subheader("📊 Student Life Dashboard")

    col1, col2, col3 = st.columns(3)

    try:
        study_df = pd.read_csv("study_data.csv",names=["Date","Day","Subject","Hours"])
        total_study = study_df["Hours"].sum()
    except:
        total_study = 0

    try:
        expense_df = pd.read_csv("expense_data.csv",names=["Date","Day","Category","Amount"])
        total_expense = expense_df["Amount"].sum()
    except:
        total_expense = 0

    try:
        prod_df = pd.read_csv("productivity_data.csv",
        names=["Date","Day","Study Hours","Sleep Hours","Screen Time"])
        avg_productivity = prod_df["Study Hours"].mean()
    except:
        avg_productivity = 0

    col1.metric("📚 Total Study Hours",round(total_study,2))
    col2.metric("💰 Total Expenses",round(total_expense,2))
    col3.metric("⚡ Avg Study Hours",round(avg_productivity,2))


# ================= Monthly Analytics =================

    st.markdown("## 📈 Monthly Analytics")

    try:
        study_df["Date"] = pd.to_datetime(study_df["Date"])
        current_month = pd.to_datetime("today").month
        monthly_study = study_df[study_df["Date"].dt.month==current_month]["Hours"].sum()
    except:
        monthly_study = 0

    try:
        expense_df["Date"] = pd.to_datetime(expense_df["Date"])
        monthly_expense = expense_df[expense_df["Date"].dt.month==current_month]["Amount"].sum()
    except:
        monthly_expense = 0

    try:
        prod_df["Date"] = pd.to_datetime(prod_df["Date"])
        monthly_productivity = prod_df[prod_df["Date"].dt.month==current_month]["Study Hours"].mean()
    except:
        monthly_productivity = 0

    col1, col2, col3 = st.columns(3)

    col1.metric("📚 Monthly Study",round(monthly_study,2))
    col2.metric("💰 Monthly Expense",round(monthly_expense,2))
    col3.metric("⚡ Monthly Productivity",round(monthly_productivity,2))


# ================= Monthly Goals =================

    st.markdown("## 🎯 Monthly Goals")

    study_goal = st.number_input("Study Goal",100)
    expense_goal = st.number_input("Expense Limit",5000)
    productivity_goal = st.number_input("Productivity Goal",6)

    col1, col2, col3 = st.columns(3)

    col1.metric("Study Progress",f"{monthly_study}/{study_goal}")
    col1.progress(min(monthly_study/study_goal if study_goal else 0,1.0))

    col2.metric("Expense Used",f"{monthly_expense}/{expense_goal}")
    col2.progress(min(monthly_expense/expense_goal if expense_goal else 0,1.0))

    col3.metric("Productivity",f"{round(monthly_productivity,2)}/{productivity_goal}")
    col3.progress(min(monthly_productivity/productivity_goal if productivity_goal else 0,1.0))


# ================= Heatmap =================

    st.markdown("## 📅 Study Heatmap")

    try:
        heatmap = study_df.groupby("Date")["Hours"].sum().reset_index()

        for _, row in heatmap.iterrows():
            bars = "🟩" * int(row["Hours"])
            st.write(f"{row['Date'].date()}  {bars}")

    except:
        st.write("No data yet")

# ================= Study Tracker =================

elif option == "Study Tracker":

    st.subheader("📚 Study Tracker")

    date = st.date_input("Date")
    subject = st.text_input("Subject")
    hours = st.number_input("Hours",0.0,24.0)

    if st.button("Add Study"):

        df = pd.DataFrame([{
            "Date":date,
            "Day":date.strftime("%A"),
            "Subject":subject,
            "Hours":hours
        }])

        df.to_csv("study_data.csv",mode="a",header=False,index=False)
        st.success("Study Added")

    try:
        df = pd.read_csv("study_data.csv",
        names=["Date","Day","Subject","Hours"])

        st.dataframe(df)
        st.bar_chart(df["Hours"])

        st.subheader("📊 Weekly Study")

        df["Date"]=pd.to_datetime(df["Date"])
        df["Week"]=df["Date"].dt.isocalendar().week

        weekly=df.groupby("Week")["Hours"].sum()

        st.bar_chart(weekly)


# ================= Study Streak =================

        st.subheader("🔥 Study Streak")

        df=df.sort_values("Date")
        streak=0
        longest=0
        prev=None

        for date in df["Date"]:
            if prev is None:
                streak=1
            else:
                diff=(date-prev).days
                if diff==1:
                    streak+=1
                else:
                    longest=max(longest,streak)
                    streak=1
            prev=date

        longest=max(longest,streak)

        col1,col2=st.columns(2)
        col1.metric("Current Streak",streak)
        col2.metric("Longest Streak",longest)


# Delete

        st.subheader("🗑 Delete")

        delete_index=st.selectbox("Select entry",df.index)

        if st.button("Delete Study"):
            df=df.drop(delete_index)
            df.to_csv("study_data.csv",index=False,header=False)
            st.rerun()

    except:
        st.write("No data")

# ================= Expense Tracker =================

elif option == "Expense Tracker":

    st.subheader("💰 Expense Tracker")

    date = st.date_input("Date")
    category = st.selectbox("Category",
    ["Food","Travel","Shopping","Education","Other"])

    amount = st.number_input("Amount")

    if st.button("Add Expense"):

        df = pd.DataFrame([{
            "Date":date,
            "Day":date.strftime("%A"),
            "Category":category,
            "Amount":amount
        }])

        df.to_csv("expense_data.csv",mode="a",header=False,index=False)
        st.success("Expense Added")

    try:
        df = pd.read_csv("expense_data.csv",
        names=["Date","Day","Category","Amount"])

        st.dataframe(df)
        st.bar_chart(df["Amount"])

        st.subheader("📊 Weekly Expense")

        df["Week"]=pd.to_datetime(df["Date"]).dt.isocalendar().week
        weekly=df.groupby("Week")["Amount"].sum()

        st.bar_chart(weekly)

        delete_index=st.selectbox("Delete Expense",df.index)

        if st.button("Delete Expense"):
            df=df.drop(delete_index)
            df.to_csv("expense_data.csv",index=False,header=False)
            st.rerun()

    except:
        st.write("No data")

# ================= Productivity =================

elif option == "Productivity Tracker":

    st.subheader("⚡ Productivity Tracker")

    date=st.date_input("Date")

    study=st.number_input("Study Hours")
    sleep=st.number_input("Sleep Hours")
    screen=st.number_input("Screen Time")

    if st.button("Add Productivity"):

        df=pd.DataFrame([{
            "Date":date,
            "Day":date.strftime("%A"),
            "Study Hours":study,
            "Sleep Hours":sleep,
            "Screen Time":screen
        }])

        df.to_csv("productivity_data.csv",mode="a",header=False,index=False)
        st.success("Added")

    try:
        df=pd.read_csv("productivity_data.csv",
        names=["Date","Day","Study Hours","Sleep Hours","Screen Time"])

        st.dataframe(df)
        st.bar_chart(df[["Study Hours","Sleep Hours","Screen Time"]])

        delete_index=st.selectbox("Delete",df.index)

        if st.button("Delete Productivity"):
            df=df.drop(delete_index)
            df.to_csv("productivity_data.csv",index=False,header=False)
            st.rerun()

    except:
        st.write("No data")

# ================= Todo =================

elif option == "To-Do List":

    st.subheader("📝 To Do")

    date=st.date_input("Date",datetime.date.today())

    try:
        df=pd.read_csv("todo.csv")
    except:
        df=pd.DataFrame(columns=["Date","Task","Completed"])

    task=st.text_input("Task")

    if st.button("Add Task"):
        new={"Date":str(date),"Task":task,"Completed":0}
        df=pd.concat([df,pd.DataFrame([new])])
        df.to_csv("todo.csv",index=False)
        st.rerun()

    day=df[df["Date"]==str(date)]

    for i in day.index:
        checked=st.checkbox(
            df.loc[i,"Task"],
            value=df.loc[i,"Completed"]==1,
            key=f"task{i}"
        )
        df.loc[i,"Completed"]=int(checked)

    df.to_csv("todo.csv",index=False)

    total=len(day)
    done=len(day[day["Completed"]==1])

    if total>0:
        st.progress(done/total)

# ================= Calendar =================

elif option=="Calendar":

    from streamlit_calendar import calendar

    events=[]

    try:
        df=pd.read_csv("study_data.csv",
        names=["Date","Day","Subject","Hours"])

        df["Date"]=pd.to_datetime(df["Date"])

        for _,row in df.iterrows():
            events.append({
                "title":f"📚 {row['Subject']}",
                "start":row["Date"].strftime("%Y-%m-%d")
            })
    except:
        pass

    calendar(events=events)