from bot import Bot
from config import TOKEN

def main():
    bot = Bot(TOKEN)
    bot.run()

if __name__ == "__main__":
    main()