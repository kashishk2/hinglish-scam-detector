import sys
sys.path.insert(0, "src")
import streamlit as st
from predict import load_model, analyze, highlight_html

st.set_page_config(page_title="Hinglish Scam Detector", page_icon="🛡️")

@st.cache_resource
def get_model():
    return load_model()

model = get_model()

st.title("🛡️ Hinglish Scam Message Detector")
st.caption("Paste an SMS / WhatsApp message written in Hinglish and check whether it looks like a scam.")

EXAMPLES = {
    "Fake KYC": "Dear customer, aapka SBI account KYC expire ho gaya hai. Abhi update karein warna account block ho jayega: bit.ly/kyc-upd8",
    "Lottery": "Congratulations! Aapne 25 lakh ki lottery jeeti hai. Claim karne ke liye processing fee 2000 bhejein",
    "Real bank alert": "Rs 850 debited from a/c XX2231 for UPI payment to Dominos. -HDFC Bank",
    "Friend message": "Bhai kal 6 baje cafe mein milte hain, notes bhi le aana",
}

if "text" not in st.session_state:
    st.session_state.text = ""

cols = st.columns(len(EXAMPLES))
for col, (name, msg) in zip(cols, EXAMPLES.items()):
    if col.button(name, use_container_width=True):
        st.session_state.text = msg

text = st.text_area("Message", key="text", height=140, placeholder="Yahan message paste karein...")

if st.button("Check message", type="primary"):
    if not text.strip():
        st.warning("Please enter a message first.")
    else:
        res = analyze(model, text)
        prob = res["probability"]
        if res["label"] == "scam":
            st.error(f"🚨 Likely SCAM  (confidence ≈ {prob:.0%})")
            st.markdown("**Suspicious words:**", help="Words that most increase the scam score")
            st.markdown(highlight_html(res["tokens"], res["flagged"]), unsafe_allow_html=True)
            st.info("Don't click links, share OTP/PIN/CVV, or send money. Real banks never ask for these. "
                    "Report fraud at cybercrime.gov.in or call 1930.")
        else:
            st.success(f"✅ Looks SAFE  (scam probability ≈ {prob:.0%})")
            st.caption("No model is perfect. If a message asks for money, OTP, or personal details, stay cautious.")
