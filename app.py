import os

folder = "/content/drive/MyDrive/Tomato_Project"

app_code = r'''
import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

st.set_page_config(
    page_title="Tomato AI Doctor",
    page_icon="🍅",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    text-align: center;
}
.main-title {
    color: #269447;
    font-size: 34px;
    font-weight: bold;
    text-align: center;
}
.subtitle {
    color: gray;
    text-align: center;
}
.footer {
    text-align: center;
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("tomato_disease_model.keras")

@st.cache_data
def load_classes():
    with open("class_names.json", "r") as f:
        return json.load(f)

translations = {
    "Tomato_Bacterial_spot": ("التبقع البكتيري", "Bacterial Spot"),
    "Tomato_Early_blight": ("اللفحة المبكرة", "Early Blight"),
    "Tomato_Late_blight": ("اللفحة المتأخرة", "Late Blight"),
    "Tomato_Leaf_Mold": ("عفن الأوراق", "Leaf Mold"),
    "Tomato_Septoria_leaf_spot": ("تبقع أوراق السبتوريا", "Septoria Leaf Spot"),
    "Tomato_Spider_mites_Two_spotted_spider_mite": ("أضرار العنكبوت الأحمر", "Spider Mites"),
    "Tomato__Target_Spot": ("التبقع الهدف", "Target Spot"),
    "TomatoTomato_YellowLeafCurl_Virus": ("فيروس تجعد واصفرار الأوراق", "Tomato Yellow Leaf Curl Virus"),
    "Tomato__Tomato_mosaic_virus": ("فيروس موزاييك الطماطة", "Tomato Mosaic Virus"),
    "Tomato_healthy": ("ورقة سليمة", "Healthy Leaf")
}

st.markdown(
    '<div class="main-title">🍅 Tomato AI Doctor</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">الطبيب الذكي لأمراض الطماطة<br>AI System for Tomato Leaf Disease Detection</div>',
    unsafe_allow_html=True
)

st.divider()

st.markdown("### 🌱 مرحباً بك | Welcome")
st.write("ارفع صورة ورقة الطماطة لتشخيص حالتها.")
st.write("Upload a tomato leaf image to detect its condition.")

uploaded_file = st.file_uploader(
    "📷 اختر صورة | Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="الصورة المرفوعة | Uploaded Image",
             use_container_width=True)

    if st.button("🔍 ابدأ التشخيص | Start Diagnosis",
                 use_container_width=True):
        try:
            with st.spinner("جاري تحليل الصورة | Analyzing image..."):
                model = load_model()
                class_names = load_classes()

                resized = image.resize((224, 224))
                arr = np.array(resized, dtype=np.float32)
                arr = preprocess_input(arr)
                arr = np.expand_dims(arr, axis=0)

                predictions = model.predict(arr, verbose=0)[0]
                top_indices = np.argsort(predictions)[::-1][:3]

            best_index = top_indices[0]
            best_name = class_names[best_index]
            arabic, english = translations.get(
                best_name, (best_name, best_name)
            )
            confidence = float(predictions[best_index]) * 100

            st.success("اكتمل التشخيص | Diagnosis Completed")

            st.markdown("### 📋 نتيجة التشخيص | Diagnosis Result")
            st.markdown(f"## {arabic}")
            st.markdown(f"### {english}")
            st.metric(
                "نسبة ثقة النموذج | Model Confidence",
                f"{confidence:.2f}%"
            )

            st.markdown("### أعلى ثلاثة احتمالات | Top 3 Predictions")

            for index in top_indices:
                name = class_names[index]
                ar, en = translations.get(name, (name, name))
                score = float(predictions[index]) * 100

st.write(f"{ar} | {en}")
                st.progress(float(predictions[index]))
                st.caption(f"{score:.2f}%")
                st.info(
                "ملاحظة: النتيجة تقديرية وتحتاج إلى تأكيد زراعي متخصص."
                "\n\nNote: AI predictions are estimates and may require "
                "confirmation by an agricultural specialist."
            )

        except Exception as e:
            st.error(f"حدث خطأ | Error: {e}")

st.divider()

st.markdown("""
<div class="footer">
Developed by Abbas Fadhil<br>
تطوير: عباس فاضل<br>
Smart Agricultural Engineering | هندسة الزراعة الذكية
</div>
""", unsafe_allow_html=True)
'''

with open(os.path.join(folder, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_code)
