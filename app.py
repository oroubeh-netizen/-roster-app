import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض الجدول بالكامل مع إبقاء الأرقام والبيانات مجتمعة في نفس الخلية كما هي في ملف الـ PDF:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    page_numbers = list(range(1, len(reader.pages) + 1))
    selected_page = st.selectbox("📄 اختر الصفحة المطلوبة من جدول الـ PDF:", page_numbers)
    
    page = reader.pages[selected_page - 1]
    # استخدام استخراج التخطيط للحفاظ على المواقع الأصلية للأعمدة
    text = page.extract_text(extraction_mode="layout")
    
    lines = text.split('\n')
    table_rows = []
    
    for line in lines:
        stripped = line.strip()
        # تقسيم الأجزاء بناءً على المسافات الكبيرة بين الأعمدة في ملف الـ PDF
        parts = re.split(r'\s{2,}', stripped)
        if parts and parts[0].isdigit():
            row_data = {"Pos": parts[0]}
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for idx, day in enumerate(days):
                if idx + 1 < len(parts):
                    # دمج النصوص المتعددة في نفس الخلية إن وجدت بنفس الترتيب
                    row_data[day] = parts[idx + 1]
                else:
                    row_data[day] = ""
            table_rows.append(row_data)

    if table_rows:
        df = pd.DataFrame(table_rows)
        st.success(f"تم تحميل الجدول وتنسيق الخانات للصفحة رقم {selected_page} بنجاح!")
        
        # جدول تفاعلي يتيح لك رؤية كل الأرقام داخل الخلية وتعديلها بكل مرونة
        edited_df = st.data_editor(df, use_container_width=True, key=f"exact_grid_p{selected_page}")
        
        st.info("💡 جميع الأرقام والورديات مرتبة الآن في نفس الخلية تماماً كما هي في الملف الأصلي، ويمكنك النقر وتعديل أي خانة بسهولة.")
    else:
        st.warning("هذه الصفحة تحتوي على نصوص ترويجية أو إدارية، وإليك التخطيط الأصلي للنص:")
        st.code(text, language="text")

except Exception as e:
    st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
