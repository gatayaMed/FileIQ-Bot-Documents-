# 🤖 FileIQ - Document Intelligence Bot

An advanced AI-powered document assistant that allows users to upload documents (PDF, DOCX, TXT) and interact with them using natural language. Powered by Deepseek, Groq, OpenAI, and Anthropic Claude via LangChain.

![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-red.svg)

## ✨ Features

### 🎯 Core Capabilities
- **📄 Document Upload** — Support for PDF, DOCX, and TXT files
- **🤖 Multi-LLM Support** — Deepseek, Groq, OpenAI, Anthropic Claude
- **🔍 RAG Retrieval** — Retrieves relevant document chunks with citations
- **💬 Conversation Memory** — Maintains chat history within session
- **📊 Document Comparison** — Compare two documents side-by-side
- **📥 Export Chat** — Download chat history as text file
- **🎨 Modern UI** — Clean, responsive Streamlit interface
- **🔒 Session Management** — Secure per-session chat history
- **🔗 API Integration** — Easy provider switching

### 🚀 Advanced Features
- **Multi-Document Upload** — Process multiple documents at once
- **Vector Search** — FAISS-powered semantic search
- **Source Citations** — Shows document sources for AI answers
- **Customizable Models** — Choose LLM and adjust temperature
- **Real-time Processing** — Fast document extraction with Pypdf & pdfplumber
- **Error Handling** — Graceful fallbacks for document parsing
- **Streaming Responses** — Watch AI generate answers in real-time

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web application framework |
| **AI Framework** | LangChain | LLM orchestration |
| **Vector Store** | FAISS-CPU | Semantic search & retrieval |
| **Embeddings** | HuggingFace | Text vectorization |
| **Document Processing** | Pypdf, pdfplumber, python-docx | PDF/DOCX parsing |
| **LLM Providers** | Deepseek, Groq, OpenAI, Anthropic | AI models |
| **Container** | Docker | Deployment |

## 📋 Installation

### Option 1: Local Installation

#### Prerequisites
- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

#### Step-by-Step

```bash
# Clone the repository
git clone https://github.com/gatayaMed/FileIQ-Bot-Documents-.git
cd FileIQ-Bot-Documents-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Run the application
streamlit run app.py
```

The app will be available at: `http://localhost:8501`

### Option 2: Docker Deployment

```bash
# Clone the repository
git clone https://github.com/gatayaMed/FileIQ-Bot-Documents-.git
cd FileIQ-Bot-Documents-

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Build Docker image
docker build -t fileiq .

# Run container
docker run -p 8501:8501 \
  -e DEEPSEEK_API_KEY=your_key_here \
  -e STREAMLIT_SECRET_KEY=your_secret_here \
  -v $(pwd)/data:/app/data \
  fileiq
```

## 🔑 Configuration

### Setting Up API Keys

#### Deepseek (Primary Provider)
1. Visit: https://platform.deepseek.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create a new API key
5. Add to `.env`:
   ```bash
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
   ```

#### Groq (Alternative)
1. Visit: https://console.groq.com/
2. Sign up / Log in
3. Get your API key
4. Add to `.env`:
   ```bash
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxx
   ```

#### OpenAI (Alternative)
1. Visit: https://platform.openai.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create a new API key
5. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
   ```

#### Anthropic Claude (Alternative)
1. Visit: https://console.anthropic.com/
2. Sign up / Log in
3. Get your API key
4. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
   ```

#### Generate Streamlit Secret
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Add to `.env`:
```bash
STREAMLIT_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 📚 Usage

### Uploading Documents

1. Click **"Upload Documents"** in the sidebar
2. Select one or multiple files:
   - PDF (.pdf)
   - Word documents (.docx)
   - Text files (.txt)
3. Click **"Process Documents"** to extract text
4. Click **"Create Search Index"** to enable RAG

### Chatting with Documents

1. Type your question in the chat input
2. Toggle **"Use RAG"** to enable/disable document retrieval
3. Click **"Send"** to get AI response
4. View citations showing which document sections were used

### Comparing Documents

1. Click **"Document Comparison"** in sidebar
2. Upload two documents to compare
3. Click **"Compare Documents"**
4. See similarity metrics and unique word analysis

### Managing Chat

- **Clear History:** Clears all chat messages
- **Export Chat:** Downloads conversation as text file
- **Session-based:** History is lost on page refresh

## 🔧 Development

### Project Structure

```
FileIQ/
├── app.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Adding New Features

1. Add new function to `app.py`
2. Update requirements.txt if needed
3. Test locally
4. Commit and push changes

## 🚀 Deployment

### Deploy to Coolify

1. Push repository to GitHub
2. Log in to Coolify
3. Create new application
4. Select **Git Repository**
5. Enter: `https://github.com/gatayaMed/FileIQ-Bot-Documents-.git`
6. Add environment variables:
   - `DEEPSEEK_API_KEY`
   - `STREAMLIT_SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*.smarta.website`
7. Add domain: `fileiq.smarta.website`
8. Click Deploy

### Environment Variables for Coolify

| Variable | Value | Secret? |
|-----------|-------|--------|
| DEBUG | False | No |
| DEEPSEEK_API_KEY | your_key_here | ✅ Yes |
| STREAMLIT_SECRET_KEY | your_secret_here | ✅ Yes |
| ALLOWED_HOSTS | *.smarta.website | No |

## 🔍 Troubleshooting

### Document Processing Issues

**Problem:** "Error processing document"

**Solutions:**
- Ensure file is valid (not corrupted)
- Try uploading a smaller document first
- Check file format is supported
- Check browser console for detailed error

### LLM Issues

**Problem:** "Error initializing LLM"

**Solutions:**
- Verify API key is correct
- Check API key has proper permissions
- Ensure you have sufficient credits/quota
- Try different LLM provider
- Check network connection

### Vector Store Issues

**Problem:** "Error creating vector store"

**Solutions:**
- Ensure documents have been processed first
- Check available memory
- Try with fewer documents
- Restart the application

### Docker Issues

**Problem:** Container won't start

**Solutions:**
```bash
# Check logs
docker logs <container_id>

# Rebuild image
docker build -t fileiq .

# Run without cache
docker build --no-cache -t fileiq .
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact: 

## 🙏 Acknowledgments

- **Streamlit** - Web framework
- **LangChain** - AI orchestration framework
- **HuggingFace** - Embeddings
- **Deepseek** - Primary LLM provider
- **Groq** - Alternative LLM provider
- **OpenAI** - Alternative LLM provider
- **Anthropic** - Alternative LLM provider
- **FAISS** - Vector similarity search

---

**Built with ❤️ by Med & Team**
**Powered by Deepseek** - Advanced AI for document intelligence
