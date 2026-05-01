import streamlit as st
import pandas as pd
import joblib

# Page config
st.set_page_config(page_title="Genetic Disorder Predictor", page_icon="🧬", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');
   
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
    }
    .main {
        background-color: #f0f4f8;
    }
    .stButton>button {
        background-color: #1a1a2e;
        color: white;
        border-radius: 8px;
        padding: 0.6em 2em;
        font-size: 16px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #16213e;
    }
    .result-box {
        background-color: #1a1a2e;
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 1rem;
    }
    .result-box h2 {
        color: #00d4aa;
        font-size: 1.2rem;
        margin-bottom: 0.2rem;
    }
    .result-box h1 {
        color: white;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    .divider {
        border-top: 1px solid #ffffff33;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load model and columns
@st.cache_resource
def load_model():
    model = joblib.load('genetic_disorder_model.pkl')
    columns = joblib.load('model_columns.pkl')
    return model, columns

model, model_columns = load_model()

# Disorder mapping
disorder_map = {
    'Leigh syndrome': 'Mitochondrial genetic inheritance disorders',
    'Mitochondrial myopathy': 'Mitochondrial genetic inheritance disorders',
    'Cystic fibrosis': 'Single-gene inheritance diseases',
    'Tay-Sachs': 'Single-gene inheritance diseases',
    'Hemochromatosis': 'Single-gene inheritance diseases',
    "Leber's hereditary optic neuropathy": 'Single-gene inheritance diseases',
    'Diabetes': 'Multifactorial genetic inheritance disorders'
}

# Header
st.markdown("<h1 style='text-align:center;'>🧬 Genetic Disorder Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Enter patient details below to predict the genetic disorder subclass</p>", unsafe_allow_html=True)
st.markdown("---")

# Input form
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Patient Info")
    patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Ambiguous"])
    blood_cell = st.number_input("Blood Cell Count (mcL)", min_value=0.0, value=5000.0)
    wbc = st.number_input("White Blood Cell Count (thousand/µL)", min_value=0.0, value=7.0)
    symptom1 = st.number_input("Symptom 1", min_value=0, max_value=10, value=0)
    symptom2 = st.number_input("Symptom 2", min_value=0, max_value=10, value=0)
    symptom3 = st.number_input("Symptom 3", min_value=0, max_value=10, value=0)
    symptom4 = st.number_input("Symptom 4", min_value=0, max_value=10, value=0)
    symptom5 = st.number_input("Symptom 5", min_value=0, max_value=10, value=0)

with col2:
    st.subheader("👨‍👩‍👧 Family Info")
    mothers_age = st.number_input("Mother's Age", min_value=0, max_value=100, value=30)
    fathers_age = st.number_input("Father's Age", min_value=0, max_value=100, value=32)
    genes_mother = st.selectbox("Genes in Mother's Side", ["Yes", "No"])
    inherited_father = st.selectbox("Inherited from Father", ["Yes", "No"])
    maternal_gene = st.selectbox("Maternal Gene", ["Yes", "No"])
    paternal_gene = st.selectbox("Paternal Gene", ["Yes", "No"])
    prev_abortions = st.number_input("No. of Previous Abortions", min_value=0, max_value=20, value=0)
    history_anomalies = st.selectbox("History of Anomalies in Previous Pregnancies", ["Yes", "No"])

with col3:
    st.subheader("🏥 Medical History")
    respiratory_rate = st.selectbox("Respiratory Rate (breaths/min)", ["Normal (30-60)", "Tachypnea"])
    heart_rate = st.selectbox("Heart Rate (rates/min)", ["Normal", "Tachycardia"])
    parental_consent = st.selectbox("Parental Consent", ["Yes"])
    follow_up = st.selectbox("Follow-up", ["Low", "High"])
    birth_asphyxia = st.selectbox("Birth Asphyxia", ["No", "Yes", "No record", "Not available"])
    autopsy = st.selectbox("Autopsy Shows Birth Defect", ["Not applicable", "No", "Not Performed", "Yes"])
    folic_acid = st.selectbox("Folic Acid Details (peri-conceptional)", ["Yes", "No"])
    maternal_illness = st.selectbox("H/O Serious Maternal Illness", ["Yes", "No"])
    radiation = st.selectbox("H/O Radiation Exposure (x-ray)", ["Not applicable", "Yes", "No", "-"])
    substance_abuse = st.selectbox("H/O Substance Abuse", ["-", "No", "Yes", "Not applicable"])
    ivf = st.selectbox("Assisted Conception IVF/ART", ["Yes", "No"])
    birth_defects = st.selectbox("Birth Defects", ["Multiple", "Singular"])
    blood_test = st.selectbox("Blood Test Result", ["slightly abnormal", "abnormal", "normal", "inconclusive"])

st.markdown("---")

# Predict button
if st.button("🔍 Predict Genetic Disorder"):
    input_dict = {
        'Patient Age': patient_age,
        "Genes in mother's side": genes_mother,
        'Inherited from father': inherited_father,
        'Maternal gene': maternal_gene,
        'Paternal gene': paternal_gene,
        'Blood cell count (mcL)': blood_cell,
        "Mother's age": mothers_age,
        "Father's age": fathers_age,
        'Respiratory Rate (breaths/min)': respiratory_rate,
        'Heart Rate (rates/min)': heart_rate,
        'Parental consent': parental_consent,
        'Follow-up': follow_up,
        'Gender': gender,
        'Birth asphyxia': birth_asphyxia,
        'Autopsy shows birth defect (if applicable)': autopsy,
        'Folic acid details (peri-conceptional)': folic_acid,
        'H/O serious maternal illness': maternal_illness,
        'H/O radiation exposure (x-ray)': radiation,
        'H/O substance abuse': substance_abuse,
        'Assisted conception IVF/ART': ivf,
        'History of anomalies in previous pregnancies': history_anomalies,
        'No. of previous abortion': prev_abortions,
        'Birth defects': birth_defects,
        'White Blood cell count (thousand per microliter)': wbc,
        'Blood test result': blood_test,
        'Symptom 1': symptom1,
        'Symptom 2': symptom2,
        'Symptom 3': symptom3,
        'Symptom 4': symptom4,
        'Symptom 5': symptom5,
    }

    input_df = pd.DataFrame([input_dict])
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
    prediction = model.predict(input_encoded)[0]
    genetic_disorder_type = disorder_map.get(prediction, 'Unknown')

    st.markdown(f"""
        <div class="result-box">
            <h2>🧬 Genetic Disorder Type</h2>
            <h1>{genetic_disorder_type}</h1>
            <div class="divider"></div>
            <h2>🔬 Disorder Subclass</h2>
            <h1>{prediction}</h1>
        </div>
    """, unsafe_allow_html=True)
