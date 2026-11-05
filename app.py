import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Angered Roster", layout="wide")

st.title("🚍 نظام إدارة وتبديل جداول الورديات (Angered Roster)")
st.write("عرض واستعراض جداول الورديات المنظمة من ملف الـ PDF الخاص بك:")

pdf_path = "2027 Scheman Angered.pdf"

try:
    reader = PdfReader(pdf_path)
    
    roster_data = []
    current_roster = "غير محدد"
    
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                if "Cycle:" in line or "Roster:" in line:
                    current_roster = line.strip()
                
                if any(day in line for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) or ("1 " in line or "2 " in line or "3 " in line):
                    roster_data.append({
                        "البيانات/الجدول": current_roster,
                        "تفاصيل الوردية والأسطر": line.strip(),
                        "الصفحة": index + 1
                    })

    if roster_data:
        df_roster = pd.DataFrame(roster_data)
        
        search_query = st.text_input("🔍 ابحث عن رقم الجدول أو الموقف (مثال: 700 أو Pos):")
        if search_query:
            df_roster = df_roster[df_roster['تفاصيل الوردية والأسطر'].str.contains(search_query, case=False, na=False) | 
                                  df_roster['البيانات/الجدول'].str.contains(search_query, case=False, na=False)]
        
        st.success("تم استخراج وتنظيم جداول الورديات بنجاح!")
        st.subheader("📊 الجداول المستخرجة:")
        st.dataframe(df_roster, use_container_width=True)
    else:
        st.warning("لم يتم العثور على أنماط جداول مطابقة، سيتم عرض كافة أسطر الملف:")
        all_rows = [{"الصفحة": i+1, "السطر": line} for i, p in enumerate(reader.pages) for line in (p.extract_text() or "").split('\n')]
        st.dataframe(pd.DataFrame(all_rows), use_container_width=True)

except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
