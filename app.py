import os

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from msc_project import reduce_fps, get_video_details

app = FastAPI()

templates = Jinja2Templates(directory="./templates")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "msc_project/static"),
    name="static",
)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"message": "index page", "request": request})

@app.post("/upload")
async def upload_video(video: UploadFile):
    filename = video.filename
    with open(f"input/{filename}", "wb") as f:
        content = await video.read()
        f.write(content)
    return {"message": "Video uploaded successfully!"}


@app.get("/video")
def video_endpoint(video_path: str):
    def iterfile():  #
        with open(video_path, mode="rb") as file_like:  #
            yield from file_like  #
    return StreamingResponse(iterfile(), media_type="video/mp4")

@app.get("/processing")
async def process_video(request: Request):
    return templates.TemplateResponse("processing.html", context={"message": "Video Processing", "request": request})

@app.get("/fps_reduce")
async def fps_reduce(request: Request):
    return templates.TemplateResponse("reduce_fps.html", context={"message": "Reduce FPS", "request": request})

@app.get("/video_stats")
async def fps_reduce(request: Request, video_path: str):
    # video_path = "reduce_fps_processing/reduced_fps_video_8_fps.mp4"
    video_stats = get_video_details.get_video_stats(video_path)
    video_stats["video_path"] = video_path
    return templates.TemplateResponse("show_video_and_stats.html", context={"message": "Video Stats", "request": request, "data": video_stats})

@app.post("/reduce_fps_upload")
async def reduce_fps_upload(video: UploadFile, fps: int = Form(...)):
    filename = os.path.join("reduce_fps_processing", video.filename)
    with open(filename, "wb") as f:
        content = await video.read()
        f.write(content)
    reduce_fps_handler = reduce_fps.ReduceFPS(input_file=filename, fps=fps)
    return_handler = reduce_fps_handler.fps_reduction()
    if return_handler:
        print("FPS reduce successfull")
        return RedirectResponse(url=f"/video_stats?video_path={return_handler}", status_code=303)
    else:
        return {"message": "Error in reducing FPS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
