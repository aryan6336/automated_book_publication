# app.py

import streamlit as st
import os
from datetime import datetime
from ai_agents.writer import run_writer_agent
from q_learning_agent import run_q_learning_ai_reviewer
from scrape_chapter import scrape_chapter_from_url
import subprocess
import sys
from version_control_chroma import save_version, client as chroma_client  # Fixed import

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

st.set_page_config(page_title="AI Book Publication Workflow", layout="wide")
st.title("📘 Automated Book Publication – Full Pipeline")

# --- 1. Take URL Input from User ---
url = st.text_input("📎 Enter Chapter URL:", value="https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1")

if st.button("🚀 Start Workflow"):
    with st.spinner("🔍 Scraping chapter..."):
        python_exec = sys.executable
        try:
            subprocess.run([python_exec, "scrape_runner.py", url], check=True)
            save_version("output/chapter1.txt", chapter_id="chapter1", version_label="v1", source="scraper")
        except subprocess.CalledProcessError as e:
            st.error(f"❌ Scraping failed.\nDetails: {e}")
            st.stop()

    with st.spinner("✍️ Running AI Writer..."):
        run_writer_agent()
        save_version("output/rewritten_by_writer.txt", chapter_id="chapter1", version_label="rewritten", source="writer")

    with st.spinner("🧠 Running AI Reviewer..."):
        run_q_learning_ai_reviewer()
        save_version("output/reviewed_output.txt", chapter_id="chapter1", version_label="final", source="reviewer")

    st.success("✅ Pipeline Complete! Scroll down to review outputs.")

# --- 2. Load Files ---
def load_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "File not found."

chapter = load_file("output/chapter1.txt")
writer_output = load_file("output/rewritten_by_writer.txt")
reviewer_output = load_file("output/reviewed_output.txt")

# --- 3. Display AI Outputs for Review ---
st.markdown("## 🧾 Review AI Outputs")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📖 Original Chapter")
    st.text_area("Original", chapter, height=500, disabled=True)

with col2:
    st.subheader("✍️ AI Writer Output")
    st.text_area("Writer Version", writer_output, height=500, disabled=True)

with col3:
    st.subheader("🧹 AI Reviewer Output")
    human_input = st.text_area("Human Editor (Editable)", reviewer_output, height=500)

# --- 4. Human Review Submission ---
if st.button("✅ Submit Human Review"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output/reviewed_iteration_{timestamp}.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(human_input)
    save_version(output_filename, chapter_id="chapter1", version_label=f"human_{timestamp}", source="human")
    st.success(f"✔️ Saved as `{output_filename}`")

# --- 5. View Past Versions ---
st.header("🕓 Past Versions")

if st.button("📂 View All Versions"):
    collection = chroma_client.get_or_create_collection(name="chapter_versions")
    results = collection.get(include=["documents", "metadatas"])


    if not results["ids"]:
        st.info("⚠️ No versions saved yet.")
    else:
        for i, doc_id in enumerate(results["ids"]):
            metadata = results["metadatas"][i]
            document = results["documents"][i]

            with st.expander(f"📄 {metadata['source'].capitalize()} – {metadata['version']} ({metadata['timestamp']})"):
                st.markdown(f"**Chapter ID:** `{metadata['chapter_id']}`")
                st.markdown(f"**Source:** `{metadata['source']}`")
                st.markdown(f"**Version:** `{metadata['version']}`")
                st.markdown(f"**Timestamp:** `{metadata['timestamp']}`")
                st.code(document, language="markdown")

