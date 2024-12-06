from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from model.translator import Translator

app = FastAPI()
translator = Translator()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, user_input: str = Form(...)):
    translated_text = translator.translate_text(user_input)
    params = {"request": request, "translate": translated_text}
    return templates.TemplateResponse("index.html", params)
