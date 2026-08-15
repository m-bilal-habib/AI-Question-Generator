import os
import streamlit as st
from pydantic import BaseModel, Field
from typing import List
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ==========================================
# 1. PYDANTIC SCHEMAS (Structured Output)
# ==========================================
class QuestionItem(BaseModel):
    id: int = Field(description="Question number starting from 1")
    question: str = Field(description="Clear question generated strictly from the source text")
    answer: str = Field(description="Exact and complete answer based strictly on the source text")
    explanation: str = Field(description="Brief explanation referencing key details from the source text")

class QuizResponse(BaseModel):
    quiz_title: str = Field(description="A concise, descriptive title for the question set")
    questions: List[QuestionItem] = Field(description="List of generated questions")


# ==========================================
# 2. LANGCHAIN & PROMPT INTEGRATION
# ==========================================
def get_quiz_chain(hf_api_key: str):
    """Initializes the Hugging Face model and LangChain pipeline."""
    
    # Initialize the LLM
    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-7B-Instruct",
        task="text-generation",
        max_new_tokens=2500,
        temperature=0.2,  # Low temperature for strict adherence to text and JSON formatting
        huggingfacehub_api_token=hf_api_key
    )
    
    chat_model = ChatHuggingFace(llm=llm)
    parser = PydanticOutputParser(pydantic_object=QuizResponse)

    # Master Prompt enforcing strict rules
    prompt_template = """You are a strict academic assistant. Your sole task is to generate questions based ONLY and EXCLUSIVELY on the provided SOURCE TEXT.

STRICT RULES:
1. Generate EXACTLY {num_questions} questions (Must be strictly between 5 and 10 questions).
2. All questions and answers must be strictly derived from facts directly stated in the SOURCE TEXT.
3. DO NOT use any outside knowledge, assumptions, or external context.
4. Each question must be clear, concise, and directly test understanding of the provided text.
5. Difficulty Level: {difficulty}

SOURCE TEXT:
---
{context_text}
---

FORMAT REQUIREMENTS:
Return ONLY valid JSON matching the format instructions below. Do not add any introductory or concluding text outside the JSON structure.

{format_instructions}"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context_text", "num_questions", "difficulty"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Chain: Prompt -> LLM -> JSON Parser
    return prompt | chat_model | parser


# ==========================================
# 3. STREAMLIT USER INTERFACE
# ==========================================
st.set_page_config(page_title="AI Question Generator", page_icon="🧠", layout="wide")

# Custom CSS for word wrapping in text boxes and code blocks
st.markdown("""
<style>
code, pre, .stCodeBlock code {
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
textarea {
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Question Generator")
st.markdown("Paste your source text below, and the AI will generate strict, text-based questions for you.")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Load API key from env or let user input it
    env_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN") or ""
    hf_api_key = st.text_input(
        "Hugging Face API Key", 
        value=env_api_key, 
        type="password", 
        help="Get this from your Hugging Face account settings."
    )
    
    st.divider()
    
    difficulty = st.selectbox("Select Difficulty", ["Easy", "Intermediate", "Hard"])
    
    # Strict range of 5 to 10 questions
    num_questions = st.number_input(
        "Number of Questions (Strictly 5 - 10)", 
        min_value=5, 
        max_value=10, 
        value=5, 
        step=1,
        help="Select between 5 and 10 questions to generate."
    )

# Main Input Area
text_input = st.text_area(
    "Paste Source Text", 
    height=250, 
    placeholder="Paste Wikipedia articles, study notes, textbook excerpts, or any text here..."
)

# Generation Logic
if st.button("Generate Questions", type="primary"):
    if not hf_api_key:
        st.error("⚠️ Please enter your Hugging Face API key in the sidebar or set it in your .env file.")
    elif not text_input.strip():
        st.error("⚠️ Please paste some source text before generating questions.")
    elif not (5 <= num_questions <= 10):
        st.error("⚠️ Number of questions must be strictly between 5 and 10.")
    else:
        word_count = len(text_input.split())
        
        if word_count < 30:
            st.warning(f"Your text is very short ({word_count} words). The AI might struggle to generate {num_questions} unique questions.")
        
        with st.spinner("Analyzing text and generating questions..."):
            try:
                # Build the LangChain pipeline
                chain = get_quiz_chain(hf_api_key)
                
                # Execute the API call
                quiz_data = chain.invoke({
                    "context_text": text_input,
                    "num_questions": int(num_questions),
                    "difficulty": difficulty
                })
                
                st.session_state["quiz_data"] = quiz_data
                st.success("Questions Generated Successfully!")
            except Exception as e:
                st.error("Failed to generate questions. The model may have returned improperly formatted JSON or timed out.")
                st.exception(e)

# Render Quiz and Copy section if quiz_data exists in session_state
if "quiz_data" in st.session_state and st.session_state["quiz_data"] is not None:
    quiz_data = st.session_state["quiz_data"]
    
    st.header(f"📝 {quiz_data.quiz_title}")
    st.caption(f"Generated {len(quiz_data.questions)} questions from your text.")
    
    # Copy Feature
    with st.expander("📋 Copy Questions / Answers", expanded=True):
        copy_option = st.radio(
            "Select format to copy:",
            options=["Questions Only", "Questions & Answers"],
            horizontal=True,
            key="copy_format_option"
        )
        
        copy_lines = [f"Title: {quiz_data.quiz_title}\n"]
        for i, q in enumerate(quiz_data.questions, start=1):
            copy_lines.append(f"{i}. {q.question}")
            if copy_option == "Questions & Answers":
                copy_lines.append(f"   Answer: {q.answer}")
                copy_lines.append(f"   Explanation: {q.explanation}")
            copy_lines.append("")  # empty line separator
            
        formatted_text = "\n".join(copy_lines)
        st.markdown("Click the copy icon on the top-right of the box below:")
        st.code(formatted_text, language=None)
        
    st.divider()
    
    # Render questions
    for i, q in enumerate(quiz_data.questions):
        st.markdown(f"### Q{i+1}: {q.question}")
        
        user_answer = st.text_input("Your Answer:", key=f"q_{i}", placeholder="Type your answer here to test yourself...")
        
        with st.expander("Show Answer & Explanation"):
            st.markdown(f"**Correct Answer:** {q.answer}")
            st.markdown(f"**Explanation:** {q.explanation}")
        
        st.divider()