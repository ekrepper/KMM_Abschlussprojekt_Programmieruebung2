import json
from datetime import datetime

class Person:
    def __init__(self, person_dict):
        self.date_of_birth = person_dict["date_of_birth"]
        self.age = self.calculate_age()
        self.max_hr = self.calc_max_HR()
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.ekg_tests = person_dict["ekg_tests"]
        self.intervall_tests = person_dict.get("intervall_tests", {})

    def calculate_age(self):
        today = datetime.today().year
        age = today - self.date_of_birth
        return age

    def calc_max_HR(self):
        """Calculates the maximum heart rate for a person."""
        return 220 - self.age

    @staticmethod
    def load_person_data():
        """Loads the person database and returns a dictionary with the persons."""
        with open("data/person_db.json", 'r') as file:
            person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """Returns a list of all person names from the person data dictionary."""
        return [f"{entry['lastname']}, {entry['firstname']}" for entry in person_data]

    @staticmethod
    def find_person_data_by_name(full_name):
        """Finds and returns person data by the full name string (lastname, firstname)."""
        person_data = Person.load_person_data()

        if full_name == "None":
            return {}

        lastname, firstname = full_name.split(", ")

        for entry in person_data:
            if entry["lastname"] == lastname and entry["firstname"] == firstname:
                return entry
        return {}

    @staticmethod
    def load_by_id(person_id):
        """Instantiates a Person object based on the ID from the database."""
        person_data = Person.load_person_data()
        for entry in person_data:
            if entry["id"] == person_id:
                return Person(entry)
        return None
