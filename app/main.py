import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.controller.user_prompt import router as user_prompt
from app.controller.user_prompt_sql import router as user_prompt_sql
from app.controller.get_prompt_collection import router as get_prompt_collection
from app.controller.create_collections import router as create_collection
from app.controller.file_upload import router as create_file_upload
from app.controller.upload_img_s3 import router as upload_img_s3
from app.controller.chat_completion import router as chatbot_service
app = FastAPI()

app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
                   )

app.include_router(user_prompt, prefix='/api', tags=["User Prompt"])
app.include_router(get_prompt_collection, prefix='/api', tags=["Get Prompt Collections"])
app.include_router(create_collection, prefix='/api', tags=["Create Collection"])
app.include_router(create_file_upload, prefix='/api', tags=["Create File Upload"])
app.include_router(upload_img_s3, prefix='/api', tags=["Upload Image_S3"])
app.include_router(chatbot_service, prefix='/api', tags=["Chatbot Service"])
app.include_router(user_prompt_sql, prefix='/api', tags=["User Prompt_sql"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chart Service API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    print('Port', port)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, debug=True)