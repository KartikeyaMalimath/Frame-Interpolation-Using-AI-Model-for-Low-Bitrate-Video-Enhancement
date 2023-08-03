import os
import cv2

def get_video_stats(video_path):
    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_size_in_KB = os.path.getsize(video_path) / 1024

    return {"width": width, "height": height, "fps": fps, "total_frames": total_frames, "size": round(video_size_in_KB, 2)}

if __name__ == "__main__":
    video_path = "reduce_fps_processing/reduced_fps_video_8_fps.mp4"
    video_stats = get_video_stats(video_path)
    print("Video resolution: {}x{}".format(video_stats.get("width"), video_stats.get("height")))
    print("Video FPS: {}".format(video_stats.get("fps")))
    print("Total frames: {}".format(video_stats.get("total_frames")))
    print("Video Size : {} Kb".format(video_stats.get("size")))