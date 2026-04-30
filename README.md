RAG-Based Chatbot

This project is an AI-powered chatbot that lets you upload a **PDF or Word document** and ask questions about it.
Instead of manually reading long documents, you can just upload them and chat with your content.

What this project does

--Upload a document (PDF or Word)
--Ask questions in natural language
--Get answers based only on the document content

It works like ChatGPT, but focused only on your uploaded file.

How it works (simple explanation)

1. You upload a document  
2. The app reads and splits it into smaller parts  
3. Each part is converted into embeddings (numerical meaning)  
4. These are stored in a vector database (ChromaDB)  
5. When you ask a question:
   - The most relevant parts are found
   - They are sent to the AI model (Groq)
6. The AI generates a response based on that context  

This approach is called **RAG (Retrieval-Augmented Generation)**.

eatures

- Supports PDF and Word files  
- Chat with your document  
- Fast responses using Groq API  
- Chat history is saved  
- Create new chats  
- Delete chats  
- Clean and simple UI  

---

## Tech Stack

- **Frontend:** Streamlit  
- **LLM:** Groq (LLaMA 3)  
- **Embeddings:** Sentence Transformers  
- **Vector Database:** ChromaDB  
- **PDF/Doc Parsing:** PyPDF2, python-docx  

## Project Structure
pdf-chatbot/
│
├── app.py
├── requirements.txt
├── .env
│
├── config/
├── services/
├── storage/


---

## 🔐 Setup (API Key)

Create a `.env` file and add your Groq API key:


---

## ⚙️ How to run

1. Clone the repository:

```bash
git clone https://github.com/your-username/pdf-chatbot.git
cd pdf-chatbot

2.Install dependencies:

pip install -r requirements.txt

3. Run the app:
streamlit run app.py