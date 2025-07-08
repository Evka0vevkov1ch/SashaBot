from telegram import Update
from telegram.ext import ContextTypes
from config import AdminID
import logging

class AdminHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Stops the bot (available only to the administrator)."""
        if update.effective_user.id != AdminID:
            await update.message.reply_text("❌ У вас нет прав для остановки бота.")
            return

        await update.message.reply_text("🛑 Бот отключается...")
        self.logger.info("🛑 Бот был остановлен администратором.")
        exit(0)  # Terminate the program

    async def add_redactor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Adds a redactor to the database."""
        if update.effective_user.id != AdminID:
            await update.message.reply_text("❌ У вас нет прав для добавления редакторов.")
            return

        if context.args:
            user_id = context.args[0]

            try:
                with open("redactors.txt", "a", encoding="utf-8") as file:
                    file.write(str(user_id) + "\n")

                await update.message.reply_text(f"✅ Редактор с ID {user_id} успешно добавлен!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка при добавлении редактора: {e}")
            return
        elif update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
            try:
                with open("redactors.txt", "a", encoding="utf-8") as file:
                    file.write(str(user_id) + "\n")

                await update.message.reply_text(f"✅ Редактор с ID {user_id} успешно добавлен!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка при добавлении редактора: {e}")
            return
        else:
            await update.message.reply_text(
                "❌ Вы должны ответить этой командой на сообщение пользователя, которого хотите добавить в редакторы.\n"
                "Или написать команду с ID пользователя.\nПример: /add_redactor 123456789"
            )