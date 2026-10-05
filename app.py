import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES 
# --------------------------------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Interview Preparation & Evaluation System",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    :root {
        --bg-dark: #0f172a;
        --bg-panel: #111827;
        --bg-surface: #1e293b;
        --primary: #7c3aed;
        --secondary: #22d3ee;
        --text: #e2e8f0;
        --muted: #cbd5e1;
        --success: #34d399;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 40%, #1e293b 100%);
        color: var(--text) !important;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        letter-spacing: 0.04em;
        margin: 0.5rem 0 0.75rem 0;
        background: linear-gradient(90deg, #7c3aed, #22d3ee, #34d399);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: var(--muted);
        margin-bottom: 2rem;
        letter-spacing: 0.02em;
    }

    .score {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        color: var(--success);
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(17, 24, 39, 0.96));
        border-right: 1px solid rgba(148, 163, 184, 0.2);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(15, 23, 42, 0.35);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 0.8rem 1rem;
    }

    div[data-testid="stFileUploader"],
    div[data-testid="stExpander"] {
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.35);
        padding: 0.5rem;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.65rem 1.1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(124, 58, 237, 0.35);
    }

    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc;
    }

    p, li, div {
        color: var(--text);
    }

    .stMarkdownContainer code {
        background: rgba(15, 23, 42, 0.9);
        color: #c4b5fd;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HUGGING FACE CLIENT
# --------------------------------------------------

if HF_TOKEN:
    client = InferenceClient(
        token=HF_TOKEN
    )
else:
    client = None

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(uploaded_file):
    document = Document(uploaded_file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def ask_huggingface(prompt):

    if not client:
        return "Hugging Face token is missing. Please add HF_TOKEN to your .env file."

    try:

        response = client.chat_completion(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an expert AI interview preparation assistant.
Give clear, professional and useful answers.
Evaluate interview answers fairly and provide constructive feedback.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error connecting to Hugging Face: {e}"


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 AI Interview Preparation & Evaluation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Prepare smarter • Practice interviews • Get AI-powered feedback</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "🏠 Home",
        "📄 Resume Analysis",
        "🎯 Generate Questions",
        "💬 Interview Practice",
        "📊 Answer Evaluation"
    ]
)

# ==================================================
# HOME
# ==================================================

if page == "🏠 Home":

    st.header("Welcome 👋")

    st.write("""
    This AI-powered system helps students and job seekers prepare
    for technical and HR interviews.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📄 Resume Analysis")
        st.write("Upload your resume and extract your skills.")

    with col2:
        st.subheader("🎯 Question Generator")
        st.write("Generate interview questions based on your role.")

    with col3:
        st.subheader("📊 AI Evaluation")
        st.write("Get AI-powered feedback and scoring.")

    st.info(
        "💡 Start by uploading your resume or generating interview questions."
    )

# ==================================================
# RESUME ANALYSIS
# ==================================================

elif page == "📄 Resume Analysis":

    st.header("📄 Resume Analysis")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"]
    )

    if uploaded_file:

        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_pdf_text(uploaded_file)

        else:
            resume_text = extract_docx_text(uploaded_file)

        st.success("Resume uploaded successfully!")

        with st.expander("View Resume Text"):
            st.text(resume_text[:5000])

        if st.button("🔍 Analyze Resume"):

            prompt = f"""
Analyze the following resume for an interview.

Identify:

1. Technical skills
2. Programming languages
3. Projects
4. Strengths
5. Areas to improve
6. Suitable job roles
7. Interview topics to prepare

Resume:

{resume_text}
"""

            with st.spinner("Analyzing resume..."):

                result = ask_huggingface(prompt)

            st.subheader("🤖 AI Resume Analysis")

            st.write(result)

# ==================================================
# QUESTION GENERATOR
# ==================================================

elif page == "🎯 Generate Questions":

    st.header("🎯 Interview Question Generator")

    role = st.selectbox(
        "Select Job Role",
        [
            "AIML Engineer",
            "Machine Learning Engineer",
            "Data Scientist",
            "Python Developer",
            "Data Analyst",
            "Software Developer"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    number = st.slider(
        "Number of Questions",
        1,
        15,
        5
    )

    if st.button("🚀 Generate Questions"):

        prompt = f"""
Generate {number} interview questions for the following position:

Job Role: {role}

Difficulty: {difficulty}

Include a mixture of:
- Technical questions
- Conceptual questions
- Practical questions
- Scenario-based questions

Number each question clearly.
"""

        with st.spinner("Generating questions..."):

            result = ask_huggingface(prompt)

        st.subheader("🤖 Generated Questions")

        st.write(result)

# ==================================================
# INTERVIEW PRACTICE
# ==================================================

elif page == "💬 Interview Practice":

    st.header("💬 Interview Practice")

    role = st.selectbox(
        "Choose your interview role",
        [
            "AIML Engineer",
            "Machine Learning Engineer",
            "Python Developer",
            "Data Scientist",
            "Data Analyst"
        ]
    )

    question = st.text_area(
        "Enter the interview question",
        placeholder="Example: What is Machine Learning?"
    )

    answer = st.text_area(
        "Enter your answer",
        height=200,
        placeholder="Type your interview answer here..."
    )

    if st.button("🤖 Evaluate My Answer"):

        if not question or not answer:

            st.warning("Please enter both question and answer.")

        else:

            prompt = f"""
You are an expert technical interviewer.

Job Role:
{role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Give:

1. Score out of 10
2. What was done well
3. What was missing
4. Technical correctness
5. How to improve
6. A better sample answer
"""

            with st.spinner("Evaluating your answer..."):

                result = ask_huggingface(prompt)

            st.subheader("📊 Interview Feedback")

            st.write(result)

# ==================================================
# ANSWER EVALUATION
# ==================================================

elif page == "📊 Answer Evaluation":

    st.header("📊 AI Answer Evaluation")

    question = st.text_area(
        "Interview Question",
        placeholder="Enter the interview question..."
    )

    answer = st.text_area(
        "Candidate Answer",
        height=250,
        placeholder="Enter the candidate's answer..."
    )

    if st.button("📈 Evaluate Answer"):

        if not question or not answer:

            st.warning("Please provide both question and answer.")

        else:

            prompt = f"""
Evaluate this interview answer as a professional interviewer.

Question:
{question}

Candidate Answer:
{answer}

Provide the evaluation in this format:

Overall Score: X/10

Technical Knowledge:
Communication:
Relevance:
Confidence:
Completeness:

Strengths:
- 

Weaknesses:
-

Suggestions:
-

Improved Answer:
-
"""

            with st.spinner("AI is evaluating the answer..."):

                result = ask_huggingface(prompt)

            st.subheader("📊 Evaluation Result")

            st.write(result)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.info(
    "Powered by Python + Streamlit + Hugging Face"
)