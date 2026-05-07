from groq import Groq

from app.core.config import GROQ_API_KEY
from app.core.prompts import SYSTEM_PROMPT

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_answer(question, retrieved_docs):

    context = "\n\n".join([
        doc.page_content for doc in retrieved_docs
    ])

    final_prompt = SYSTEM_PROMPT.format(
        context=context
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": final_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content