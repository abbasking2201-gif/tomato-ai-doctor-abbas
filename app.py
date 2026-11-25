
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
import base64

with open("istockphoto-1927716071-612x612.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(
            rgba(0,0,0,0.35 ),
            rgba(0,0,0,0.55)
        ), url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# Disease information: Arabic and English
diseases = {
    "Tomato_Bacterial_spot": {
        "ar": ("التبقع البكتيري",
               "بقع صغيرة داكنة على الأوراق، وقد تتحول إلى اللون الأصفر وتسقط الأوراق.",
               "تسببه بكتيريا تنتشر غالباً مع رذاذ الماء والأدوات والنباتات المصابة.",
               "إزالة الأوراق المصابة، تجنب تبليل الأوراق أثناء الري، استخدام بذور وشتلات سليمة، وتعقيم الأدوات."),
        "en": ("Bacterial Spot",
               "Small dark spots on leaves, sometimes surrounded by yellow areas. Leaves may fall.",
               "Caused by bacteria that spread through water splash, tools and infected plants.",
               "Remove infected leaves, avoid overhead irrigation, use healthy seedlings and sanitize tools.")
    },
    "Tomato_Early_blight": {
        "ar": ("اللفحة المبكرة",
               "بقع بنية دائرية على الأوراق، غالباً تظهر بشكل حلقات متداخلة.",
               "يسببها فطر Alternaria، وتساعد الرطوبة وبقايا النباتات المصابة على انتشارها.",
               "إزالة الأوراق المصابة، تحسين التهوية، تجنب الري فوق الأوراق، وتدوير المحاصيل."),
        "en": ("Early Blight",
               "Brown circular leaf spots, often showing concentric rings.",
               "Caused by Alternaria fungus. Humidity and infected plant debris help it spread.",
               "Remove infected leaves, improve airflow, avoid overhead watering and rotate crops.")
    },
    "Tomato_Late_blight": {
        "ar": ("اللفحة المتأخرة",
               "بقع مائية داكنة تتوسع بسرعة، وقد يظهر نمو أبيض أسفل الورقة في الظروف الرطبة.",
               "يسببها كائن شبيه بالفطريات يسمى Phytophthora infestans، وينتشر بسرعة في الجو البارد الرطب.",
               "إزالة النباتات المصابة بشدة، تحسين التهوية، عدم ترك الأوراق مبللة، ومراقبة المحصول باستمرار."),
        "en": ("Late Blight",
               "Dark water-soaked lesions that spread rapidly. White growth may appear underneath in humid conditions.",
               "Caused by the fungus-like organism Phytophthora infestans, favored by cool, wet weather.",
               "Remove severely infected plants, improve ventilation, keep foliage dry and monitor crops frequently.")
    },
    "Tomato_Leaf_Mold": {
        "ar": ("عفن أوراق الطماطة",
               "بقع صفراء على السطح العلوي للأوراق، وقد يظهر نمو زيتوني أو مخملي أسفلها.",
               "يسببه فطر Passalora fulva، وتساعد الرطوبة العالية وضعف التهوية على انتشاره.",
               "تقليل الرطوبة، تحسين التهوية، إزالة الأوراق المصابة، وتجنب ازدحام النباتات."),
        "en": ("Leaf Mold",
               "Yellow patches on the upper leaf surface, with olive or velvety growth underneath.",
               "Caused by Passalora fulva fungus, favored by high humidity and poor airflow.",
               "Reduce humidity, improve ventilation, remove infected leaves and avoid overcrowding.")
    },
    "Tomato_Septoria_leaf_spot": {
        "ar": ("تبقع أوراق السبتوريا",
               "بقع صغيرة دائرية ذات مركز رمادي أو فاتح وحواف داكنة.",
               "يسببه فطر Septoria lycopersici، وينتشر مع الماء وبقايا النباتات المصابة.",
               "إزالة الأوراق المصابة، تنظيف بقايا المحصول، الري قرب سطح التربة وتدوير المحاصيل."),
        "en": ("Septoria Leaf Spot",
               "Small circular spots with pale gray centers and dark margins.",
               "Caused by Septoria lycopersici fungus and spread by water and infected plant debris.",
               "Remove infected leaves, clean crop debris, water near the soil and rotate crops.")
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "ar": ("أضرار العنكبوت الأحمر",
               "نقاط صفراء دقيقة على الأوراق، وقد يظهر نسيج عنكبوتي رقيق مع جفاف الأوراق.",
               "تسببها حشرة العنكبوت الأحمر الدقيقة، وتزداد الإصابة في الأجواء الحارة والجافة.",
               "فحص أسفل الأوراق، إزالة الأجزاء شديدة الإصابة، تقليل الغبار ومراقبة انتشار الآفة."),
        "en": ("Spider Mites",
               "Fine yellow speckling on leaves. Webbing and leaf drying may occur in severe infestations.",
               "Caused by tiny spider mites, which often increase in hot and dry conditions.",
               "Inspect leaf undersides, remove heavily infested parts, reduce dust and monitor populations.")
    },
    "Tomato__Target_Spot": {
        "ar": ("التبقع الهدف",
               "بقع بنية دائرية قد تظهر عليها حلقات متداخلة، وقد تصيب الأوراق والسيقان والثمار.",
               "يسببه فطر Corynespora cassiicola، وتساعد الرطوبة وبلل الأوراق على انتشاره.",
               "إزالة الأجزاء المصابة، تحسين التهوية، تجنب الري فوق الأوراق وتنظيف بقايا النباتات."),
        "en": ("Target Spot",
               "Brown circular lesions that may show concentric rings and affect leaves, stems and fruit.",
               "Caused by Corynespora cassiicola fungus, favored by humidity and wet foliage.",
               "Remove infected parts, improve airflow, avoid overhead irrigation and clear plant debris.")
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "ar": ("فيروس تجعد واصفرار أوراق الطماطة",
               "اصفرار الأوراق الحديثة، تجعدها للأعلى، وصغر حجم النبات وضعف نموه.",
               "يسببه فيروس ينتقل غالباً بواسطة الذبابة البيضاء.",
               "إزالة النباتات المصابة بشدة، مكافحة الذبابة البيضاء بطرق الإدارة المتكاملة، وإزالة الأعشاب المضيفة."),
        "en": ("Tomato Yellow Leaf Curl Virus",
               "Yellowing of young leaves, upward curling, stunted growth and reduced plant size.",
               "Caused by a virus commonly transmitted by whiteflies.",
               "Remove severely infected plants, manage whiteflies using integrated pest management and remove weed hosts.")
    },
    "Tomato__Tomato_mosaic_virus": {
        "ar": ("فيروس موزاييك الطماطة",
               "ظهور تلوّن أخضر فاتح وداكن بشكل فسيفسائي، مع تشوه الأوراق وضعف النمو أحياناً.",
               "يسببه فيروس ينتقل عبر العصارة النباتية والأيدي والأدوات والمواد النباتية المصابة.",
               "استخدام بذور سليمة، تعقيم الأدوات، غسل اليدين، وإزالة النباتات المصابة."),
        "en": ("Tomato Mosaic Virus",
               "Light and dark green mosaic patterns, sometimes with distorted leaves and reduced growth.",
               "Caused by a virus spread through plant sap, hands, tools and infected plant material.",
               "Use healthy seeds, sanitize tools, wash hands and remove infected plants.")
    },
    "Tomato_healthy": {
        "ar": ("ورقة سليمة",
               "تبدو الورقة خضراء وطبيعية دون علامات واضحة للمرض في الصورة.",
               "لم تظهر علامات واضحة لأحد الأمراض العشرة التي تدرب عليها النموذج.",
               "استمر بالري والتسميد المتوازن، وراقب الأوراق باستمرار للكشف المبكر عن أي تغير."),
        "en": ("Healthy Leaf",
               "The leaf appears green and normal, with no obvious disease symptoms in the image.",
               "No clear signs of the ten diseases learned by the model were detected.",
               "Maintain balanced irrigation and fertilization, and inspect leaves regularly for early changes.")
    }
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
st.write("Smart AI system for tomato leaf disease diagnosis")
st.write("نظام ذكي لتشخيص أمراض أوراق الطماطة")

language = st.selectbox(
    "اختر اللغة | Choose Language",
    ["العربية", "English"]
)

uploaded_file = st.file_uploader(
    "ارفع صورة ورقة الطماطة | Upload a tomato leaf image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="صورة الورقة | Leaf Image",
             use_container_width=True)

    if st.button("🔍 ابدأ التشخيص | Start Diagnosis"):
        with st.spinner("جاري تحليل الصورة... Please wait"):
            resized = image.resize((224, 224))
            array = np.array(resized, dtype=np.float32)
            array = tf.keras.applications.mobilenet_v2.preprocess_input(array)
            array = np.expand_dims(array, axis=0)

            predictions = model.predict(array, verbose=0)[0]
            top_indices = np.argsort(predictions)[::-1][:3]

        st.success("اكتمل التشخيص | Diagnosis Complete")

        best_index = int(top_indices[0])
        best_disease = class_names[best_index]
        confidence = float(predictions[best_index]) * 100

        info = diseases.get(best_disease)

        if info:
            name, symptoms, cause, treatment = info[
                "ar" if language == "العربية" else "en"
            ]

            st.header("نتيجة التشخيص | Diagnosis Result")
            st.subheader(name)
            st.metric("نسبة الثقة | Confidence", f"{confidence:.2f}%")

            st.subheader("الأعراض | Symptoms")
            st.write(symptoms)

            st.subheader("الأسباب | Causes")
            st.write(cause)

            st.subheader("المكافحة والوقاية | Management")
            st.write(treatment)

        st.divider()
        st.subheader("أعلى ثلاث نتائج | Top 3 Predictions")

        for index in top_indices:
            disease = class_names[int(index)]
            arabic_name, english_name = diseases.get(
                disease, {}
            ).get("ar", (disease, "", "", ""))[0:1] + ("", "", "") if False else (
                diseases[disease]["ar"][0],
                diseases[disease]["en"][0]
            )
            display_name = arabic_name if language == "العربية" else english_name
            score = float(predictions[index])
            st.write(f"**{display_name} — {score * 100:.2f}%**")
            st.progress(score)

        st.warning(
            "تنبيه: النتائج تقديرية وليست تشخيصاً مخبرياً مؤكداً. "
            "قد تتشابه أعراض الأمراض، لذا يُنصح بفحص النبات ميدانياً."
            if language == "العربية" else
            "Note: Results are estimates, not confirmed laboratory diagnoses. "
            "Disease symptoms can overlap, so field inspection is recommended."
        )

st.divider()
st.caption("Developed by Abbas Fadhil | Smart Agricultural Engineering")
