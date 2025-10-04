#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

@author: andreacardiel
"""

#%% Imports
# Running the model on my computer
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TQDM_DISABLE"] = "1"
from qwen_med_lora_50_chat_model import load_model_and_tokenizer, Chat, BASE_MODEL, ADAPTER_DIR, PROMPT
from pydantic import BaseModel

# API
from fastapi import FastAPI # server setup!
from fastapi.middleware.cors import CORSMiddleware




#%% Setting up the actual API 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      "http://localhost:5173",
      "http://127.0.0.1:5173",
      "http://localhost:3000",
      "http://127.0.0.1:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


#%% Setting up for model
_tokenizer = None
_model = None
_chat = None

#%% Starting Chat
def get_chat():
    global _tokenizer, _model, _chat
    if _chat is None:
        print("Loading model… (first call only)")
        _tokenizer, _model = load_model_and_tokenizer(BASE_MODEL, ADAPTER_DIR)
        _chat = Chat(_model, _tokenizer, system=PROMPT)
        print("Model loaded. Ready.")
    return _chat

#%% Resetting Chat
@app.post("/reset")
def reset_chat():
    chat = get_chat()
    chat.reset() 
    return {"ok": True}

#%% Check server is working
@app.get("/")
def root():
    return{"message":"Server is running!"}

#%% Directory check
@app.get("/check")
def check():
    return {
        "base_model": BASE_MODEL,
        "adapter_dir": ADAPTER_DIR,
        "has_prompt": bool(PROMPT),
    }
#%%

class ChatRequest(BaseModel):
    message: str  # what the user sends
@app.post("/chat")
def chat_endpoint(body: ChatRequest):
    chat = get_chat()  
    reply = chat.say(body.message)
    return {"reply": reply}
