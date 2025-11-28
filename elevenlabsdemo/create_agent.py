# from elevenlabs import ElevenLabs

# client = ElevenLabs(

#     base_url="https://api.elevenlabs.io"

# )

# client.conversational_ai.agents.create(
#     "conversation_config": {
#         "agent": {
#             "prompt": "You are a helpful assistant...",
#             "llm": {
#                 "model": "mistral-large-latest",
#                 "temperature": 0.2
#             },
#             "language": "en",
#             "first_message": "Hey there, I'm the assistant of the pharmacy. Who's there ?"
#         }
#     }
# )

import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

agent = client.conversational_ai.agents.create(
    name="Mon Agent",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "You are an AI agent for a pharmacy, that asks to the suppliers calling what is new about their products, their price changings and their delivery time."
            },
            "first_message": "Hey there, I'm the assistant of the pharmacy. Who's there ?",
            "language": "en"
        },
        "tts": {
            "voice_id": "Xb7hH8MSUJpSbSDYk0k2"
        }
    }
)

print(agent)