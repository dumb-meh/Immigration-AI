# Study Buddy 📚✨

An AI-powered learning companion that transforms your study experience through intelligent text processing, creative learning tools, and memory enhancement techniques.

## 🌟 Features

### 🤖 AI-Generated Summaries
Transform lengthy texts into concise, digestible summaries that enhance reading comprehension and save study time.

### 📖 Creative Text Conversion  
Convert boring study material into engaging stories with characters and AI-generated artwork, making learning more memorable and fun.

### 🎯 Flashcards & Quiz Games
Generate interactive flashcards, comprehension questions, and quiz games based on your study material to reinforce learning and test retention.

### 🧠 Mnemonic Creation
Create personalized mnemonics and memory aids to make complex information easier to remember and recall.

### 🧠 Task Management
An AI-driven task manager to organize tasks and prioritize.AI suggests how to best prepare for upcoming events, assignments, or tasks.


## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker (optional)
- OpenAI API Key

### Installation

#### Method 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/study-buddy.git
cd study-buddy

# Create environment file
cp .env.example .env
# Add your OpenAI API key to .env file

# Build and run with Docker Compose
docker-compose up --build
```

#### Method 2: Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/study-buddy.git
cd study-buddy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file and add your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Run the application
uvicorn main:app --host 0.0.0.0 --port 9013 --reload
```

### Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 📡 API Endpoints

### Summary Generation
```http
POST /summary
Content-Type: text/plain

Request Body: Your text content to summarize
```

### Creative Story Creation
```http
POST /story
Content-Type: text/plain

Request Body: Text to convert into a creative story
```

### Flashcard & Quiz Generation
```http
POST /flashcard-quiz
Content-Type: text/plain

Request Body: Study material for flashcard/quiz creation
```

### Mnemonic Generation
```http
POST /mnemonic
Content-Type: text/plain

Request Body: Information to create mnemonics for
```

### Task Suggestions
```http
POST /suggestion
Content-Type: application/json

Request Body: Task information for AI-powered suggestions
```

## 🏗️ Project Structure

```
study-buddy/
├── app/
│   ├── core/
│   │   └── config.py              # Application configuration
│   └── services/
│       ├── summary/               # Text summarization service
│       ├── story/                 # Creative story generation
│       ├── flashcard_quiz/        # Flashcard and quiz creation
│       ├── mnemonic/              # Mnemonic generation
│       └── task_suggestion/       # AI task suggestions
├── nginx/
│   ├── nginx.conf/
├── docker-compose.yml             # Docker composition
├── docker-compose.yml             # Docker composition
├── Dockerfile                     # Docker container setup
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🛠️ Technology Stack

- **Backend Framework:** FastAPI
- **AI Integration:** OpenAI GPT-3.5-turbo
- **Image Generation:** DALL-E 3
- **Containerization:** Docker
- **Environment Management:** Python-dotenv
- **Data Validation:** Pydantic

## 🔧 Development

### Adding New Services
1. Create a new service directory under `app/services/`
2. Implement the service class with OpenAI integration
3. Define Pydantic schemas for request/response validation
4. Create FastAPI routes
5. Register the router in `main.py`

