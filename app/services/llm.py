from groq import Groq

from app.core.config import GROQ_API_KEY
from app.core.prompts import SYSTEM_PROMPT

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(question, retrieved_docs):

    context_parts = []

    for doc in retrieved_docs:

        page_number = doc.metadata.get("page")

        chunk_text = doc.page_content

        formatted_chunk = f"""
Page Number: {page_number}

Content:
{chunk_text}
"""

        context_parts.append(formatted_chunk)

    final_context = "\n\n".join(context_parts)

    final_prompt = SYSTEM_PROMPT.format(context=final_context)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": question},
        ],
    )

    return response.choices[0].message.content
