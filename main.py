import requests, random, logging, sys, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, CallbackContext, CallbackQueryHandler, InlineQueryHandler
from config import TOKEN, sashaID, AIKEY, AdminID
CITATIONS_FILE = "sasha_citates.txt"
REDACTORS = "redactors.txt"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

API_KEY = AIKEY  
BOT_TOKEN = TOKEN  
TARGET_USER_ID = sashaID  

async def eget_random_line(filename="ad.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return random.choice(lines).strip()
async def get_ai_response(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": (
                "Ты переводчик с непонятного языка на нормальный русский. "
                "Отвечай только на русском языке. "
                "Переводи суть кратко, без пояснений и анализа."
            )},
            {"role": "user", "content": f"Переведи на нормальный русский:\n{text}"}
        ],
        "temperature": 0.1  
    }

    try:
        response = requests.post(url, headers=headers, json=json_data)
        response_json = response.json()
        ai_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        if not ai_text:
            logging.warning("⚠️ OpenRouter вернул пустой ответ")
            return "Я не понял, что он сказал 🤷‍♂️"

        return ai_text
    except Exception as e:
        logging.error(f"❌ Ошибка AI: {e}")
        return "Ошибка AI, попробуй позже!"
async def status_command(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Бот работает!")
async def sasha_command(update: Update, context: CallbackContext):
    message = update.message
    reklama = await eget_random_line()
    if not message.reply_to_message:
        await message.reply_text(f"❌ Ты должен ответить этой командой на сообщение Саши!\n\n\nРЕКЛАМА\n{reklama}")
        return
    
    replied_message = message.reply_to_message

    if replied_message.from_user.id != TARGET_USER_ID:
        await message.reply_text(f"❌ Это сообщение не от Саши!\n\n\nРЕКЛАМА\n{reklama}")
        return

    text = replied_message.text
    if not text:
        await message.reply_text(f"❌ В сообщении нет текста!\n\n\nРЕКЛАМА\n{reklama}")
        return

    ai_response = await get_ai_response(text)
    reply_text = f"💬 Саша скорее всего имел в виду:\n\n{ai_response}\n\n\nРЕКЛАМА\n{reklama}"
    await update.message.reply_text(reply_text)
async def get_random_line(filename="sasha_citates.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return random.choice(lines).strip()
async def citata_sash(update: Update, context: CallbackContext):
    random_citata = await get_random_line()
    reklama = await eget_random_line()
    if not random_citata:
        await update.message.reply_text("❌ Ошибка: файл цитат пуст.")
        return
    await update.message.reply_text(f"Как говорил великий Саша...\n\n{random_citata}\n\n\n\nРЕКЛАМА:\n{reklama}")
def load_redactors(filename="redactors.txt"):
    """Загружает список редакторов из файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [int(line.strip()) for line in file if line.strip().isdigit()]
    except Exception as e:
        logging.error(f"❌ Ошибка при загрузке редакторов: {e}")
        return []
async def add_citata(update: Update, context: CallbackContext) -> None:
    """Добавляет цитату в файл через команду /add_citata {текст}."""
    redactors = load_redactors()  # Загружаем актуальный список редакторов
    reklama = await eget_random_line()
    if update.effective_user.id not in redactors:
        await update.message.reply_text(f"❌ У вас нет прав для добавления цитат.\n\n\nРЕКЛАМА\n{reklama}")
        return

    if context.args:
        
    
        citata = " ".join(context.args)  # Объединяем аргументы в строку

        try:
            with open(CITATIONS_FILE, "a", encoding="utf-8") as file:
                file.write(citata + "\n")

            await update.message.reply_text(f"✅ Цитата успешно добавлена!\n\n\nРЕКЛАМА\n{reklama}")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при добавлении цитаты: {e}\n\n\nРЕКЛАМА\n{reklama}")
            
    elif update.message.reply_to_message:
        if update.message.reply_to_message.from_user.id != sashaID:
            await update.message.reply_text(f"❌Это не сообщение Саши.\n\n\nРЕКЛАМА\n{reklama}")    
            return
        citata = update.message.reply_to_message.text
        try:
            with open(CITATIONS_FILE, "a", encoding="utf-8") as file:
                file.write(citata + "\n")

            await update.message.reply_text(f"✅ Цитата успешно добавлена!\n\n\nРЕКЛАМА\n{reklama}")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при добавлении цитаты: {e}\n\n\nРЕКЛАМА\n{reklama}")
    else:
        await update.message.reply_text(
            "❌ Вы должны ответить этой командой на сообщение с цитатой.\n"
            f"Или написать команду с текстом цитаты.\nПример: /add_citata текст\n\n\nРЕКЛАМА\n{reklama}"
        )
        return                    
async def stop_command(update: Update, context: CallbackContext) -> None:
    """Останавливает бота (доступно только администратору)."""
    if update.effective_user.id != AdminID:  # Проверяем, что команду вызывает администратор
        await update.message.reply_text("❌ У вас нет прав для остановки бота.")
        return

    await update.message.reply_text("🛑 Бот отключается...")
    logging.info("🛑 Бот был остановлен администратором.")
    sys.exit(0)  # Завершаем выполнение программы
async def nnstart(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Добавить редактора", callback_data="ain_redactoradd")],
        [InlineKeyboardButton("Остановить бота", callback_data="ain_stop")],
        [InlineKeyboardButton("перезапустить бота", callback_data="ain_restart")],
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
async def redactorstarthandler(update: Update, context: CallbackContext):
    query = update.callback_query
    chatid = update.effective_user.id  # Получаем ID чата
    await query.answer()  # Отвечаем на callback, чтобы убрать "часики" в Telegram
    
    if query.data == "rin_add_citata":
        await query.edit_message_text("Ответьте на сообщение пользователя и используйте команду /add_citata.")
    elif query.data == "rin_view_citatas":
        random_citata = await get_random_line()
        if not random_citata:
            return
        await context.bot.send_message(chat_id=chatid, text=f"Как говорил великий Саша...\n\n{random_citata}")
async def handle_admin_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Отвечаем на callback, чтобы убрать "часики" в Telegram

    if query.data == "ain_redactoradd":
        await query.edit_message_text("Ответьте на сообщение пользователя и используйте команду /add_redactor.")
    elif query.data == "ain_stop":
        await stop_command(update, context) 
    elif query.data == "ain_restart":
        await query.edit_message_text("🛑 Бот перезапускается...")
        logging.info("🛑 Бот был перезапущен администратором.")
        os.execv(sys.executable, ['python'] + sys.argv)  
async def rstart(update: Update, context: CallbackContext):
    """Функция для редактора при вызове команды /start."""
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
async def start(update: Update, context: CallbackContext):
    userID = update.effective_user.id  # Получаем ID пользователя
    
    if userID == AdminID:
        await nnstart(update, context)  # Вызываем функцию с аргументами
    #elif userID in load_redactors():  # Проверяем, есть ли userID в списке редакторов
        #await rstart(update, context)  # Вызываем функцию с аргументами
    else:
        await nstart(update, context)  # Вызываем функцию с аргументами
async def nstart(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение при запуске бота."""
    text="👋 Привет\\! *Я бот, который помогает переводить непонятные сообщения Саши на нормальный русский\.*\n" \
     "Используй команду */sasha*, чтобы перевести сообщение от *Саши*\.\n" \
     "Используй команду */citata*, чтобы увидеть его цитату\.\n" \
        
    await update.message.reply_text(text, parse_mode="MarkdownV2")
async def add_redactor(update: Update, context: CallbackContext) -> None:
    """Добавляет редактора в базу данных."""
    if update.effective_user.id != AdminID:  # Проверяем, что команду вызывает администратор
        await update.message.reply_text("❌ У вас нет прав для добавления редакторов.")
        return

    if context.args:
        user_id = context.args[0]  # Получаем ID пользователя из аргументов

        try:
            with open("redactors.txt", "a", encoding="utf-8") as file:
                file.write(str(user_id) + "\n")  # Преобразуем user_id в строку

            await update.message.reply_text(f"✅ Редактор с ID {user_id} успешно добавлен!")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при добавлении редактора: {e}")
        return
    elif update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            with open("redactors.txt", "a", encoding="utf-8") as file:
                file.write(str(user_id) + "\n")  # Преобразуем user_id в строку

            await update.message.reply_text(f"✅ Редактор с ID {user_id} успешно добавлен!")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при добавлении редактора: {e}")
        return
    else:
        await update.message.reply_text(
            "❌ Вы должны ответить этой командой на сообщение пользователя, которого хотите добавить в редакторы.\n"
            "Или написать команду с ID пользователя.\nПример: /add_redactor 123456789"
        )
        return
async def get_username_by_chat_id(chat_id: int, context: CallbackContext) -> str:
    try:
        chat = await context.bot.get_chat(chat_id)
        return chat.username or chat.first_name or "Неизвестный пользователь"
    except Exception as e:
        logging.error(f"Ошибка при получении имени пользователя: {e}")
        return "Ошибка"
def create_file_if_not_exists(filename):
    open(filename, "a").close()
async def delete_message(update: Update, context: CallbackContext) -> None:
    """Удаляет сообщение, на которое отвечает пользователь."""
    if update.message.reply_to_message:
        try:
            chat_id = update.message.chat_id
            message_id = update.message.reply_to_message.message_id
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            
        except Exception as e:
            print(f"❌ Ошибка при удалении сообщения: {e}")
    else:
        print("❌ Вы должны ответить этой командой на сообщение, которое хотите удалить.")



def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    redactors = (load_redactors())
    
    app.add_handler(CommandHandler("status", status_command, filters=filters.ChatType.PRIVATE))
    app.add_handler(CommandHandler("sasha", sasha_command))
    app.add_handler(CommandHandler("citata", citata_sash))
    app.add_handler(CommandHandler("add_citata", add_citata))
    app.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))
    app.add_handler(CommandHandler("add_redactor", add_redactor, filters=filters.ChatType.PRIVATE))
    app.add_handler(CommandHandler("stop", stop_command, filters= filters.User(AdminID) & filters.ChatType.PRIVATE))
    app.add_handler(CommandHandler("delete_message", delete_message, filters=filters.User(AdminID)))
    
    app.add_handler(CallbackQueryHandler(handle_admin_buttons, pattern="ain_.*")) 
    app.add_handler(CallbackQueryHandler(redactorstarthandler, pattern="rin_.*"))
    
    create_file_if_not_exists(CITATIONS_FILE)
    create_file_if_not_exists(REDACTORS)
    logging.info("🤖 Бот запущен...")
    app.run_polling()
if __name__ == "__main__":
    main()
