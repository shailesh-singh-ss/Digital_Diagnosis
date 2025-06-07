import streamlit as st
from streamlit_extras.stylable_container import stylable_container
st.set_page_config(page_title="Digital Diagnosis System", page_icon="🩺")

from diagnosis_symptoms.diagnosis_page import diagnosis_app, reset_session
from instant_answer.ia_page import instant_answer_page

def show_home():
        
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            scroll-behavior: smooth;
        }
        .main-header {
            background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 50%, #3b82f6 100%);
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            animation: fadeInDown 1s ease-out;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        .feature-card {
            background: #f8fafc;
            padding: 2rem;
            border-radius: 15px;
            border-left: 6px solid #3b82f6;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            animation: fadeInUp 0.8s ease-out;
            color: #1e293b;
        }
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        .about-section {
            background: #eff6ff;
            border: 2px solid #60a5fa;
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            color: #1e293b;
        }
        @keyframes fadeInDown {
            0% { opacity: 0; transform: translateY(-30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🩺 Digital Diagnosis System</h1>
        <p style="font-size: 1.25rem; margin-top: 0.8rem;">Your Trusted AI-Powered Health Companion</p>
    </div>
    """, unsafe_allow_html=True)

    with stylable_container(
        key="diagnosis_button",
        css_styles="""
            button {
                background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
                color: white;
                padding: 1.2rem 2rem;
                border: none;
                border-radius: 16px;
                font-size: 1.1rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                cursor: pointer;
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
                width: 100%;
                margin-bottom: 1.5rem;
                position: relative;
                overflow: hidden;
                text-transform: uppercase;
                backdrop-filter: blur(10px);
            }
            button:before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            button:hover {
                transform: translateY(-6px) scale(1.02);
                box-shadow: 0 15px 40px rgba(59, 130, 246, 0.5);
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            }
            button:hover:before {
                left: 100%;
            }
            button:active {
                transform: translateY(-2px) scale(0.98);
                transition: transform 0.1s;
            }
        """,
    ):
        # Navigation Buttons with Streamlit (functional)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🩺 Check Symptoms", key="diagnosis_btn"):
                st.query_params.page = "diagnosis"
                st.rerun()
        with col2:
            if st.button("💡 Instant Health Q&A", key="instant_btn"):
                st.query_params.page = "instant_answer"
                st.rerun()


    # Feature Grid
    st.markdown("""
    
    <div class="card-grid">
        <div class="feature-card">
            <h4>🩺 Intelligent Symptom Checker</h4>
            <p>Analyze your symptoms with smart algorithms and receive possible diagnosis suggestions instantly.</p>
        </div>
        <div class="feature-card">
            <h4>🔐 Private & Secure</h4>
            <p>Your data stays local and secure. No health data is stored or shared externally.</p>
        </div>
        <div class="feature-card">
            <h4>💬 AI-Powered Instant Q&A</h4>
            <p>Ask any health-related questions and get accurate, AI-generated responses in seconds.</p>
        </div>
        <div class="feature-card">
            <h4>📱 Mobile-Friendly</h4>
            <p>Optimized UI for all screen sizes with a responsive and accessible design.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # About Section
    st.markdown("""
    <div class="about-section">
        <h3 style="color: #1e3a8a;">ℹ️ About Digital Diagnosis</h3>
        <p style="line-height: 1.6;">
            Digital Diagnosis System is your assistant for gaining quick, reliable, and AI-powered health insights.
            Designed with simplicity and accessibility in mind, it ensures that anyone can interact with AI for their basic medical concerns.
        </p>
        <ul>
            <li>✅ Easy to Use</li>
            <li>✅ No Sign-Up Required</li>
            <li>✅ Backed by Medical Knowledge Graph</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="
        text-align: center; 
        margin-top: 3rem; 
        padding: 2rem; 
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        border-radius: 20px; 
        color: #f8fafc;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.3);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 30%, rgba(59, 130, 246, 0.1) 50%, transparent 70%);
            pointer-events: none;
        "></div>
        <div style="position: relative; z-index: 1;">
            <h4 style="
                color: #fbbf24; 
                margin-bottom: 1rem; 
                font-size: 1.1rem;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            ">
                ⚠️ Important Disclaimer
            </h4>
            <p style="
                font-size: 1rem; 
                line-height: 1.6; 
                margin-bottom: 1rem;
                color: #e2e8f0;
            ">
                This tool provides <strong style="color: #60a5fa;">preliminary health insights</strong> and educational information only.
                <br>Always consult with qualified healthcare professionals for proper medical diagnosis and treatment.
            </p>
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                gap: 1rem; 
                margin-top: 1.5rem;
                flex-wrap: wrap;
            ">
                <span style="
                    background: rgba(59, 130, 246, 0.2); 
                    padding: 0.5rem 1rem; 
                    border-radius: 25px; 
                    font-size: 0.85rem;
                    border: 1px solid rgba(59, 130, 246, 0.3);
                    color: #93c5fd;
                ">
                    🔒 Privacy Protected
                </span>
                <span style="
                    background: rgba(34, 197, 94, 0.2); 
                    padding: 0.5rem 1rem; 
                    border-radius: 25px; 
                    font-size: 0.85rem;
                    border: 1px solid rgba(34, 197, 94, 0.3);
                    color: #86efac;
                ">
                    ⚡ AI-Powered
                </span>
                <span style="
                    background: rgba(168, 85, 247, 0.2); 
                    padding: 0.5rem 1rem; 
                    border-radius: 25px; 
                    font-size: 0.85rem;
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    color: #c4b5fd;
                ">
                    🩺 Educational Use
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_diagnosis():
    if st.button("🔙 Back to Home"):
        reset_session()
        st.query_params.page = "home"
        st.rerun()

def show_instant_answer():
    if st.button("🔙 Back to Home"):
        st.query_params.page = "home"
        st.rerun()

def main():
    page = st.query_params.get("page", "home")
    if page == "diagnosis":
        diagnosis_app()
        show_diagnosis()
    elif page == "instant_answer":
        instant_answer_page()
        show_instant_answer()
    else:
        show_home()


if __name__ == "__main__":
    main()
