from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

class StartHandler:
    def __init__(self, bot):
        self.bot = bot

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        userID = update.effective_user.id
        
        if userID == context.bot.config.ADMIN_ID:
            await self.nnstart(update, context)
        elif userID in context.bot.redactors:
            await self.rstart(update, context)
        else:
            await self.nstart(update, context)

    async def nnstart(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("Добавить редактора", callback_data="ain_redactoradd")],
            [InlineKeyboardButton("Остановить бота", callback_data="ain_stop")],
            [InlineKeyboardButton("Перезапустить бота", callback_data="ain_restart")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 Привет! Я бот, который помогает переводить непонятные сообщения Саши на нормальный русский.\n"
            "Используй команду /sasha, чтобы перевести сообщение от Саши.\n"
            "Используй команду /citata, чтобы увидеть его цитату.\n"
            "Используй команду /add_citata, чтобы добавить новую цитату в базу данных.\n"
            "Используй команду /add_redactor, чтобы добавить нового редактора в базу данных.\n"
            "Используй команду /stop, чтобы остановить бота.",
            reply_markup=reply_markup
        )

    async def rstart(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("Добавить цитату", callback_data="rin_add_citata")],
            [InlineKeyboardButton("Посмотреть цитату", callback_data="rin_view_citatas")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = (
            "👋 *Привет, редактор!*\n\n"
            "Вы можете использовать следующие команды:\n"
            "- `/add_citata {текст}` — добавить новую цитату.\n"
            "- `/citata` — посмотреть случайную цитату.\n"
        )
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    async def nstart(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = "👋 Привет! *Я бот, который помогает переводить непонятные сообщения Саши на нормальный русский.*\n" \
               "Используй команду */sasha*, чтобы перевести сообщение от *Саши*.\n" \
               "Используй команду */citata*, чтобы увидеть его цитату.\n"
        await update.message.reply_text(text, parse_mode="MarkdownV2")