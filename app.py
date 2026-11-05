import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(page_title="Angered Roster Excel View", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض الجدول بنظام شبكي يشبه ملف الإكسل (Excel Grid) يجمع تفاصيل كل وردية وأوقاتها وأرقام الـ Tjänst في خاناتها الأصلية:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    # اختيار الصفحة المطلوبة من الـ PDF
    page_numbers = list(range(1, len(reader.pages) + 1))
    selected_page = st.selectbox("📄 اختر الصفحة المطلوبة:", page_numbers)
    
    page = reader.pages[selected_page - 1]
    text = page.extract_text(extraction_mode="layout")
    
    lines = text.split('\n')
    grid_rows = {}
    
    # استخراج وتجميع البيانات لكل موقف (Pos) وأيام الأسبوع
    current_pos = None
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    for line in lines:
        stripped = line.strip()
        parts = re.split(r'\s{2,}', stripped)
        
        # التقاط صف الموقف (Pos)
        if parts and parts[0].isdigit() and len(parts) >= 2:
            current_pos = parts[0]
            if current_pos not in grid_rows:
                grid_rows[current_pos] = {day: [] for day in days}
                
        # تجميع محتويات الخانات الأفقية للأيام
        elif current_pos and len(stripped) > 0:
            # توجيه النصوص وتوزيعها على الأيام بناءً على التخطيط
            for i, day in enumerate(days):
                if i + 1 < len(parts) and parts[i+1]:
                    grid_rows[current_pos][day].append(parts[i+1])

    # تحويل البيانات إلى هيكل إكسل شبكي (DataFrame)
    table_data = []
    for pos, day_dict in grid_rows.items():
        row = {"Pos": pos}
        for day in days:
            # دمج تفاصيل الخلية الواحدة (الأوقات، رقم التورديات Tjänst، والراحة) بترتيبها
            cell_content = "\n".join(day_dict[day]) if day_dict[day] else "OFF"
            row[day] = cell_content
        table_data.append(row)

    if table_data:
        df_excel = pd.DataFrame(table_data)
        
        st.success(f"تم إنشاء شبكة الجدول بنجاح للصفحة رقم {selected_page}!")
        
        # عرض الجدول بشكل شبكي تفاعلي يشبه الإكسل مع إمكانية التعديل
        edited_excel = st.data_editor(df_excel, use_container_width=True, key=f"excel_grid_p{selected_page}")
        
        st.info("💡 الخانات الآن مصممة كجدول إكسل متكامل؛ يمكنك رؤية وقت البدء/الانتهاء، رقم Tjänst، وأوقات الراحة مجتمعة في كل خانة، مع إمكانية التعديل المباشر.")
    else:
        st.warning("هذه الصفحة تحتوي على نصوص عامة، وإليك التخطيط الأصلي للنص:")
        st.code(text, language="text")

except Exception as e:
    st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
