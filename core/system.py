"""
⚡ تشخیص خودکار منابع سیستم
"""
import os
import subprocess
from functools import lru_cache


@lru_cache(maxsize=1)
def get_cpu_cores() -> int:
    return os.cpu_count() or 4


@lru_cache(maxsize=1)
def get_available_encoders() -> dict:
    """تشخیص انکودرهای موجود در FFmpeg"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            capture_output=True, text=True, timeout=10,
        )
        out = result.stdout
        return {
            "h264":  "libx264"     in out,
            "h265":  "libx265"     in out,
            "vp9":   "libvpx-vp9"  in out,
            "av1":   "libaom-av1"  in out,
            "nvenc": "h264_nvenc"  in out,
            "qsv":   "h264_qsv"    in out,
            "opus":  "libopus"     in out,
            "aac":   "aac"         in out,
            "mp3":   "libmp3lame"  in out,
        }
    except Exception:
        return {"h264": True, "aac": True}


@lru_cache(maxsize=1)
def get_available_tools() -> dict:
    """تشخیص ابزارهای نصب‌شده"""
    tools = {}
    for t in ["zstd", "7z", "brotli", "gs", "cwebp", "mozjpeg", "optipng", "pngquant"]:
        try:
            subprocess.run([t, "--version"], capture_output=True, timeout=3)
            tools[t] = True
        except Exception:
            try:
                subprocess.run([t, "-version"], capture_output=True, timeout=3)
                tools[t] = True
            except Exception:
                tools[t] = False
    return tools


def get_best_video_encoder() -> str:
    """انتخاب بهترین انکودر ویدئو موجود"""
    enc = get_available_encoders()
    if enc.get("nvenc"): return "h264_nvenc"
    if enc.get("qsv"):   return "h264_qsv"
    if enc.get("h264"):  return "libx264"
    return "libx264"


def get_system_info() -> dict:
    """خلاصه وضعیت سیستم"""
    return {
        "cores":    get_cpu_cores(),
        "encoder":  get_best_video_encoder(),
        "encoders": get_available_encoders(),
        "tools":    get_available_tools(),
    }
