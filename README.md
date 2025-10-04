# medassist
Rudimentary chatbot for simulating patient-provider interactions. Not real medical advice. At all. **Model is still in progress!**

▶️ [Watch the demo](docs/Medassist-Demo.mp4)


## Motivations
As a pre-med who studied data science - I am deeply interested in the intersection of
healthcare and AI.

It has been difficult to find available datasets that allow me to truly  explore this interest, but now [thanks to the work](https://arxiv.org/abs/2310.15959) done to produce [NoteChat](https://huggingface.co/datasets/akemiH/NoteChat), the public now has access to a dataset of over 207k patient-provider interactions. 

Largely inspired by this paper, which fine-tunes LLMs on this data, I did the same, just to see for myself the true potential of where medicine and technology may be headed.

I'm still working on the model in of itself - but just wanted to see what I could do in a short amount of time and I think it's pretty cool!

## Quickstart

### Backend 
`cd backend `

`python -m pip install -r requirements.txt`

`uvicorn server:app --reload`

### Frontend
`cd frontend`

`npm install`

`npm run dev`

### Instructions
* Type a message and press `Enter` to send.
* Press `Esc` to clear the chat
* Replies stream in the chat area.

### API 
`GET /` - Server check 

`GET /docs` - UI

`POST /chat` - Main chat body

`POST /reset` - Clears conversation




