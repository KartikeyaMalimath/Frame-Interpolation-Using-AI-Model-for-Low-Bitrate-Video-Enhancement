import os
import psutil

from fastapi import FastAPI, Request, UploadFile, Form, BackgroundTasks
from fastapi.responses import StreamingResponse, RedirectResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from moviepy.editor import VideoFileClip

from msc_project import reduce_fps, get_video_details, split_frame
from msc_project.frame_interpolation import FrameInterpolation
from msc_project.merge_frames import MergeFrames

app = FastAPI()

templates = Jinja2Templates(directory="./templates")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "msc_project/static"),
    name="static",
)

# A global variable to store the status and result of the task
task_status = {"done": False, "result": None}
def interpolation_task(current_fps: int, target_fps: int, input_video: str):
    global task_status
    split_frame_handler = split_frame.SplitFrame(input_video_path=input_video)
    split_frame_handler.split_frame() #split input video to frame images
    split_frame_handler.split_audio() #split and store audio from the input video
    frame_interpolation_handler = FrameInterpolation(current_fps=current_fps, target_fps=target_fps)
    return_flag = frame_interpolation_handler.initiate_interpolation()
    if return_flag:
        clip = VideoFileClip(input_video)
        duration = clip.duration
        merge_frame_handler = MergeFrames(duration=duration)
        merge_ret = merge_frame_handler.merge_frames()
        if merge_ret:
            video_stats = get_video_details.get_video_stats(merge_ret)
            task_status["result"] = merge_ret
            task_status["done"] = True

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"message": "index page", "request": request})

@app.get("/processing")
async def process_video(request: Request, video_path: str, target_fps: int):
    video_stats = get_video_details.get_video_stats(video_path)
    video_stats["video_path"] = video_path
    video_stats["target_fps"] = target_fps
    return templates.TemplateResponse("processing.html", context={"message": "Video Processing", "request": request, "data": video_stats})

@app.post("/upload")
async def upload_video(video: UploadFile, fps: int = Form(...)):
    filename = os.path.join("input", video.filename)
    with open(filename, "wb") as f:
        content = await video.read()
        f.write(content)
    print("video uploaded successfully")
    return RedirectResponse(url=f"/processing?video_path={filename}&target_fps={fps}", status_code=303)

@app.get("/video")
def video_endpoint(video_path: str):
    def iterfile():  #
        with open(video_path, mode="rb") as file_like:  #
            yield from file_like  #
    return StreamingResponse(iterfile(), media_type="video/mp4")

@app.get("/fps_reduce")
async def fps_reduce(request: Request):
    return templates.TemplateResponse("reduce_fps.html", context={"message": "Reduce FPS", "request": request})

@app.get("/video_stats")
async def fps_reduce(request: Request, video_path: str):
    # video_path = "reduce_fps_processing/reduced_fps_video_8_fps.mp4"
    video_stats = get_video_details.get_video_stats(video_path)
    video_stats["video_path"] = video_path
    return templates.TemplateResponse("show_video_and_stats.html",
                                      context={"message": "Video Stats",
                                               "request": request, "data": video_stats})

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

@app.post("/system_usage_charts")
async def system_usage__charts(background_tasks: BackgroundTasks, request: Request,
                               current_fps: str = Form(...), target_fps: str = Form(...), input_path: str = Form(...)):
    current_fps = int(round(float(current_fps)))
    target_fps = int(target_fps)
    background_tasks.add_task(interpolation_task, current_fps=current_fps, target_fps=target_fps, input_video=input_path)
    return templates.TemplateResponse("system_usage.html", context={"message": "System Usage", "request": request})

@app.get("/interpolate_status")
async def check_status(request: Request):
    # Check the global variable for the status and result of the task
    global task_status
    if task_status["done"]:
        # Return the second template response with the result
        return PlainTextResponse(f"/video_stats?video_path={task_status['result']}")
    else:
        # Return a message to indicate that the task is not done yet
        return JSONResponse({"message": "Interpolation still in progress"})

@app.get("/system_usage")
async def system_usage(request: Request):
    # Get the CPU and RAM usage
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    # Return the data as a JSON response
    return {"cpu": cpu_usage, "ram": ram_usage}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
