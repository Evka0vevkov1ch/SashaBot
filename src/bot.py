from telegram import Update
from telegram.ext import Application
from handlers.admin_handler import AdminHandler
from handlers.citata_handler import CitataHandler
from handlers.redactor_handler import RedactorHandler
from handlers.sasha_handler import SashaHandler
from handlers.start_handler import StartHandler
from config import TOKEN

class Bot:
    def __init__(self):
        self.application = Application.builder().token(TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        admin_handler = AdminHandler(self.application)
        citata_handler = CitataHandler(self.application)
        redactor_handler = RedactorHandler(self.application)
        sasha_handler = SashaHandler(self.application)
        start_handler = StartHandler(self.application)

        admin_handler.register_handlers()
        citata_handler.register_handlers()
        redactor_handler.register_handlers()
        sasha_handler.register_handlers()
        start_handler.register_handlers()

    def run(self):
        self.application.run_polling()

if __name__ == "__main__":
    bot = Bot()
    bot.run()