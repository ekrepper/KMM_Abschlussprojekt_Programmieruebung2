import json
from datetime import datetime

class Person:
    def __init__(self, person_dict):
        """
        Initializes a Person object.

        Args:
            person_dict (dict): A dictionary containing the person's information.

        Attributes:
            date_of_birth (str): The date of birth of the person.
            age (int): The age of the person.
            max_hr (int): The maximum heart rate of the person.
            firstname (str): The first name of the person.
            lastname (str): The last name of the person.
            picture_path (str): The path to the person's picture.
            id (int): The ID of the person.
            ekg_tests (list): A list of EKG tests performed on the person.
            intervall_tests (dict): A dictionary of interval tests performed on the person.
        """
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
        """
        Calculates the age of the person based on the current year and the date of birth.

        Returns:
            int: The age of the person.
        """
        today = datetime.today().year
        age = today - self.date_of_birth
        return age

    def calc_max_HR(self):
        """
        Calculates the maximum heart rate for a person.

        Returns:
            int: The maximum heart rate of the person.
        """
        return 220 - self.age

    @staticmethod
    def load_person_data():
        """
        Loads the person database and returns a dictionary with the persons.

        Returns:
            dict: A dictionary containing the person data.
        """
        with open("data/person_db.json", 'r') as file:
            person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """
        Returns a list of all person names from the person data dictionary.

        Args:
            person_data (dict): A dictionary containing the person data.

        Returns:
            list: A list of all person names in the format "lastname, firstname".
        """
        return [f"{entry['lastname']}, {entry['firstname']}" for entry in person_data]

    @staticmethod
    def find_person_data_by_name(full_name):
        """
        Finds and returns person data by the full name string (lastname, firstname).

        Args:
            full_name (str): The full name of the person in the format "lastname, firstname".

        Returns:
            dict: A dictionary containing the person data.
        """
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
        """
        Instantiates a Person object based on the ID from the database.

        Args:
            person_id (int): The ID of the person.

        Returns:
            Person or None: A Person object if the ID is found in the database, None otherwise.
        """
        person_data = Person.load_person_data()
        for entry in person_data:
            if entry["id"] == person_id:
                return Person(entry)
        return None
