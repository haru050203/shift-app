
import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="シフト提出フォーム", layout="wide")

st.title("📝 シフト希望入力（日本語対応）")

st.write("以下のフォームにシフト希望を入力してください。")

name = st.text_input("あなたの名前")
days = st.multiselect("希望する出勤日（複数選択可）", 
                      ["2025-06-10", "2025-06-11", "2025-06-12", "2025-06-13", "2025-06-14"])
shift_times = []
for day in days:
    time = st.text_input(f"{day} の希望時間（例：9:00〜17:00）", key=day)
    shift_times.append((day, time))

num_shifts = st.slider("週の希望出勤回数", 1, 7, 3)
submit = st.button("送信してシフトを自動作成")

if submit:
    st.success("✅ 希望を受け付けました！")
    df = pd.DataFrame({
        "日付": [d[0] for d in shift_times],
        "希望時間": [d[1] for d in shift_times],
        "名前": name
    })

    st.write("### 📋 あなたのシフト希望一覧")
    st.dataframe(df)

    # 仮の自動割当ロジック（例：そのまま反映）
    st.write("### ✅ 自動シフト案（簡易）")
    df["決定シフト"] = df["希望時間"]  # 今はそのまま通す
    st.dataframe(df)

    # PDF出力
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="シフト表（自動作成）", ln=1, align="C")
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['日付']} - {row['名前']}：{row['決定シフト']}", ln=1)

    pdf.output("shift_result.pdf")
    with open("shift_result.pdf", "rb") as f:
        st.download_button("📥 PDFでダウンロード", f, file_name="shift_result.pdf")
