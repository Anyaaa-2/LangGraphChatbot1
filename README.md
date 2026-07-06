# LangGraph Gemini Chatbot

A simple chatbot built using LangGraph and Google's Gemini API.

## Features

- Classifies user input as greeting or search query
- Uses LangGraph to define a state-based workflow
- Calls Gemini for non-greeting questions
- Visualizes the workflow using NetworkX and Matplotlib

## Workflow

START → classify → respond → END

## Setup

1. Create a virtual environment:
python3.11 -m venv .venv
source .venv/bin/activate

2. Install dependencies:
pip install -r requirements.txt

3. Create a .env file:
GEMINI_API_KEY=your_api_key_here

4. Run the chatbot:
python bot.py

Also create `requirements.txt`:

```bash
pip freeze > requirements.txt
