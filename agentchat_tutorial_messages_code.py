# Code snippets from AgentChat Tutorial - Messages Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/messages.html)

from io import BytesIO
import requests # Requires requests library: pip install requests
from autogen_agentchat.messages import TextMessage, MultiModalMessage
from autogen_core import Image as AGImage # Requires autogen-core
from PIL import Image # Requires Pillow library: pip install Pillow

# --- TextMessage Example ---
print(\"--- TextMessage Example ---\")
text_message = TextMessage(content=\"Hello, world!\", source=\"User\")
print(f\"TextMessage: {text_message}\")


# --- MultiModalMessage Example ---
print(\"\\n--- MultiModalMessage Example ---\")
try:
    # Fetch a sample image
    image_url = \"https://picsum.photos/300/200\"
    response = requests.get(image_url)
    response.raise_for_status() # Check if the request was successful

    # Process image with PIL and wrap with autogen_core.Image
    pil_image = Image.open(BytesIO(response.content))
    ag_image = AGImage(pil_image)

    # Create the message
    multi_modal_message = MultiModalMessage(
        content=[\"Can you describe the content of this image?\", ag_image],
        source=\"User\"
    )
    print(f\"MultiModalMessage Content Type: {type(multi_modal_message.content)}\")
    print(f\"MultiModalMessage Content[0] (Text): {multi_modal_message.content[0]}\")
    print(f\"MultiModalMessage Content[1] (Image Type): {type(multi_modal_message.content[1])}\")
    # Displaying the image object itself might not be very informative in console
    # print(f\"MultiModalMessage Image Object: {ag_image}\")
    # You could optionally save or show the PIL image if in an environment that supports it
    # pil_image.show()
except requests.exceptions.RequestException as e:
    print(f\"Error fetching image: {e}\")
except Exception as e:
    print(f\"An error occurred: {e}\")
