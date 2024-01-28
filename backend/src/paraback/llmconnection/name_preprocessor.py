from tqdm import tqdm

from paraback.models.law_model import Law
from openai import OpenAI
import json

from paraback.saving.mongo_connector import MongoConnector


class NamePreprocessor:
    """Preprocesses Law names for the Linking mechanism."""

    def __init__(self, law: Law):
        self.law = law

    @staticmethod
    def get_all_names(laws):
        """Preprocesses all Law names for the Linking mechanism."""
        io = MongoConnector()
        io.clear_names()
        names_dict = {}
        for law in tqdm(laws):
            name_processor = NamePreprocessor(law)
            variants = name_processor.get_variants()
            my_dict = {string : law.stemmedabbreviation for string in variants}
            names_dict.update(my_dict)
        return names_dict

    def get_variants(self):
        """Preprocesses the name."""
        liste = [self.law.abbreviation, self.law.title]

        example1 = ["BGB", "Bürgerliches Gesetzbuch"]
        solution1 = ["BGB", "BGBs", "Bürgerliches Gesetzbuch", "Bürgerlichen Gesetzbuchs", "Bürgerlichen Gesetzbuch"]
        example2 = ["AktG", "Aktiengesetz"]
        solution2 = ["AktG", "AktGs", "Aktiengesetz", "Aktiengesetzes"]

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_format = { "type": "json_object" },
            messages=[
                {"role": "system", "content": "Du bist ein linguistisches System, welches Gesetzesnamen in alle grammatikalischen Fälle dekliniert. Du antwortest nur mit JSON und dem key 'Kasus' mit einer Liste von Gesetzesnamen."},
                {"role": "user", "content": str(example1)},
                {"role": "assistant", "content": '{"Kasus": ["' + '", "'.join(solution1) + '"]}'},
                {"role": "user", "content": str(example2)},
                {"role": "assistant", "content": '{"Kasus": ["' + '", "'.join(solution2) + '"]}'},
                {"role": "user", "content": str(liste)},
            ]
        )

        return list(set(json.loads(completion.choices[0].message.content)["Kasus"]))