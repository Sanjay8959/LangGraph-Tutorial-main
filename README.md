# LangGraph-Tutorial with Streamlit UI

A dual-mode chatbot that automatically switches between emotional support and logical responses based on message classification. Built with LangGraph, LangChain, and Streamlit.

## Features

- **Automatic Message Classification**: Determines if your message requires an emotional or logical response
- **Dual-Mode Responses**: 
  - Emotional/Therapist mode for personal or emotional topics
  - Logical mode for factual information and practical solutions
- **Interactive Streamlit UI**: Clean, modern interface for chatting with the bot

## Setup Instructions

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. Follow these steps to set up the project:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LangGraph-Tutorial-main
   ```

2. **Create a virtual environment with uv**
   ```bash
   uv venv .venv
   ```

3. **Activate the virtual environment**
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`

4. **Install dependencies with uv**
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Set up your environment variables**
   - Create a `.env` file with your Mistral API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```

## Running the Application

1. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Access the UI**
   - Open your browser and go to `http://localhost:8501`

## Project Structure

- `main.py`: Core LangGraph implementation with message classification and agent routing
- `app.py`: Streamlit UI for interacting with the chatbot
- `simple.py`: A simplified version of the chatbot for reference
- `requirements.txt`: Project dependencies

## Usage

Simply type your message in the chat input field. The system will automatically:

1. Classify your message as emotional or logical
2. Route it to the appropriate agent
3. Display the response in the chat interface

You can view which mode was used for each response in the sidebar.

## License

MIT