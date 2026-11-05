import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("استعراض جداول الورديات منظمة بأعمدة واضحة من ملف الـ PDF:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            all_text += t + "\n"
            
    lines = all_text.split('\n')
    
    cycles_data = {}
    current_cycle = "جداول عامة"
    current_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "Cycle:" in line:
            if current_rows:
                cycles_data[current_cycle] = current_rows
                current_rows = []
            current_cycle = line
        elif "Pos" in line and "Mon" in line:
            current_rows.append("رأس الجدول: " + line)
            i += 1
            while i < len(lines):
                row_line = lines[i].strip()
                if "Cycle:" in row_line or "Total:" in row_line or "Average:" in row_line:
                    if "Cycle:" in row_line:
                        i -= 1
                    break
                if row_line:
                    current_rows.append(row_line)
                i += 1
        i += 1
    if current_rows:
        cycles_data[current_cycle] = current_rows

    if cycles_data and len(cycles_data) > 1:
        cycle_list = list(cycles_data.keys())
        selected_cycle = st.selectbox("🎯 اختر رقم الجدول أو الدورة (Cycle):", cycle_list)
        
        rows = cycles_data[selected_cycle]
        df_table = pd.DataFrame(rows, columns=["بيانات الورديات والأيام"])
        
        st.success(f"تم تحميل الجدول بنجاح!")
        st.dataframe(df_table, use_container_width=True)
    else:
        # عرض افتراضي منظم في حال عدم مطابقة الشروط الدقيقة
        df_all = pd.DataFrame([{"محتوى الأسطر": l} for l in lines if l.strip()])
        search = st.text_input("🔍 بحث سريـع في الورديات:")
        if search:
            df_all = df_all[df_all['محتوى الأسطر'].str.contains(search, case=False, na=False)]
        st.dataframe(df_all, use_container_width=True)

except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
