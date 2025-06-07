
import streamlit as st
import pandas as pd
from pulp import *

st.title("AIシフト自動作成ツール")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    days = list(range(7))
    staffs = {}

    for _, row in df.iterrows():
        name = row['名前']
        hope = int(row['希望日数'])
        possible_days = [int(d) for d in str(row['出勤可能日']).split(',')]
        staffs[name] = {"希望日数": hope, "出勤可能日": possible_days}

    required_per_day = st.slider("1日に必要な人数", 1, 5, 2)

    prob = LpProblem("Shift", LpMaximize)
    x = {(s, d): LpVariable(f"{s}_{d}", cat="Binary") for s in staffs for d in days}

    prob += lpSum([x[s, d] for s in staffs for d in days if d in staffs[s]["出勤可能日"]])
    for s in staffs:
        prob += lpSum([x[s, d] for d in days if d in staffs[s]["出勤可能日"]]) <= staffs[s]["希望日数"]
    for d in days:
        prob += lpSum([x[s, d] for s in staffs if d in staffs[s]["出勤可能日"]]) == required_per_day

    if st.button("シフトを自動作成"):
        prob.solve()
        results = {d: [] for d in days}
        for d in days:
            for s in staffs:
                if value(x[s, d]) == 1:
                    results[d].append(s)

        st.subheader("シフト結果")
        for d in days:
            st.write(f"Day {d}: {', '.join(results[d])}")
