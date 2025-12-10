# AI Presentation Creator

An AI-powered presentation generator with a React frontend and FastAPI backend that creates PowerPoint presentations automatically based on user topics.

## Project Structure

```
persantation_maker/
├── ai-presentation-creator/    # React frontend (Vite + TypeScript)
├── app/                       # FastAPI backend
│   ├── backend/              # Authentication & database
│   ├── ppt_content/          # PPT generation logic
│   └── main.py              # FastAPI server
└── README.md
```

## Features

- 🤖 AI-powered presentation generation
- 🔐 User authentication (signup/login)
- 📊 Customizable slide count
- 📁 PowerPoint file download
- 🎨 Modern React UI with shadcn/ui components
- 🔄 Real-time API integration

## Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite build tool
- Tailwind CSS + shadcn/ui
- React Router for navigation
- TanStack Query for API calls

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- JWT authentication
- OpenAI integration
- python-pptx for PowerPoint generation

## Installation

### Backend Setup

1. Navigate to the app directory:
```bash
cd app
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with:
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key
```

4. Run the FastAPI server:
```bash
python main.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ai-presentation-creator
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Usage

1. Open your browser to `http://localhost:5173`
2. Sign up or log in to your account
3. Enter a presentation topic
4. Specify the number of slides (default: 10)
5. Click generate to create your presentation
6. Download the generated PowerPoint file

## API Endpoints

- `POST /signup` - User registration
- `POST /login` - User authentication
- `POST /generate_pptx` - Generate PowerPoint presentation

## Development

### Frontend Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

### Backend

The FastAPI server runs on `http://127.0.0.1:8000` with automatic API documentation at `/docs`.

## License

MIT License