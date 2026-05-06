import os
import json
from groq import AsyncGroq

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def transcribe_audio_video(file_path: str) -> str:
    with open(file_path, "rb") as file:
        transcription = await client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3",
        )
    return transcription.text

async def generate_summary_and_timestamps(text: str, file_type: str = "media") -> dict:
    safe_text = text[:25000] 
    
    if file_type == "pdf":
        prompt = f"""
        Analyze the following PDF document. 
        1. Extract the most critical Key Points.
        2. Format the "summary" field as a clean list of bullet points using the '•' symbol.
        3. Provide 5-10 SEO-style "keywords" that represent the document.
        4. Since this is a static document, the "timestamps" field MUST be an empty list [].
        Format your EXACT response as a valid JSON object with keys "summary" (string), "timestamps" (list), and "keywords" (list of strings). Do not include markdown blocks.
        Document Text: {safe_text}
        """
    else:
        prompt = f"""
        Analyze the following video/audio transcript. 
        1. Provide a highly professional, concise summary.
        2. Extract logical topics and timestamps.
        3. Provide 5-10 SEO-style "keywords" that represent the media.
        Format your EXACT response as a valid JSON object with keys "summary" (string), "timestamps" (list of objects with "time" in seconds and "topic"), and "keywords" (list of strings). Do not include markdown blocks.
        Document Text: {safe_text}
        """
    
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert Data Analyst. You only output valid JSON."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"}
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"summary": "Failed to parse document.", "timestamps": [], "keywords": []}

async def answer_document_question(context: str, question: str) -> str:
    safe_context = context[:25000]
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a Document Assistant. Answer accurately based ONLY on the provided context."},
            {"role": "user", "content": f"Context Document:\n{safe_context}\n\nUser Question: {question}"}
        ],
        model="llama-3.1-8b-instant",
    )
    return response.choices[0].message.content