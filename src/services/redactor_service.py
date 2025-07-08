import logging
class RedactorService:
    def __init__(self, filename="redactors.txt"):
        self.filename = filename

    def load_redactors(self):
        """Loads the list of redactors from the file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return [int(line.strip()) for line in file if line.strip().isdigit()]
        except Exception as e:
            logging.error(f"❌ Error loading redactors: {e}")
            return []

    def add_redactor(self, user_id):
        """Adds a redactor to the file."""
        try:
            with open(self.filename, "a", encoding="utf-8") as file:
                file.write(str(user_id) + "\n")
            return True
        except Exception as e:
            logging.error(f"❌ Error adding redactor: {e}")
            return False

    def is_redactor(self, user_id):
        """Checks if a user is a redactor."""
        redactors = self.load_redactors()
        return user_id in redactors