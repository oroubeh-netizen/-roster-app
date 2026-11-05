import streamlit as st
import pandas as pd
pdfplumber_available = True
try:
    import pdfplumber
except ImportError:
    pdfplumber_available = False

st.set_page_config(page_title="Angered Roster Exact View", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("النسخة الدقيقة المطابقة لملف الـ PDF الأصلي:")

pdf_path = "2027 Scheman Angered.pdf"

if pdfplumber_available:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page_numbers = list(range(1, len(pdf.pages) + 1))
            selected_page = st.selectbox("📄 اختر الصفحة المطلوبة من الجدول:", page_numbers)
            
            page = pdf.pages[selected_page - 1]
            tables = page.extract_tables()
            
            st.success(f"تم قراءة الصفحة رقم {selected_page} بدقة عالية بنجاح!")
            
            if tables:
                for idx, table in enumerate(tables):
                    df_table = pd.DataFrame(table)
                    st.dataframe(df_table, use_container_width=True)
            else:
                # في حال لم يتم التقاط جدول حدودي، نعرض النص المنظم بدقة تامة بناءً على الكوردينات
                text = page.extract_text(layout=True)
                st.code(text, language="text")
                
    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف عبر pdfplumber: {e}")
else:
    st.warning("الرجاء إضافة `pdfplumber` إلى ملف `requirements.txt` لضمان قراءة الجداول المعقدة بدقة.")
