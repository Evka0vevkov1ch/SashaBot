# SashaBot

SashaBot is a Telegram bot designed to help users translate unclear messages from a user named Sasha into clear Russian. The bot also manages quotes attributed to Sasha and allows designated users (redactors) to add new quotes and manage the bot's functionality.

## Features

- **Message Translation**: Translates messages from Sasha into understandable Russian.
- **Quote Management**: Allows users to retrieve random quotes from Sasha and add new quotes.
- **Admin Controls**: Admin users can manage redactors and stop the bot.
- **User-Friendly Interface**: Provides a simple command structure for users to interact with the bot.

## Project Structure

```
sasha-bot
├── src
│   ├── bot.py                # Initializes the Telegram bot and sets up the application.
│   ├── config.py             # Contains configuration constants (TOKEN, sashaID, AIKEY, AdminID).
│   ├── main.py               # Entry point for the application; sets up the bot and starts polling.
│   ├── handlers               # Contains handler classes for different bot functionalities.
│   │   ├── __init__.py       # Marks the handlers directory as a package.
│   │   ├── admin_handler.py   # Manages admin-specific commands and actions.
│   │   ├── citata_handler.py  # Manages commands related to quotes.
│   │   ├── redactor_handler.py # Manages commands related to redactors.
│   │   ├── sasha_handler.py   # Manages commands related to translating messages from Sasha.
│   │   └── start_handler.py   # Manages the start command and sends welcome messages.
│   ├── services               # Contains service classes for handling business logic.
│   │   ├── __init__.py       # Marks the services directory as a package.
│   │   ├── ai_service.py      # Handles interactions with the AI API.
│   │   ├── citata_service.py  # Manages retrieval and storage of quotes.
│   │   ├── file_service.py    # Handles file operations (reading/writing).
│   │   └── redactor_service.py # Manages loading and saving redactor information.
│   └── utils                  # Contains utility functions and classes.
│       ├── __init__.py       # Marks the utils directory as a package.
│       └── logger.py          # Sets up logging for the application.
├── ad.txt                     # Contains advertisement messages for the bot.
├── sasha_citates.txt          # Contains quotes attributed to Sasha.
├── redactors.txt              # Contains a list of user IDs designated as redactors.
└── README.md                  # Documentation for the project, including setup instructions and usage guidelines.
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sasha-bot.git
   cd sasha-bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure the bot by editing the `src/config.py` file with your Telegram bot token and other necessary credentials.

## Usage

- Start the bot by running:
  ```
  python src/main.py
  ```

- Use the following commands in the Telegram chat:
  - `/start` - Start the bot and receive a welcome message.
  - `/sasha` - Translate a message from Sasha.
  - `/citata` - Retrieve a random quote from Sasha.
  - `/add_citata {text}` - Add a new quote to the database (redactors only).
  - `/add_redactor {user_id}` - Add a new redactor (admin only).
  - `/stop` - Stop the bot (admin only).

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.