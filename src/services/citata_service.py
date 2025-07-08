import logging, random, os
class CitataService:
    def __init__(self, citations_file="sasha_citates.txt"):
        self.citations_file = citations_file

    def get_random_citation(self):
        with open(self.citations_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return random.choice(lines).strip() if lines else None

    def add_citation(self, citation):
        try:
            with open(self.citations_file, "a", encoding="utf-8") as file:
                file.write(citation + "\n")
            return True
        except Exception as e:
            logging.error(f"Error adding citation: {e}")
            return False

    def is_empty(self):
        return os.path.getsize(self.citations_file) == 0