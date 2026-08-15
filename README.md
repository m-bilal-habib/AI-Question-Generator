<div align="center">

# 🧠 AI Question Generator

**A lightweight application to generate context-grounded academic questions, answers, and explanations from any source text.**

<br>

[![Live Demo](https://img.shields.io/badge/LIVE_DEMO-STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://ai-question-generator-evlrgyheacxa4yefkgjbol.streamlit.app/)
[![Python](https://img.shields.io/badge/PYTHON-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Model](https://img.shields.io/badge/MODEL-QWEN_2.5_7B-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
[![Framework](https://img.shields.io/badge/FRAMEWORK-LANGCHAIN-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)

<br>

**Author:** [M Bilal Habib](https://github.com/m-bilal-habib)

</div>

---




## 🤖 Model Information

* **Model Used:** [`Qwen/Qwen2.5-7B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
* **Model Type:** A 7-billion parameter, open-weights instruction-tuned Large Language Model (LLM) developed by Alibaba Cloud.
* **Why this model?** Highly optimized for strict instruction following, structured JSON output generation, and multi-turn reasoning with low latency.

---

## 🔑 Hugging Face API Key Setup

An access token from Hugging Face is required to run the inference endpoint:

1. Create a free account at [Hugging Face](https://huggingface.co/).
2. Go to **Settings** → **[Access Tokens](https://huggingface.co/settings/tokens)** and generate a new token (Role: `Read`).
3. Add your token in **one of two ways**:
   * **Via `.env` file (Recommended):** Create a `.env` file in the root folder:
     ```env
     HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
     ```
   * **Via UI:** Paste your token directly into the sidebar text field inside the running Streamlit app.

---

## ✨ Main Features

* **Strict Text Grounding:** Questions and answers are derived *exclusively* from your input text to eliminate external AI hallucinations.
* **Structured Output:** Employs LangChain and Pydantic schemas to ensure reliable JSON parsing.
* **Customizable:** Select difficulty (*Easy*, *Intermediate*, *Hard*) and question count (*5 to 10*).
* **Interactive Testing:** Type in your answers before revealing the correct solutions.
* **One-Click Export:** Copy questions only or questions with full answers and explanations.

---

## 🚀 Quickstart

### 1. Install Dependencies
```bash
pip install streamlit langchain-huggingface langchain-core pydantic python-dotenv