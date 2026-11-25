
import streamlit as st
import tensorflow as tf
import numpy as np
import json
from PIL import Image

st.set_page_config(
    page_title="Tomato AI Doctor",
    page_icon="🍅",
    layout="centered"
)

translations = {
    "Tomato_Bacterial_spot": ("التبقع البكتيري", "Bacterial Spot"),
    "Tomato_Early_blight": ("اللفحة المبكرة", "Early Blight"),
    "Tomato_Late_blight": ("اللفحة المتأخرة", "Late Blight"),
    "Tomato_Leaf_Mold": ("عفن الأوراق", "Leaf Mold"),
    "Tomato_Septoria_leaf_spot": ("تبقع أوراق السبتوريا", "Septoria Leaf Spot"),
    "Tomato_Spider_mites_Two_spotted_spider_mite": ("أضرار العنكبوت الأحمر", "Spider Mites"),
    "Tomato__Target_Spot": ("التبقع الهدف", "Target Spot"),
    "Tomato__Tomato_YellowLeaf__Curl_Virus": ("فيروس تجعد واصفرار الأوراق", "Tomato Yellow Leaf Curl Virus"),
    "Tomato__Tomato_mosaic_virus": ("فيروس موزاييك الطماطة", "Tomato Mosaic Virus"),
    "Tomato_healthy": ("ورقة سليمة", "Healthy Leaf")
}

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("tomato_disease_model.keras")

@st.cache_data
def load_classes():
    with open("class_names.json", "r", encoding="utf-8") as f:
        return json.load(f)

model = load_model()
class_names = load_classes()

st.title("🍅 Tomato AI Doctor")
st.subheader("طبيب الطماطة الذكي")
st.write("AI-powered tomato leaf disease diagnosis")
st.write("نظام ذكي لتشخيص أمراض أوراق الطماطة")

language = st.selectbox(
    "Language | اللغة",
    ["العربية", "English"]
)

uploaded_file = st.file_uploader(
    "ارفع صورة ورقة الطماطة | Upload a tomato leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="صورة الورقة | Leaf Image", use_container_width=True)

    if st.button("🔍 ابدأ التشخيص | Start Diagnosis"):
        with st.spinner("جاري تحليل الصورة... Please wait"):
            resized = image.resize((224, 224))
            array = np.array(resized, dtype=np.float32)
            array = tf.keras.applications.mobilenet_v2.preprocess_input(array)
            array = np.expand_dims(array, axis=0)

            predictions = model.predict(array, verbose=0)[0]
            top_indices = np.argsort(predictions)[::-1][:3]

        st.success("اكتمل التشخيص | Diagnosis Complete")

        for rank, index in enumerate(top_indices):
            disease = class_names[index]
            arabic, english = translations.get(
                disease, (disease, disease)
            )
            confidence = float(predictions[index]) * 100

            name = arabic if language == "العربية" else english
            st.write(f"**{rank + 1}. {name}**")
            st.progress(confidence / 100)
            st.write(f"{confidence:.2f}%")

        st.warning(
            "النتيجة تقديرية وتعتمد على جودة الصورة. "
            "يُنصح بالتأكد ميدانياً قبل اتخاذ قرار العلاج."
        )

st.divider()
st.caption("Developed by Abbas Fadhil | Smart Agricultural Engineering")
