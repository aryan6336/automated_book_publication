# 📘 AI-Based Automated Book Publication Workflow

## This project implements a complete **automated book publishing pipeline** using **Python3.10.11, Streamlit, Playwright, LangChain**, and **ChromaDB**. The system allows scraping public domain book chapters, rewriting the content using an AI writer agent, reviewing it via an AI reviewer agent, and tracking all versions using a vector database.
---

## 🧩 Project Features

- 🔗 **Scraping**: Scrapes chapter content from a given URL (e.g., WikiSource) using Playwright.
- ✍️ **AI Writer**: Rewrites the chapter using a local or remote LLM agent.
- 🧠 **AI Reviewer**: Reviews and refines the rewritten content for better readability and flow.
- 🧑‍💻 **Human-in-the-loop**: Allows manual editing of AI-reviewed content.
- 🧾 **Version Control**: Tracks all iterations (scraped, AI-generated, human-edited) using ChromaDB and vector embeddings.

---

## 🛠️ Technologies Used

| Purpose               | Tools / Libraries                                  |
|----------------------|-----------------------------------------------------|
| UI & Workflow        | `Streamlit`                                         |
| Web Scraping         | `Playwright`                                        |
| LLM Agent Interface  | `LangChain`, `langchain-community`                  |
| Embeddings & Vectors | `sentence-transformers`, `transformers`, `ChromaDB` |
| Data Processing      | `pandas`, `numpy`, `tqdm`                           |

---

---

## ▶️ How to Run

### 1. 🧱 Setup Virtual Environment

```bash
python -m venv venv        # On Linux/Mac
./venv/Scripts/activate           # On Windows
streamlit run human_reviewer_app.py 
```
### 2.Download playwright seperately 

```bash
pip install playwright
playwright install
```
### 3.Download requirements 

```bash 
pip install -r requirements.txt
```
---

---
## ✅ Workflow Steps
### Input URL of a chapter (e.g., from WikiSource).

### Click "Start Workflow":

- 🔍 Scrapes the chapter

- ✍️ Generates rewritten version

- 🧠 Reviews the generated version

### Manually edit the reviewed version and click "Submit Human Review"

### View and explore all past iterations saved in ChromaDB with metadata.

---
---
## 📚 Version Control with ChromaDB
### Each document (original, rewritten, reviewed, human-edited) is stored with metadata:

- Chapter ID

- Source (scraper, writer, reviewer, user)

- Version tag (e.g., v1, rewritten, final, user edit)

- Timestamp

### Enables semantic vector search and version retrieval later.

---
