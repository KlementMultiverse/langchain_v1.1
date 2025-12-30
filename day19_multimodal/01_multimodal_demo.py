"""
LangChain Academy - Module 1 - Lesson 1.4: Multimodal Messages
Sending text + images to AI in one message
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage
import base64

# Read and encode image
def encode_image(image_path: str) -> str:
    """Convert image file to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Create agent (requires vision model)
agent = create_agent(model="gpt-4o-mini")

# NOTE: You'll need an actual image file for this to work
# Example: /path/to/your/image.png

try:
    # Encode image
    base64_image = encode_image("test_image.png")

    # Create multimodal message
    message = HumanMessage(
        content=[
            {"type": "text", "text": "What do you see in this image?"},
            {
                "type": "image",
                "image": base64_image,
                "mime_type": "image/png"
            }
        ]
    )

    response = agent.invoke({"messages": [message]})
    print(response['messages'][-1].content)

except FileNotFoundError:
    print("Image file not found. Please provide a valid image path.")
    print("\nMultimodal message structure:")
    print("""
    HumanMessage(
        content=[
            {"type": "text", "text": "Your question"},
            {"type": "image", "image": base64_string, "mime_type": "image/png"}
        ]
    )
    """)
