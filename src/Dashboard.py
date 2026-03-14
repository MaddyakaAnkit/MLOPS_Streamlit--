import json
import requests
import streamlit as st
from pathlib import Path
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)
#FASTAPI_BACKEND_ENDPOINT = "http://localhost:8000"
FASTAPI_BACKEND_ENDPOINT = "http://127.0.0.1:8000"


st.set_page_config(page_title="Penguins Prediction Demo", page_icon="🐧")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### Backend status")
    try:
        r = requests.get(FASTAPI_BACKEND_ENDPOINT, timeout=3)
        if r.status_code == 200:
            st.success("Backend online ✅")
            health = r.json()
        else:
            st.warning("Problem connecting 😭")
            health = None
    except requests.ConnectionError as ce:
        LOGGER.error(ce)
        st.error("Backend offline 😱")
        health = None

    st.divider()
    st.markdown("### Input mode")
    mode = st.radio("How do you want to provide inputs?",
                    options=["Sliders", "Upload JSON"], horizontal=True)

    uploaded = None
    if mode == "Upload JSON":
        uploaded = st.file_uploader("Upload penguin features JSON", type=["json"])
        if uploaded:
            try:
                up = json.load(uploaded)
                st.write("Preview:")
                st.json(up)
                st.session_state["HAS_JSON"] = True
            except Exception as e:
                st.error(f"Invalid JSON: {e}")
                st.session_state["HAS_JSON"] = False
        else:
            st.session_state["HAS_JSON"] = False

    predict_btn = st.button("Predict")

# ---------- Body ----------
st.write("# Penguins Prediction 🐧")

# Fetch metadata for slider ranges and class labels
meta = None
try:
    m = requests.get(f"{FASTAPI_BACKEND_ENDPOINT}/meta", timeout=3)
    if m.status_code == 200:
        meta = m.json()
except Exception as e:
    LOGGER.warning(f"Could not fetch /meta: {e}")

if meta is None:
    st.info("Model metadata not available yet. Start the FastAPI server and refresh.")
    st.stop()

FEATURES = meta["features"]
RANGES = meta["ranges"]
CLASSES = meta["classes"]

# Build inputs
def sliders():
    st.info("Use sliders or switch to JSON upload in the sidebar.")
    vals = {}
    for feat in FEATURES:
        r = RANGES[feat]
        vals[feat] = st.slider(
            feat.replace("_", " ").title(),
            min_value=float(r["min"]),
            max_value=float(r["max"]),
            value=float((r["min"] + r["max"]) / 2),
            step=0.1
        )
    return vals

# TABS for nicer UX
tab_pred, tab_about, tab_sample = st.tabs(["🔮 Predict", "ℹ️ About Model", "📄 Sample JSON"])

with tab_pred:
    container = st.empty()

    if predict_btn:
        if mode == "Sliders":
            payload = sliders()  # render sliders and collect values
        else:
            if not st.session_state.get("HAS_JSON"):
                st.error("Please upload a valid JSON file.")
                st.stop()
            # Expect flat JSON with the four numeric keys
            payload = up

        # Normalize keys if user uploaded {"input_test": {...}}
        if "input_test" in payload and isinstance(payload["input_test"], dict):
            payload = payload["input_test"]

        # Validate required keys
        missing = [k for k in FEATURES if k not in payload]
        if missing:
            st.error(f"Missing keys: {missing}. Expected: {FEATURES}")
            st.stop()

        with st.spinner("Predicting..."):
            try:
                res = requests.post(f"{FASTAPI_BACKEND_ENDPOINT}/predict",
                                    json=payload, timeout=6)
                if res.status_code == 200:
                    data = res.json()
                    pred = data["prediction"]
                    probs = data["probabilities"]
                    # Pretty result
                    container.success(f"**Prediction:** {pred}")
                    df = pd.DataFrame({"class": CLASSES, "probability": probs})
                    st.bar_chart(df.set_index("class"))
                else:
                    st.toast(f":red[Server status {res.status_code}]",
                             icon="🔴")
            except Exception as e:
                st.toast(":red[Problem contacting backend. Refresh and check status]",
                         icon="🔴")
                LOGGER.error(e)
    else:
        # Render sliders so user can see ranges even before clicking
        if mode == "Sliders":
            _ = sliders()

with tab_about:
    st.write("**Model:** RandomForestClassifier on Palmer Penguins (numeric features only).")
    st.write(f"**Features:** {', '.join(FEATURES)}")
    if "metrics" in meta and "accuracy" in meta["metrics"]:
        st.metric("Held-out Accuracy", f"{meta['metrics']['accuracy']:.3f}")
    if health:
        st.caption(f"Backend: {health}")

with tab_sample:
    example = {
        "bill_length_mm": 43.2,
        "bill_depth_mm": 17.1,
        "flipper_length_mm": 193.0,
        "body_mass_g": 3600.0
    }
    st.code(json.dumps(example, indent=4), language="json")
    st.caption("You can also wrap this under an 'input_test' key if you prefer.")
