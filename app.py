import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("استعراض وتعديل الجداول والأرقام الحقيقية المستخرجة مباشرة من ملف الـ PDF:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    # قائمة لاختيار الصفحة المطلوبة
    page_numbers = list(range(1, len(reader.pages) + 1))
    selected_page = st.selectbox("📄 اختر الصفحة المطلوبة من جدول الـ PDF:", page_numbers)
    
    page = reader.pages[selected_page - 1]
    text = page.extract_text(extraction_mode="layout")
    
    lines = text.split('\n')
    table_rows = []
    
    # تحليل التخطيط لاستخراج الصفوف والأعمدة الحقيقية
    for line in lines:
        stripped = line.strip()
        parts = re.split(r'\s{2,}', stripped)
        if parts and parts[0].isdigit():
            row_data = {"Pos": parts[0]}
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for idx, day in enumerate(days):
                if idx + 1 < len(parts):
                    row_data[day] = parts[idx + 1]
                else:
                    row_data[day] = ""
            table_rows.append(row_data)

    if table_rows:
        df = pd.DataFrame(table_rows)
        st.success(f"تم استخراج الجدول الحقيقي من الصفحة رقم {selected_page} بنجاح!")
        
        # عرض الجدول الشبكي التفاعلي بالبيانات الحقيقية مع إمكانية التعديل والتغيير بين الخانات
        edited_df = st.data_editor(df, use_container_width=True, key=f"real_grid_p{selected_page}")
        
        st.info("💡 يمكنك الآن النقر مباشرة على أي خانة في الجدول أعلاه وتغيير أو تعديل الأرقام والورديات بكل سهولة!")
    else:
        st.warning("هذه الصفحة تحتوي على نصوص تنظيمية، وإليك التخطيط الأصلي للنص تماماً كما هو في الـ PDF:")
        st.code(text, language="text")

except Exception as e:
    st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
