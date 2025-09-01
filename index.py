from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/download")
def download_info(url: str = Query(..., description="Video URL (YouTube, Facebook, etc.)")):
    ydl_opts = {"quiet": True, "dump_single_json": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [
                {
                    "format_id": f["format_id"],
                    "ext": f["ext"],
                    "resolution": f.get("resolution") or f.get("height"),
                    "filesize": f.get("filesize")
                }
                for f in info["formats"]
                if f.get("filesize")
            ]
            return JSONResponse(content={
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "formats": formats
            })
    except Exception as e:
        return {"error": str(e)}
