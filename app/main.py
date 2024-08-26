from fastapi import HTTPException
from typing import Dict
import time
from langdetect import detect
from deep_translator import GoogleTranslator


from . import app
from .models import QueryRequest

from lama_model.query_handler import qa_chain



@app.post("/query")
async def handle_query(request: QueryRequest) -> Dict[str, str]:
    try:
        start_time = time.time()
        
        query = request.query
        language = detect(query)  

       
        
        response = qa_chain.invoke({"query": query})
        result = response.get("result", "No result found")
        
        try:
            translated_result = GoogleTranslator(source='en', target=language).translate(result)
        except Exception as translation_error:
            raise HTTPException(status_code=500, detail=f"Translation Error: {str(translation_error)}")
        
        run_time = time.time() - start_time

        return {"result": translated_result, "run_time": str(run_time), "language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))