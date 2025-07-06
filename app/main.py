from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from app.downloader import download_single_audio, download_playlist_audio, cleanup_temp_files
from app.lyrics_scraper import search_genius_lyrics_and_scrape
from app.lyrics_scraper_ddg import search_lyrics_and_scrape_with_ddg

app = FastAPI()


@app.post("/download/single")
def download_single(url: str = Form(...)):
    try:
        file_path = download_single_audio(url)
        return FileResponse(
            path=file_path,
            filename=file_path.split('/')[-1],
            media_type='audio/mpeg'
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cleanup_temp_files()


@app.post("/download/playlist")
def download_playlist(url: str = Form(...)):
    try:
        zip_file_path, zip_file_name = download_playlist_audio(url)
        return FileResponse(
            path=zip_file_path,
            filename=zip_file_name,
            media_type='application/zip'
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cleanup_temp_files()

@app.get("/song/lyrics")
def get_lyrics(song_name: str):
    try:
        print(f"[INFO] Attempting Brave search for: {song_name}")
        lyrics = search_genius_lyrics_and_scrape(song_name)
        return JSONResponse(content={"song": song_name, "lyrics": lyrics})

    except Exception as e1:
        print(f"[WARN] Brave scraper failed: {e1}")
        try:
            print(f"[INFO] Falling back to DuckDuckGo search for: {song_name}")
            lyrics = search_lyrics_and_scrape_with_ddg(song_name)
            return JSONResponse(content={"song": song_name, "lyrics": lyrics})

        except Exception as e2:
            print(f"[ERROR] DuckDuckGo scraper also failed: {e2}")
            return JSONResponse(content={"status": "Error", "message": f"Brave error: {e1} | DDG error: {e2}"})