from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

nvai_url = "https://ai.api.nvidia.com/v1/vlm/microsoft/florence-2"
header_auth = f'Bearer {os.getenv("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", "")}'
DETAILED_CAPTION_PROMPT = "<DETAILED_CAPTION>"

def _upload_asset(input: bytes, description: str) -> str:
    """Uploads an asset to the NVIDIA API."""
    authorize = requests.post(
        "https://api.nvcf.nvidia.com/v2/nvcf/assets",
        headers={
            "Authorization": header_auth,
            "Content-Type": "application/json",
            "accept": "application/json",
        },
        json={"contentType": "image/jpeg", "description": description},
        timeout=30,
    )
    authorize.raise_for_status()

    response = requests.put(
        authorize.json()["uploadUrl"],
        data=input,
        headers={
            "x-amz-meta-nvcf-asset-description": description,
            "content-type": "image/jpeg",
        },
        timeout=300,
    )
    response.raise_for_status()
    return str(authorize.json()["assetId"])

def _generate_content(asset_id: str) -> str:
    """Generates the content string for the detailed caption task."""
    return f'{DETAILED_CAPTION_PROMPT}<img src="data:image/jpeg;asset_id,{asset_id}" />'

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the HTML form for the user interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Caption Generator</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Generate Detailed Caption</h1>
        <form action="/generate" method="post" enctype="multipart/form-data">
            <label for="image">Upload Image:</label>
            <input type="file" id="image" name="image" accept="image/*" required><br><br>
            <button type="submit">Generate</button>
        </form>
        <div id="result">
            <h2>Result:</h2>
            <textarea id="output" rows="10" cols="50" readonly></textarea>
        </div>
    </body>
    </html>
    """

@app.post("/generate")
async def generate_caption(image: UploadFile = File(...)):
    """Processes the uploaded image and returns the detailed caption."""
    if not header_auth:
        raise HTTPException(status_code=500, detail="API_KEY not set. Please configure the environment variable.")

    try:
        image_bytes = await image.read()
        asset_id = _upload_asset(image_bytes, description=image.filename)
        content = _generate_content(asset_id)

        inputs = {
            "messages": [{
                "role": "user",
                "content": content
            }]
        }

        headers = {
            "Content-Type": "application/json",
            "NVCF-INPUT-ASSET-REFERENCES": asset_id,
            "NVCF-FUNCTION-ASSET-IDS": asset_id,
            "Authorization": header_auth,
            "Accept": "application/json"
        }

        response = requests.post(nvai_url, headers=headers, json=inputs, timeout=300)
        response.raise_for_status()
        result = response.json().get("messages", [{}])[0].get("content", "No result returned.")

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))