import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import stream

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /stream <m3u8_link> <rtmp_url> <stream_key> to start streaming to an RTMP server. Use /stop to end the stream.")

async def stream_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the command has enough arguments
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /stream <m3u8_link> <rtmp_url> <stream_key>")
        return

    m3u8_url = context.args[0]
    rtmp_url = context.args[1]
    stream_key = context.args[2]
    rtmp_full_url = f"{rtmp_url}/{stream_key}"

    # Validate M3U8 URL
    if not m3u8_url.endswith(".m3u8"):
        await update.message.reply_text("Please provide a valid M3U8 link.")
        return

    await update.message.reply_text("Starting stream... This may take a moment.")
    try:
        stream.start_stream(m3u8_url, rtmp_full_url)
        await update.message.reply_text(f"Streaming {m3u8_url} to {rtmp_full_url}!")
    except Exception as e:
        logger.error(f"Error streaming: {e}")
        await update.message.reply_text(f"Failed to stream: {str(e)}")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        stream.stop_stream()
        await update.message.reply_text("Stream stopped.")
    except Exception as e:
        logger.error(f"Error stopping stream: {e}")
        await update.message.reply_text(f"Failed to stop stream: {str(e)}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("An error occurred. Please try again.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stream", stream_command))
    app.add_handler(CommandHandler("stop", stop))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
