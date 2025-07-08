from telegram import Update
from telegram.ext import ContextTypes
import random
from services.ai_service import AIService
from services.file_service import FileService
from config import sashaID

class SashaHandler:
    def __init__(self, ai_service: AIService, file_service: FileService):
        self.ai_service = ai_service
        self.file_service = file_service

    async def sasha_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        reklama = await self.file_service.get_random_line("ad.txt")
        
        if not message.reply_to_message:
            await message.reply_text(f"❌ Ты должен ответить этой командой на сообщение Саши!\n\n\nРЕКЛАМА\n{reklama}")
            return
        
        replied_message = message.reply_to_message

        if replied_message.from_user.id != sashaID:
            await message.reply_text(f"❌ Это сообщение не от Саши!\n\n\nРЕКЛАМА\n{reklama}")
            return

        text = replied_message.text
        if not text:
            await message.reply_text(f"❌ В сообщении нет текста!\n\n\nРЕКЛАМА\n{reklama}")
            return

        ai_response = await self.ai_service.get_ai_response(text)
        reply_text = f"💬 Саша скорее всего имел в виду:\n\n{ai_response}\n\n\nРЕКЛАМА\n{reklama}"
        await update.message.reply_text(reply_text)