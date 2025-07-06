import subprocess
import logging

logger = logging.getLogger(__name__)
process = None

def start_stream(m3u8_url: str, rtmp_url: str):
    global process
    if process and process.poll() is None:
        raise Exception("A stream is already running. Use /stop to end it first.")

    # FFmpeg command to stream M3U8 to RTMP
    cmd = [
        "ffmpeg",
        "-i", m3u8_url,
        "-c:v", "copy",
        "-c:a", "aac",
        "-f", "flv",
        rtmp_url
    ]
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Started streaming {m3u8_url} to {rtmp_url}")
    except Exception as e:
        logger.error(f"Failed to start stream: {e}")
        raise e

def stop_stream():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
        logger.info("Stream stopped.")
    process = None
