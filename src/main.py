from datetime import datetime

import webdav3
from fastapi import FastAPI, File, Form
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.requests import Request
from filetype import image_match
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from .config import client
from .config import cfg
from .functions import upload_file


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="templates")
template.env.globals['year'] = datetime.now().strftime("%Y")
template.env.globals['site_title'] = cfg.site_title
template.env.globals['site_name'] = cfg.site_name


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return template.TemplateResponse("index.html", {"request": request, "data": {}})


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return template.TemplateResponse("about.html", {"request": request, 'bot_link': cfg.tg_bot_link})


@app.get("/screenshot/{screenshot_path:path}")
def screenshot(screenshot_path: str, request: Request):
    path = f'{cfg.webdav_base_dir}/{screenshot_path}'

    try:
        info = client.info(path)
    except webdav3.exceptions.RemoteResourceNotFound:
        return template.TemplateResponse("screenshot_not_found.html", {"request": request}, status_code=404)

    data = {
        **info,
        "path": f'/download/{screenshot_path}',
    }

    return template.TemplateResponse("screenshot.html", {"request": request, "data": data})


@app.get("/download/{screenshot_path:path}")
def download(screenshot_path: str):
    path = f'{cfg.webdav_base_dir}/{screenshot_path}'

    try:
        info = client.info(path)
    except webdav3.exceptions.RemoteResourceNotFound:
        return JSONResponse(content={"message": "Image Not Found"}, status_code=404)

    return StreamingResponse(client.download_iter(path), media_type=info['content_type'])


@app.post("/upload-api")
async def upload_api(request: Request):
    token = request.headers.get('X-TOKEN')
    if token != cfg.access_token:
        return JSONResponse(content={"success": False, "message": "Invalid token in header"}, status_code=401)

    body = b''
    async for chunk in request.stream():
        body += chunk

    kind = image_match(body)
    if kind is None:
        return JSONResponse(content={"success": False, "message": "Cannot guess file type"}, status_code=400)

    file_path = cfg.site_name + '/' + upload_file(body, kind.extension)

    return {"success": True, "filepath": file_path}


@app.get("/upload", response_class=HTMLResponse)
def upload(request: Request):
    return template.TemplateResponse("upload.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
def upload_post(request: Request, image: bytes = File(), token: str = Form()):
    error = None

    if token != cfg.access_token:
        error = 'Указан неверный токен доступа!'

    kind = image_match(image)
    if kind is None:
        error = 'Загружаемый файл не является изображением!'

    if error is not None:
        return template.TemplateResponse("upload.html", {"request": request, 'error': error})

    file_path = cfg.site_name + '/' + upload_file(image, kind.extension)

    return template.TemplateResponse("upload.html", {"request": request, 'file_path': file_path})

