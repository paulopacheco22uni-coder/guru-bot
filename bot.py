import os
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
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.PHOTO, lidar_com_foto))
    
    # Obtém a porta atribuída pelo Render (essencial para web services)
    port = int(os.environ.get("PORT", "10000"))
    
    print("🤖 Bot do Guru a arrancar via webhook...")
    
    # Arranca em modo webhook para o Render ficar feliz e não fechar a ligação
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN if os.environ.get("RENDER_EXTERNAL_URL") else None
    )
