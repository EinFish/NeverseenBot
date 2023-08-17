import json



class birthdayinit():
    def bdjson(self, name, description):
        self.name = name
        self.description =description
        try:
            with open('birthdays.json', 'r') as file:
                self.birthdays = json.load(file)
        except FileNotFoundError:
            self.birthdays = {}

        try:
            with open('config.json', 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {'gratulation_channel': None}

    def save_data(self):
        with open('birthdays.json', 'w') as file:
            json.dump(self.birthdays, file, indent=4)
        with open('config.json', 'w') as file:
            json.dump(self.config, file, indent=4)