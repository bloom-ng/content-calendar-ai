import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def predict(message, history):
    history_openai_format = [
    {
        "role": "system",
        "content": "As a SOCIAL MEDIA MANAGER, you will respond in JSON format.  The format will be as follows: [    \n{\n        \"DATE\": \"\",\n        \"CONTENT\": \"\",\n        \"CAPTION\": \"\"\n    }\n].\nUsing the following guidelines:\n1. Group the dates into their corresponding weeks.\n2.Use the dd-mm-yyyy  format.\n3. Do not use emojis in the response at all.\n4. Create the CONTENT CALENDAR that covers every single day for the entire month provided by the user's prompt.\n5.The CONTENT column should provide the specific messages for each day, focusing on encouraging the brand's users to start campaigns, boost brand visibility, and engage with real people for effective marketing.\n6.The CAPTION column is designed to be informative, engaging, and visually appealing, using a consistent style and branding elements across all channels. It should convey enthusiasm about the brand and the benefits it offers.\n7. The CAPTION column should have an average word count MUST have more than 20 words  . \n8. The CONTENT column should be wordy with an average of 25-45 words whilst still being chatty and attractive using a human-like tone.\n9. Try and include rhythmic word-play in the CAPTION and CONTENT responses.\n"
    },
    ]


    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(model="llama3-groq-70b-8192-tool-use-preview",
                                              messages=history_openai_format,
                                              temperature=1.25,
                                              max_tokens=8192,
                                              top_p=0.5,
                                              stop=None,
                                              stream=False)

    partial_message = ""
    return response.choices[0].message.content