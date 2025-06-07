import streamlit as st
from instant_answer.instant_answer import generate_instant_answer
from instant_answer.schema import InstantAnswer

def instant_answer_page():
    
    st.title("💡 Instant Answer")

    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .info-section {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border-left: 5px solid #4e79a7;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        }
        .info-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #33475b;
            margin-bottom: 0.5rem;
        }
        .info-body {
            font-size: 1rem;
            color: #3c3c3c;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h2>🏥 Digital Health Assistant</h2>
        <p>Ask a health-related question and get instant, structured answers.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        user_query = st.text_input("Enter your health question:", placeholder="e.g., What should I do for a headache?", label_visibility="visible")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing to align with input
        get_answer_button = st.button("Get Answer")

    if get_answer_button:
        if user_query.strip() == "":
            st.warning("Please enter a question to get an answer.")
            return

        with st.spinner("Analyzing your query..."):
            try:
                result = generate_instant_answer(user_query)
                if not isinstance(result, InstantAnswer):
                    st.error("Unexpected response format. Please try again.")
                    return
                st.success("✅ Here's what we found:")

                def show_section(title, content):
                    st.markdown(f"""
                    <div class="info-section">
                        <div class="info-title">{title}</div>
                        <div class="info-body">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)

                if result.emergency:
                    show_section("🚨 Emergency", f"{result.emergency.emergency}<br><small>{result.emergency.description}</small>")

                if result.suggestion:
                    show_section("💡 Suggestion", result.suggestion.suggestion)

                if result.whom_to_consult:
                    show_section("👨‍⚕️ Whom to Consult", f"<p><strong>{result.whom_to_consult.specialist}</strong><br> {result.whom_to_consult.description}</p>")

                if result.clinical_guidance:
                    show_section("🏥 Clinical Guidance", f"<p><strong>{result.clinical_guidance.guidance}</strong> <br> {result.clinical_guidance.description}</p>")

                if result.treatment:
                    show_section("💊 Treatment", f"<p><strong>{result.treatment.treatment}</strong> <br> {result.treatment.description}</p>")

                if result.diet_and_nutrition:
                    show_section("🥗 Diet & Nutrition", f"<p><strong>{result.diet_and_nutrition.diet}</strong> <br> {result.diet_and_nutrition.description}</p>")

                if result.monitoring:
                    show_section("📊 Monitoring", f"<p><strong>{result.monitoring.monitoring}</strong> <br> {result.monitoring.description}</p>")

                if result.dos and result.dos.dos:
                    do_list = "<ul>" + "".join([f"<li>✅ {item}</li>" for item in result.dos.dos]) + "</ul>"
                    show_section("✅ Do's", do_list)

                if result.donts and result.donts.donts:
                    dont_list = "<ul>" + "".join([f"<li>❌ {item}</li>" for item in result.donts.donts]) + "</ul>"
                    show_section("❌ Don'ts", dont_list)

                if result.home_remedies:
                    show_section("🏠 Home Remedies", f"<p><strong>{result.home_remedies.remedies}</strong> <br> {result.home_remedies.description}</p>")

                if result.mental_health_and_well_being:
                    show_section("🧠 Mental Health & Well-Being", f"<p><strong>{result.mental_health_and_well_being.mental_health}</strong> <br> {result.mental_health_and_well_being.description}</p>")

                if result.first_aids:
                    show_section("🩹 First Aid", f"<p><strong>{result.first_aids.first_aid}</strong> <br> {result.first_aids.description}</p>")

                if result.precautions:
                    show_section("🛡️ Precautions", f"<p><strong>{result.precautions.precautions}</strong> <br> {result.precautions.description}</p>")

                if result.warnings:
                    show_section("⚠️ Warnings", f"<p><strong>{result.warnings.warnings}</strong> <br> {result.warnings.description}</p>")

            except Exception as e:
                st.error("Something went wrong while processing your query.")
                st.exception(e)

    st.markdown("""
    <hr style="margin-top: 2rem;">
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        ⚠️ <strong>Disclaimer:</strong> This is a general health assistant. Always consult a doctor for medical emergencies.
    </div>
    <hr style="margin-top: 2rem;">
    """, unsafe_allow_html=True)
