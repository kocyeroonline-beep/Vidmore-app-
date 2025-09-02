# api/index.py
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Vidmate Backend API running ✅"}

@app.get("/download")
def download_video(url: str = Query(..., description="Video URL to download")):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [
                {
                    "format_id": f["format_id"],
                    "ext": f["ext"],
                    "resolution": f.get("resolution"),
                    "filesize": f.get("filesize"),
                    "url": f.get("url"),
                }
                for f in info["formats"]
                if f.get("url")
            ]
            result = {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "formats": formats,
            }
            return JSONResponse(result)
    except Exception as e:
        return {"error": str(e)}
