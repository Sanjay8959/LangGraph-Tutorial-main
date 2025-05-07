import streamlit as st
from main import graph, State

# Set page configuration
st.set_page_config(
    page_title="Dual-Mode Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better appearance with improved visibility
st.markdown("""
<style>
:root {
    --background-color: #1E1E1E;
    --text-color: #FFFFFF;
    --primary-color: #4CAF50;
    --user-msg-bg: #2C5364;
    --assistant-msg-bg: #333333;
    --sidebar-bg: #252525;
    --border-color: #444444;
}

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

/* Main header styling */
h1, h2, h3 {
    color: var(--primary-color) !important;
    font-weight: 700 !important;
}

/* Chat container */
.stChatMessageContent {
    background-color: var(--assistant-msg-bg) !important;
    color: white !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    padding: 15px !important;
}

/* User message styling */
.stChatMessageContent[data-testid*="user"] {
    background-color: var(--user-msg-bg) !important;
    border-color: #1e88e5 !important;
}

/* Sidebar styling */
.css-1d391kg, .css-1lcbmhc, .css-12oz5g7 {
    background-color: var(--sidebar-bg) !important;
}

/* Input field styling */
.stChatInputContainer {
    background-color: #333 !important;
    border-radius: 10px !important;
    padding: 5px !important;
    border: 1px solid var(--border-color) !important;
}

.stTextInput input {
    color: white !important;
    background-color: #444 !important;
}

/* Button styling */
button.stButton>div {
    background-color: var(--primary-color) !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 5px !important;
}

/* Info box styling */
div.stAlert {
    background-color: #2C3E50 !important;
    color: white !important;
    border: 1px solid #34495E !important;
    border-radius: 5px !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 10px;
    background-color: #1E1E1E;
}

::-webkit-scrollbar-thumb {
    background-color: #555;
    border-radius: 5px;
}

/* Make text more readable */
p, li, div {
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* Chat avatar styling */
.stChatMessage .stAvatar {
    background-color: #555 !important;
}

/* Improve visibility of markdown content */
.stMarkdown {
    color: #DDD !important;
}
</style>
""", unsafe_allow_html=True)

# Create a layout with columns for better organization
col1, col2 = st.columns([3, 1])

with col1:
    # App title with improved styling
    st.title("🤖 Dual-Mode Chatbot")
    st.markdown("""<div style='background-color: rgba(76, 175, 80, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50;'>
    <h3 style='margin-top: 0;'>About this Chatbot</h3>
    <p>This intelligent chatbot automatically switches between two modes based on your message:</p>
    <ul>
        <li><strong>💚 Emotional Mode:</strong> Provides empathetic responses like a therapist</li>
        <li><strong>🔍 Logical Mode:</strong> Focuses on facts and information</li>
    </ul>
    <p>Try asking both emotional and factual questions to see how it adapts!</p>
    </div>""", unsafe_allow_html=True)

# Initialize session state for chat history and tracking
if "messages" not in st.session_state:
    st.session_state.messages = []

if "state" not in st.session_state:
    st.session_state.state = {"messages": [], "message_type": None}
    
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# Display welcome message for first-time users
if not st.session_state.conversation_started:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""👋 **Hello!** I'm your dual-mode assistant. I can provide both emotional support and logical information.  
        Try asking me something, and I'll automatically determine the best way to respond!""")

# Display chat messages with improved styling
for message in st.session_state.messages:
    icon = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# Chat input with placeholder text
user_input = st.chat_input("Type your message here... (e.g., 'I'm feeling anxious' or 'What is quantum computing?')")

if user_input:
    st.session_state.conversation_started = True
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Update state for graph processing
    st.session_state.state["messages"] = st.session_state.state.get("messages", []) + [
        {"role": "user", "content": user_input}
    ]
    
    # Process with LangGraph - show a more visually appealing spinner
    with st.status("Analyzing your message and preparing a response...", expanded=True) as status:
        status.update(label="Classifying message type...", state="running", expanded=True)
        
        # Invoke the graph with the current state
        new_state = graph.invoke(st.session_state.state)
        st.session_state.state = new_state
        
        # Determine which mode was used
        mode = new_state.get("message_type", "unknown")
        mode_display = "Emotional Support" if mode == "emotional" else "Logical Information"
        status.update(label=f"Generating {mode_display} response...", state="running")
        
        status.update(label="Response ready!", state="complete")
    
    # Get the assistant's response
    if new_state.get("messages") and len(new_state["messages"]) > 0:
        last_message = new_state["messages"][-1]
        assistant_response = last_message.content
        
        # Display assistant message with appropriate styling
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(assistant_response)
        
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        # Display the mode that was used with better styling
        mode = new_state.get("message_type", "unknown")
        mode_icon = "💚" if mode == "emotional" else "🔍"
        mode_display = "Emotional Support" if mode == "emotional" else "Logical Information"
        
        with st.sidebar:
            st.markdown(f"""<div style='background-color: rgba(52, 152, 219, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #3498db; margin-top: 20px;'>
                <h4 style='margin-top: 0;'>Last Response Type</h4>
                <p>{mode_icon} <strong>{mode_display}</strong></p>
                </div>""", unsafe_allow_html=True)

# Enhanced sidebar with better organization
with st.sidebar:
    st.header("🔄 Controls")
    
    # Add a reset button with better styling
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.state = {"messages": [], "message_type": None}
        st.session_state.conversation_started = False
        st.rerun()
    
    st.divider()
    
    st.header("ℹ️ About")
    st.markdown("""
    <div style='background-color: rgba(52, 73, 94, 0.1); padding: 15px; border-radius: 10px;'>
    <p>This chatbot uses <strong>LangGraph</strong> to dynamically route your messages to either:</p>
    <ul>
        <li><strong>💚 Emotional Agent:</strong> For personal or emotional topics</li>
        <li><strong>🔍 Logical Agent:</strong> For factual information</li>
    </ul>
    <p>The system automatically classifies your message and selects the appropriate response type.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add powered by section
    st.markdown("""
    <div style='position: absolute; bottom: 20px; left: 20px; right: 20px; text-align: center;'>
    <p style='color: #777; font-size: 12px;'>Powered by LangGraph & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
