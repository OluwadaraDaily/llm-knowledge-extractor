from typing import Union, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from app.services.openai_service import analyze_text
from app.services.nlp_service import extract_three_most_common_nouns
from app.db.models import Analysis

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class InputText(BaseModel):
    text: str

@app.post("/analyze")
async def analyze(request: InputText):
  print("request.text", request.text)
  openai_response = analyze_text(request.text)
  
  if "error" in openai_response:
    return {"error": openai_response["error"]}
  
  nlp_response = extract_three_most_common_nouns(request.text)

  # Save to database
  analysis = Analysis(
    input_text=request.text,
    summary=openai_response.get("summary", ""),
    title=openai_response.get("title", ""),
    topics=openai_response.get("key_topics", []),
    sentiment=openai_response.get("sentiment", ""),
    keywords=nlp_response
  )
  await analysis.save()

  response = {
     **openai_response,
     "keywords": nlp_response,
  }
  
  return response

@app.get("/search")
async def search(
  keyword: Optional[str] = None,
  sentiment: Optional[str] = None
):
  
  if keyword:
    analyses = await Analysis.search_by_keyword(keyword)
    return {
      "data": [
        {
          "id": analysis.id,
          "input_text": analysis.input_text,
          "summary": analysis.summary,
          "title": analysis.title,
          "topics": analysis.topics,
          "sentiment": analysis.sentiment,
          "keywords": analysis.keywords,
          "created_at": analysis.created_at
        }
        for analysis in analyses
      ]
    }
  
  if sentiment:
    analyses = await Analysis.search_by_sentiment(sentiment)
    return {
      "data": [
        {
          "id": analysis.id,
          "input_text": analysis.input_text,
          "summary": analysis.summary,
          "title": analysis.title,
          "topics": analysis.topics,
          "sentiment": analysis.sentiment,
          "keywords": analysis.keywords,
          "created_at": analysis.created_at
        }
        for analysis in analyses
      ]
    }
  
  return {"error": "No keyword or sentiment provided"}