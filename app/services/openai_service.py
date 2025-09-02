from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_text(text: str):
  prompt = f"""
    Analyze the following text and return a JSON response with exactly this format:
    {{
      "summary": "1-2 sentence summary here",
      "title": "title if available, or null",
      "key_topics": ["topic1", "topic2", "topic3"],
      "sentiment": "positive/neutral/negative"
    }}

    Text:
    \"\"\"{text}\"\"\"
    """

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
  )

  content = response.choices[0].message.content
    
  json_str = content.strip()
    
  try:
    return json.loads(json_str)
  except json.JSONDecodeError:
    return {"error": "Failed to parse JSON response", "raw_response": content}