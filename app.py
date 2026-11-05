import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض جداول الورديات تماماً بنفس تنسيق وتخطيط ملف الـ PDF الأصلي:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    # قائمة لاختيار الصفحة المطلوبة من الـ PDF
    page_numbers = list(range(1, len(reader.pages) + 1))
    selected_page = st.selectbox("📄 اختر الصفحة المطلوبة من الجدول:", page_numbers)
    
    # استخراج النصوص مع الحفاظ على التخطيط والأعمدة الأصلية للـ PDF
    page = reader.pages[selected_page - 1]
    layout_text = page.extract_text(extraction_mode="layout")
    
    st.success(f"تم عرض الصفحة رقم {selected_page} بتنسيق الجدول الأصلي:")
    
    # عرض النصوص بخط ثابت الحجم لضمان بقاء أعمدة الأيام والأوقات محاذاة تماماً كما في الملف
    st.code(layout_text, language="text")

except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
