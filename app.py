import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("استعراض جدول الورديات مقسماً بأعمدة منظمة:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            all_text += t + "\n"
            
    lines = all_text.split('\n')
    
    table_rows = []
    current_cycle = "غير محدد"
    
    for line in lines:
        line_str = line.strip()
        if "Cycle:" in line_str:
            current_cycle = line_str
        
        parts = line_str.split()
        # التقاط أسطر الورديات التي تبدأ برقم الموقف (Pos)
        if parts and parts[0].isdigit() and len(parts) >= 2:
            pos = parts[0]
            rest_data = " | ".join(parts[1:])
            table_rows.append({
                "الدورة / الجدول": current_cycle,
                "Pos (الموقف)": pos,
                "تفاصيل الورديات (الأيام والأوقات)": rest_data
            })

    if table_rows:
        df = pd.DataFrame(table_rows)
        
        cycle_options = df["الدورة / الجدول"].unique().tolist()
        selected_cycle = st.selectbox("🎯 اختر الجدول المطلوب:", cycle_options)
        
        filtered_df = df[df["الدورة / الجدول"] == selected_cycle]
        
        st.success("تم تنظيم الجدول وعرضه بنجاح!")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("جاري عرض كافة محتويات الملف:")
        st.dataframe(pd.DataFrame([{"النص": l} for l in lines if l.strip()]), use_container_width=True)

except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
