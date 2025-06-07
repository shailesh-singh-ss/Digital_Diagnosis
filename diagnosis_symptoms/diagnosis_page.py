import streamlit as st
from diagnosis_symptoms.diagnosis import follow_up_chain, diagnosis_chain, memory, query_check_chain, process_chat_history, log_similar_cases_withmetadata
from diagnosis_symptoms.schema import Initial_Response, Diagnosis_Response, Question_Response
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain


assistant_icon = "./diagnosis_symptoms/assistant_icon.png"

def format_conditions(documents):
    result = []
    for document in documents:
        # Access the metadata attribute of each Document object
        metadata = document.metadata
        condition_name = metadata['conditionName']
        result.append(f"conditionName: {condition_name}")
        
        # Collect all assessment queries
        for i in range(1, 9):
            query = metadata.get(f'assessmentQuery{i}', '')
            if query:  # Only add non-empty queries
                result.append(f"assessmentQuery{i}: {query}")
        
        # Add a line break after each condition block
        result.append("\n")
    
    # Join the list into a single string with a newline separator
    return '\n'.join(result)

# === Session State Initialization ===
def init_session():
    # Reset session state variables
    # Initialize session state variables
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'diagnosis_made' not in st.session_state:
        st.session_state.diagnosis_made = False
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'current_options' not in st.session_state:
        st.session_state.current_options = None
    if 'initial_diagnosis' not in st.session_state:
        st.session_state.initial_diagnosis = None
    if 'final_question_asked' not in st.session_state:
        st.session_state.final_question_asked = False
    if 'know_more' not in st.session_state:
        st.session_state.know_more = None
    if 'diagnosis' not in st.session_state:
        st.session_state.diagnosis = None
        
def reset_session():
    st.session_state.messages = []
    st.session_state.question_count = 0
    st.session_state.diagnosis_made = False
    st.session_state.current_question = None
    st.session_state.current_options = None
    st.session_state.initial_diagnosis= None
    st.session_state.final_question_asked = False
    st.session_state.know_more = None
    st.session_state.diagnosis = None
    


def diagnosis_chat():
    """
    Main function to handle the diagnosis chat interaction.
    """

    # === Patient Form ===
    with st.form("patient_form"):
        colored_header("👤 Patient Details", description="We keep your data safe.", color_name="blue-70")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 10, 120, 25, help="Enter your current age")
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], help="Select your gender identity")

        initial_query = st.text_area("🩺 Describe your symptoms",  placeholder="Please describe what you're experiencing in detail...")
        family_history = st.selectbox("Family History", ["None", "Heart Disease", "High Blood Pressure", "Diabetes", "Cancer", "Mental Health Conditions", "Other"], help="Select any significant medical conditions that run in your family")
        if family_history == "Other":
            family_history = st.text_input("Specify condition")

        col1, col2 = st.columns(2)
        with col1:
            bp_history = st.selectbox("High Blood Pressure", ["No", "Yes - Managed", "Yes - Unmanaged", "Not sure"], help="Have you been diagnosed with high blood pressure?")
        with col2:
            diabetes_history = st.selectbox("Diabetes History", ["No", "Type 1", "Type 2", "Pre-diabetes", "Not sure"], help="Do you have any form of diabetes?")

        smoking_history = st.selectbox("Smoking", ["Non-smoker", "Current", "Former", "Occasional", "Prefer not to say"], help="Please select your smoking status for better health assessment")
        submitted = st.form_submit_button("Start Diagnosis 🚀")

    if submitted:
        reset_session()  # Reset session state variables

        # Step 1: Add initial context to memory
        context = f"""
        Age: {age}, \t\t\t       Gender: {gender}\n
        Family History:{family_history}\n 
        Previously diagnosed with Blood pressure: {bp_history}\n
        Previously diagnosed with Diabetes: {diabetes_history}\n
        Smoking:{smoking_history}\n
        Initial Symptoms: {initial_query}\n     
        
        Would you like to confirm this?"""
        memory.chat_memory.clear()
        memory.chat_memory.add_user_message(context)
        st.session_state.messages.append({"role": "assistant", "content": context})

        # Step 2: Query Check
        check = query_check_chain.invoke({"query": initial_query, "Initial_Response": Initial_Response})
        if not check["HealthQuery"]:
            st.chat_message("assistant", avatar=assistant_icon).write(check["Note"])
            st.stop()
        if check["LifeThreatening"]:
            with st.chat_message("assistant", avatar=assistant_icon):
                st.error(check["Note"])
                st.warning(f"🚨 Emergency Level: {check['EmergencyLevel']}")
                st.success(f"Consult: {check['Consult']}")
            st.stop()

        # Step 3: Fetch similar cases
        chathistory = memory.load_memory_variables({})["history"]
        symptoms = process_chat_history(chathistory)
        cases = log_similar_cases_withmetadata({"symptoms": symptoms})
        initial_diagnosis= format_conditions(cases)
        st.session_state.initial_diagnosis = initial_diagnosis

    # === Chat Display ===
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=assistant_icon if msg["role"] == "assistant" else None):
            st.markdown(msg["content"])

    # === Chat Interaction ===
    if st.session_state.messages and not st.session_state.diagnosis_made:
        
        # Handle user input
        if st.session_state.current_options:
            
            selected_option = st.selectbox("Select your response:", 
                                        options=st.session_state.current_options,
                                        index=None,
                                        key=f"select_{st.session_state.question_count}")
            if selected_option == "Other":
                user_input = st.chat_input("Your response:")
            else:
                user_input = selected_option
                
        else:
            user_input = st.chat_input("Your response:")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            memory.chat_memory.add_user_message(user_input)

            if st.session_state.question_count < 8:
                result = follow_up_chain.invoke({
                    "age": age, "gender": gender, "initial_query": initial_query,
                    "Question_Response": Question_Response,
                    "input": "", "family_history": family_history,
                    "bp_history": bp_history, "diabetes_history": diabetes_history,
                    "smoking_history": smoking_history,
                    "initial_diagnosis": st.session_state.initial_diagnosis
                })
                q = result["query"]["question"]
                opts = result["query"]["options"]
                if opts and "Other" not in opts:
                    opts.append("Other")
                st.session_state.current_options = opts
                st.session_state.messages.append({"role": "assistant", "content": q})
                memory.chat_memory.add_ai_message(q)
                st.session_state.question_count += 1
                st.rerun()

            elif not st.session_state.final_question_asked:
                final = "🤔 Any other symptoms you want to mention?"
                st.session_state.final_question_asked = True
                st.session_state.current_options = None
                st.session_state.messages.append({"role": "assistant", "content": final})
                memory.chat_memory.add_ai_message(final)
                st.rerun()

            else:
                st.session_state.diagnosis_made = True
                st.rerun()

def diagnosis_result():
    """Display the diagnosis results after the user has answered all questions.
    This function is called when the user has completed the diagnosis process and the diagnosis_made flag is set to True.
    """
    if not st.session_state.diagnosis:
        with st.spinner("Analyzing your condition..."):
            st.session_state.diagnosis = diagnosis_chain.invoke({"Diagnosis_Response": Diagnosis_Response})
    
    diagnosis = st.session_state.diagnosis
    
    rain(emoji="💊", font_size=35, falling_speed=1, animation_length=1)
    colored_header("🧠 AI Diagnosis Result", description="Here are the possible conditions:", color_name="violet-70")

    for i, d in enumerate(diagnosis["diagnosis"]):
        with stylable_container(key=f"diag_{i}", css_styles="background-color: #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 15px;"):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"{i+1}. {d}")
            with col2:
                if st.button("Know More", key=f"know_more_{i}", args=(d), help="Click to learn more about this condition"):
                    st.session_state.know_more = d

            st.markdown(f"**🧬 Description:** {diagnosis['diagnosis_description'][i]}")
            st.markdown(f"**📊 Seriousness:** {diagnosis['serious'][i]}")
            st.markdown(f"**📈 Chance:** {diagnosis['chances'][i]}")

    if diagnosis["consult_specialties"]:
        colored_header("👨‍⚕️ Recommended Specialists", description="Consult the following experts:", color_name="blue-70")
        for spec in diagnosis["consult_specialties"]:
            st.success(f"🔹 {spec}")
    

    # st.session_state.diagnosis_made = False
        


def diagnosis_app():
    
    st.title("🩺 AI Diagnosis Assistant")
        
    # === Intro Card ===
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin-bottom: 30px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; font-weight: 300;">
                🌟 Welcome to Your Personal Health Assistant
            </h3>
            <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 16px; line-height: 1.5;">
                Get personalized medical insights powered by AI. Just describe your symptoms, answer simple questions, and receive a preliminary diagnosis.
            </p>
        </div>
    """, unsafe_allow_html=True)

    
    # Add feature highlights
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 15px;">
            <div style="font-size: 2em; margin-bottom: 10px;">🔍</div>
            <h4 style="margin: 0; color: #4a5568;">Smart Analysis</h4>
            <p style="font-size: 14px; color: #718096;">AI-powered symptom evaluation</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 15px;">
            <div style="font-size: 2em; margin-bottom: 10px;">👨‍⚕️</div>
            <h4 style="margin: 0; color: #4a5568;">Expert Guidance</h4>
            <p style="font-size: 14px; color: #718096;">Specialist recommendations</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 15px;">
            <div style="font-size: 2em; margin-bottom: 10px;">🛡️</div>
            <h4 style="margin: 0; color: #4a5568;">Secure & Private</h4>
            <p style="font-size: 14px; color: #718096;">Your health data is protected</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    
    if 'diagnosis_made' in st.session_state and ( st.session_state.diagnosis_made or st.session_state.know_more):
        if st.session_state.know_more:
            from diagnosis_symptoms.know_more_page import know_more
            know_more(st.session_state.know_more)
            st.session_state.know_more = None
            st.session_state.diagnosis_made = False
        else:
            diagnosis_result()
    else:
        init_session()
        diagnosis_chat()
    
        