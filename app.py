import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الورديات - Angered", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض وإدارة ورديات السائقين وحساب الساعات والأوقات أوتوماتيكياً.")

if "rosters" not in st.session_state:
    st.session_state.rosters = {
        "Roster 700 (Produktionssupport)": [
            {"pos": "1", "shifts": ["03:45 - 11:52", "11:52 - 19:48", "03:45 - 11:52", "11:52 - 19:48", "03:45 - 11:52", "OFF", "OFF"]},
            {"pos": "2", "shifts": ["04:00 - 12:34", "12:34 - 20:42", "04:00 - 12:34", "12:34 - 20:42", "04:00 - 12:34", "OFF", "OFF"]}
        ],
        "Roster 701 (Var tredje helg)": [
            {"pos": "1", "shifts": ["03:58 - 12:23", "12:42 - 13:22", "04:18 - 09:43", "10:51 - 11:34", "03:58 - 12:23", "OFF", "05:08 - 13:16"]},
            {"pos": "2", "shifts": ["OFF", "04:30 - 13:36", "14:29 - 15:32", "04:30 - 13:36", "13:41 - 22:07", "04:18 - 09:39", "OFF"]}
        ]
    }

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def calculate_shift_duration(shift_str):
    if "OFF" in shift_str or "-" not in shift_str:
        return 0.0
    try:
        parts = shift_str.split("-")
        sh, sm = map(int, parts[0].strip().split(':'))
        eh, em = map(int, parts[1].strip().split(':'))
        start_min, end_min = sh * 60 + sm, eh * 60 + em
        if end_min < start_min: end_min += 24 * 60
        return (end_min - start_min) / 60.0
    except:
        return 0.0

selected_roster = st.selectbox("اختر الجدول المطلوب:", list(st.session_state.rosters.keys()))
rows_data = st.session_state.rosters[selected_roster]

table_rows = []
for r in rows_data:
    row_dict = {"Pos": r["pos"]}
    total_h = 0.0
    for d_idx, day in enumerate(days):
        shift_val = r["shifts"][d_idx]
        row_dict[day] = shift_val
        total_h += calculate_shift_duration(shift_val)
    h = int(total_h)
m = int(round((total_h - h) * 60))

    row_dict["Weekly Work"] = f"{h}h {m:02d}m"
    table_rows.append(row_dict)

st.dataframe(pd.DataFrame(table_rows), use_container_width=True)
