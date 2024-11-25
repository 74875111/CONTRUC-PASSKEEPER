import json

class Localization:
    def __init__(self, language):
        self.language = language
        self.translations = self.load_translations()

    def load_translations(self):
        with open(f'locales/{self.language}.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def translate(self, key, **kwargs):
        translation = self.translations.get(key, key)
        return translation.format(**kwargs)

    def set_language(self, language):
        self.language = language
        self.translations = self.load_translations()