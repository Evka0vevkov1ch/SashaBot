import random
class FileService:
    def __init__(self, filename):
        self.filename = filename

    def read_lines(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            return file.readlines()

    def write_line(self, line):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(line + "\n")

    def clear_file(self):
        open(self.filename, "w").close()

    def get_random_line(self):
        lines = self.read_lines()
        return random.choice(lines).strip() if lines else None