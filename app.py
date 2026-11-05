import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("استعراض كافة الجداول والبيانات المستخرجة من ملف الـ PDF الخاص بك.")

# اسم ملف الـ PDF الذي رفعته مسبقاً
pdf_path = "2027 Scheman Angered.pdf"

try:
    # قراءة الملف المستضاف في المشروع تلقائياً
    reader = PdfReader(pdf_path)
    full_text = ""
    
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n\n--- [ الصفحة رقم {index + 1} ] ---\n" + text

    st.success("تم قراءة جميع صفحات ملف الـ PDF بنجاح!")
    
    # عرض النصوص والجدول الكامل المستخرج
    st.subheader("📄 محتوى الجداول الكاملة من الملف:")
    st.text_area("النصوص المستخرجة من الـ PDF:", full_text, height=450)

except Exception as e:
    st.warning("الرجاء التأكد من وجود ملف الـ PDF في المستودع أو إعادة رفعه عبر الزر أدناه:")
    uploaded_file = st.file_uploader("اختر ملف الـ PDF", type=["pdf"])
    
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        full_text = ""
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n\n--- [ الصفحة رقم {index + 1} ] ---\n" + text
        st.text_area("محتوى الملف المرفوع:", full_text, height=450)
