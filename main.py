import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])


class VideoProcessRequest(BaseModel):
    model_path: str = "best.pt"
    video_name: str

@app.post("/process_video/")
async def process_video(video_request: VideoProcessRequest):

    video_path = video_request.video_name
    if not os.path.isfile(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    command = f"yolo task=detect mode=predict model={video_request.model_path} source={video_path} conf=0.50 save=True"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Video processing failed: {str(e)}")

    return {"message": "Video processing complete"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
