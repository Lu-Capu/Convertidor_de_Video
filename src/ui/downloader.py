import os
import static_ffmpeg
import yt_dlp
from config import DESCARGAS_DIR

static_ffmpeg.add_paths()



class Downloader:
    def descargar_video(self, option: int, link: str) -> tuple[bool, str]:
        os.makedirs(DESCARGAS_DIR, exist_ok=True)

        if option == 1:
            
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": os.path.join(DESCARGAS_DIR, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "noplaylist": True,
                "restrictfilenames": True,
                "retries": 10,
                "quiet": True,
                "no_warnings": True,
            }
        else:

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(DESCARGAS_DIR, "%(title)s.%(ext)s"),
                "noplaylist": True,
                "restrictfilenames": True,
                "retries": 10,
                "quiet": True,
                "no_warnings": True,
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                codigo = ydl.download([link])
            if codigo == 0:
                return True, f"Descarga completada en {DESCARGAS_DIR}"
            return False, "La descarga terminó con errores."
        except Exception as e:
            return False, f"Hubo un problema al descargar: {e}"