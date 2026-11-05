import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("استعراض والبحث في بيانات جدول الورديات المستخرج من ملف الـ PDF:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    all_rows = []
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                all_rows.append({"الصفحة": index + 1, "محتوى السطر": line})

    df_pdf = pd.DataFrame(all_rows)
    
    st.success("تم قراءة وترتيب محتوى الملف بنجاح!")
    
    # إضافة خانة بحث ذكية للوصول إلى رقم جدول أو وقت معين (مثل 700 أو 701 أو أوقات الورديات)
    search_query = st.text_input("🔍 ابحث عن رقم وردية أو وقت (مثال: 703 أو 4:00):")
    
    if search_query:
        df_pdf = df_pdf[df_pdf['محتوى السطر'].str.contains(search_query, case=False, na=False)]
        st.info(f"نتائج البحث عن: '{search_query}'")

    # عرض البيانات في جدول تفاعلي منظم
    st.subheader("📊 جدول بيانات الورديات:")
    st.dataframe(df_pdf, use_container_width=True)

except Exception as e:
    st.warning("الرجاء التأكد من رفع ملف الـ PDF بالشكل الصحيح في المستودع.")
