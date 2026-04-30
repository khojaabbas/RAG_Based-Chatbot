from groq import Groq

from config.settings import GROQ_API_KEY, GROQ_MODEL

groq_client = Groq(api_key=GROQ_API_KEY)


def ask_llm(question, context):
    prompt = f"""
You are a helpful document chatbot.

Use ONLY the uploaded document context to answer the user.

If the answer is not available in the document, say:
"I couldn't find that in the document."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You answer only from the uploaded document context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content