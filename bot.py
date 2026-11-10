import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "9126886161:AAFG_yGcdt0FH-_ofjHtGobtG0JWfI_BGzE"

async def lidar_com_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Mestre, print recebido! A preparar o radar para cruzar os dados com o SofaScore...")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, lidar_com_foto))
    print("🤖 Bot do Guru a postos na nuvem...")
    app.run_polling()
