import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض جدول الورديات منظماً بأعمدة واضحة:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    all_rows = []
    
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                line_str = line.strip()
                parts = line_str.split()
                # التقاط الأسطر الخاصة بالورديات التي تبدأ برقم الموقف (Pos) وتتضمن أوقات أو بيانات
                if parts and parts[0].isdigit() and len(parts) >= 2:
                    pos_val = parts[0]
                    shift_details = "   |   ".join(parts[1:])
                    all_rows.append({
                        "الصفحة": page_idx + 1,
                        "Pos (الموقف)": pos_val,
                        "تفاصيل الورديات والأوقات": shift_details
                    })

    if all_rows:
        df = pd.DataFrame(all_rows)
        
        st.success("تم استخراج وترتيب جدول الورديات بنجاح!")
        
        # خانة بحث فورية للوصول لأي موقف أو وردية بسرعة
        search_query = st.text_input("🔍 ابحث برقم الموقف (Pos) أو الوقت (مثال: 1, 2, 700):")
        if search_query:
            df = df[df['Pos (الموقف)'].str.contains(search_query) | df['تفاصيل الورديات والأوقات'].str.contains(search_query, case=False)]
            
        # عرض الجدول بشكل أنيق ومناسب للهاتف
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("لم يتم العثور على أسطر جدول مطابقة، جاري عرض النصوص الكاملة:")
        full_text = "".join([p.extract_text() or "" for p in reader.pages])
        st.text_area("محتوى الملف:", full_text, height=400)

except Exception as e:
    st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
