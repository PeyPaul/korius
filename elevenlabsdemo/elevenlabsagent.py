import os
import json
import signal
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Load environment variables
load_dotenv()

# Store messages globally
messages = []

def call_agent(agent_id: str, api_key: str = None):
    """
    Call an ElevenLabs conversational agent and return the transcript.
    
    Args:
        agent_id: The ID of your ElevenLabs agent
        api_key: Your ElevenLabs API key (or set ELEVENLABS_API_KEY env var)
    
    Returns:
        dict: Conversation transcript with messages
    """
    global messages
    messages = []
    
    # Initialize client
    if api_key is None:
        api_key = os.environ.get("ELEVENLABS_API_KEY")
    
    client = ElevenLabs(api_key=api_key)
    
    # Start conversation with the agent using callbacks to capture transcript
    conversation = Conversation(
        client=client,
        agent_id=agent_id,
        requires_auth=bool(api_key),
        audio_interface=DefaultAudioInterface(),
        # Callbacks to capture the conversation
        callback_agent_response=lambda response: capture_message("agent", response),
        callback_user_transcript=lambda transcript: capture_message("user", transcript),
    )
    
    print("Starting conversation with agent...")
    print("Speak to begin. Press Ctrl+C to end the conversation.\n")
    
    # Handle Ctrl+C gracefully to save transcript before exit
    def signal_handler(sig, frame):
        print("\n\nEnding conversation...")
        try:
            conversation.end_session()
        except:
            pass
        # Save transcript immediately
        save_transcript_on_exit()
        exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the conversation
    conversation.start_session()
    
    # Wait for conversation to complete
    conversation_id = conversation.wait_for_session_end()
    
    print("\n\nConversation ended!")
    print(f"Conversation ID: {conversation_id}")
    
    return {
        "conversation_id": conversation_id,
        "agent_id": agent_id,
        "messages": messages,
        "total_messages": len(messages)
    }


def capture_message(role: str, text: str):
    """Callback function to capture messages"""
    global messages
    message = {
        "role": role,
        "text": text
    }
    messages.append(message)
    print(f"[{role.upper()}]: {text}")


def save_transcript(transcript_data: dict, filename: str = "transcript.json"):
    """Save the transcript to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(transcript_data, f, indent=2, default=str)
    print(f"\n✓ Transcript saved to {filename}")
    return filename


def save_transcript_on_exit():
    """Save transcript when interrupted"""
    global messages
    if messages:
        result = {
            "conversation_id": "interrupted",
            "agent_id": os.getenv("AGENT_ID"),
            "messages": messages,
            "total_messages": len(messages)
        }
        filename = save_transcript(result)
        print(f"\n✓ Conversation interrupted - transcript saved to {filename}")
        print(f"✓ Total messages captured: {len(messages)}")
    else:
        print("\n! No messages to save")


if __name__ == "__main__":
    # Load from environment variables
    AGENT_ID = os.getenv("AGENT_ID")
    API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    if not AGENT_ID or not API_KEY:
        print("Error: Missing AGENT_ID or ELEVENLABS_API_KEY in .env file")
        exit(1)
    
    try:
        result = call_agent(AGENT_ID, api_key=API_KEY)
        
        # Save transcript to file
        filename = save_transcript(result)
        
        # Also print to terminal
        print("\n=== TRANSCRIPT SUMMARY ===")
        print(json.dumps(result, indent=2, default=str))
        
        print(f"\n✓ Full conversation saved to {filename}")
        print(f"✓ Total messages: {result['total_messages']}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed the package: pip install elevenlabs python-dotenv")
        print("2. Installed pyaudio: brew install portaudio && pip install pyaudio")
        print("3. Created a .env file with AGENT_ID and ELEVENLABS_API_KEY")
        print("4. Have microphone permissions enabled")