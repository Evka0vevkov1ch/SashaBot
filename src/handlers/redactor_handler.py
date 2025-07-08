from telegram import Update
from telegram.ext import ContextTypes
from services.redactor_service import RedactorService
from services.file_service import FileService
import random
import logging

class RedactorHandler:
    def __init__(self, redactor_service: RedactorService, file_service: FileService):
        self.redactor_service = redactor_service
        self.file_service = file_service

    async def add_redactor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id != self.redactor_service.admin_id:
            await update.message.reply_text("❌ У вас нет прав для добавления редакторов.")
            return

        if context.args:
            user_id = context.args[0]

            try:
                self.redactor_service.add_redactor(user_id)
                await update.message.reply_text(f"✅ Редактор с ID {user_id} успешно добавлен!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка при добавлении редактора: {e}")
            return
        elif update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            try:
                self.redactor_service.add_redactor(user_id)
                await update.message.reply_text(f"✅ Редактор с ID {user_id} успешно добавлен!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка при добавлении редактора: {e}")
            return
        else:
            await update.message.reply_text(
                "❌ Вы должны ответить этой командой на сообщение пользователя, которого хотите добавить в редакторы.\n"
                "Или написать команду с ID пользователя.\nПример: /add_redactor 123456789"
            )

    async def list_redactors(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        redactors = self.redactor_service.get_redactors()
        if not redactors:
            await update.message.reply_text("❌ Нет редакторов.")
            return

        redactor_list = "\n".join(str(redactor) for redactor in redactors)
        await update.message.reply_text(f"📝 Список редакторов:\n{redactor_list}")