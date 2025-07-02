import streamlit as st
import os
from utils.prompt_parser import extract_industry_and_topic
from utils.scraper import scrape_cloud_page, scrape_industry_case_studies
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Cloud Migration Expertise - Agent42Labs", layout="wide")

# --- Custom CSS for Agent42Labs-style branding ---
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f2f6fc;
        }
        h1, h2, h3, h4 {
            color: #002e5d;
        }
        .stButton>button {
            background-color: #002e5d;
            color: white;
            font-weight: 600;
            border-radius: 6px;
            padding: 0.5rem 1rem;
        }
        .case-card {
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            padding: 1rem;
            background-color: white;
            transition: 0.3s;
            border: 1px solid #e1e8f0;
        }
        .case-card:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }
        img {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.title("🚀 Cloud Migration Expertise Page Generator")
st.subheader("Tailored by AI · Powered by Agent42Labs")

# --- User Form ---
with st.form("user_input_form"):
    col1, col2 = st.columns([1, 3])
    with col1:
        name = st.text_input("👤 Your Name")
    with col2:
        prompt = st.text_area("🧠 Describe your business need", placeholder="E.g. I'm in healthcare and need help with cloud migration", height=100)
    submitted = st.form_submit_button("Generate My Page")

# --- Output Section ---
if submitted:
    if not name or not prompt:
        st.error("Please enter both your name and your business need.")
    else:
        try:
            industry, topic = extract_industry_and_topic(prompt)
            st.success(f"🎯 Detected Industry: **{industry.capitalize()}**, Topic: **{topic}**")

            cloud_text = scrape_cloud_page()
            industry_url = f"https://agent42labs.com/{industry.lower()}/"
            case_studies = scrape_industry_case_studies(industry_url)

            st.markdown("---")
            st.markdown(f"## 👋 Welcome, {name}")
            st.markdown(f"**Your Prompt:** _{prompt}_")

            st.markdown("---")
            st.markdown(f"""
### 🧠 Cloud Strategy for {industry.capitalize()}

> Based on your need for **{topic}** in the **{industry}** sector, here’s your custom strategy guide — combining Agent42Labs insights and real-world success.

---

### ☁️ Why Cloud Matters in {industry.capitalize()}
- Secure and scalable infrastructure
- Real-time data analytics
- Enhanced compliance and governance
- AI/ML-ready environments

---

### 💡 Agent42Labs Cloud Migration Expertise
""")

            with st.expander("📘 Summary from Agent42Labs Cloud Consulting Page"):
                st.write(cloud_text)

            st.markdown("---")
            st.markdown(f"### 🧪 Successful Case Studies in {industry.capitalize()}")
            if case_studies:
                cols = st.columns(3)
                for i, case in enumerate(case_studies):
                    with cols[i % 3]:
                        st.markdown(f"""
                            <div class='case-card'>
                                <img src="{case['image']}" width="100%"/>
                                <h4>{case['title']}</h4>
                                <p>{case['summary']}</p>
                                <a href="{case['link']}" target="_blank">🔗 Read More</a>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("🚫 No case studies found for this industry.")
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
