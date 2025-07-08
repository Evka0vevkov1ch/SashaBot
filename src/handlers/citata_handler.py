from config import sashaID
class CitataHandler:
    def __init__(self, citata_service, file_service):
        self.citata_service = citata_service
        self.file_service = file_service

    async def citata_command(self, update, context):
        random_citata = await self.citata_service.get_random_citata()
        reklama = await self.file_service.get_random_line("ad.txt")
        if not random_citata:
            await update.message.reply_text("❌ Ошибка: файл цитат пуст.")
            return
        await update.message.reply_text(f"Как говорил великий Саша...\n\n{random_citata}\n\n\n\nРЕКЛАМА:\n{reklama}")

    async def add_citata(self, update, context):
        redactors = await self.file_service.load_redactors()
        reklama = await self.file_service.get_random_line("ad.txt")
        if update.effective_user.id not in redactors:
            await update.message.reply_text(f"❌ У вас нет прав для добавления цитат.\n\n\nРЕКЛАМА\n{reklama}")
            return

        if context.args:
            citata = " ".join(context.args)
            await self.citata_service.add_citata(citata)
            await update.message.reply_text(f"✅ Цитата успешно добавлена!\n\n\nРЕКЛАМА\n{reklama}")
        elif update.message.reply_to_message:
            if update.message.reply_to_message.from_user.id != sashaID:
                await update.message.reply_text(f"❌ Это не сообщение Саши.\n\n\nРЕКЛАМА\n{reklama}")
                return
            citata = update.message.reply_to_message.text
            await self.citata_service.add_citata(citata)
            await update.message.reply_text(f"✅ Цитата успешно добавлена!\n\n\nРЕКЛАМА\n{reklama}")
        else:
            await update.message.reply_text(
                "❌ Вы должны ответить этой командой на сообщение с цитатой.\n"
                "Или написать команду с текстом цитаты.\nПример: /add_citata текст\n\n\nРЕКЛАМА\n{reklama}"
            )