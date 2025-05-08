# 🧠 دليل الطالب (Student Guide Chatbot)

![KSU Logo](Deployment_app/ksu_logo_transparent.png)

**دليل الطالب** هو تطبيق دردشة ذكي يساعد طلاب الجامعة في الحصول على إجابات حول الأنظمة الجامعية والإجراءات الأكاديمية. يعتمد على نموذج ذكاء اصطناعي مدرب على مجموعة من الأسئلة الشائعة واللوائح العامة، وخاصة المتعلقة بـ:

- الأسئلة العامة حول الجامعة
- إدارة القبول والتسجيل
- كلية علوم الحاسب والمعلومات

---

## 🎯 Project Description and Objectives

This chatbot serves as a digital assistant for students, helping them navigate college policies and procedures by answering questions in Arabic. It leverages local NLP models and a simple multi-session Gradio frontend to allow switching between different consultations.

---

## 📁 Folder & File Structure

| Path                          | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `Deployment_app/`             | Contains the frontend UI, Dockerfile, and model switch logic               |
| ├── `frontend_with_examples.py` | Main Gradio UI with RTL layout and chat session logic                      |
| ├── `core_with_ollama_switch.py` | Connects frontend to the LLM inference logic                              |
| ├── `Dockerfile`              | Docker build configuration                                                 |
| ├── `requirements.txt`        | Python package dependencies                                                |
| ├── `.env`                    | Environment variables for deployment                                       |
| ├── `ksu_logo_transparent.png`| University logo shown in UI                                               |
| `Ingestion_data/`             | Raw and merged datasets for chatbot training                               |
| ├── `scraped_data/`           | Contains `.txt` files for various university guides and regulations        |
| ├── `ksuingestion.py`         | Data preprocessing and ingestion logic                                     |
| `ksuRagSystem/`               | Core backend logic and vector store configs                                |
| ├── `backend_cores/`          | Embeddings, retrieval, and response system (details inside)               |
| ├── `frontend/`               | Optional extra frontend layer or API integration                          |
| `scraping/`                   | Scripts used to extract and structure raw legal/regulation texts           |
| ├── `filefilter.py`           | Filters useful text files                                                 |
| ├── `scrape.py`               | Scrapes source websites or documents                                      |
| `.gitignore`                  | Standard Git ignore settings                                               |
| `README.md`                   | This file                                                                 |

---

## ⚙️ Setup & Installation Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/student-guide.git
cd student-guide/Deployment_app
python frontend_with_examples.py

