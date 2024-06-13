import json
import os

DATA_FILE = "data.json"


def load_data():
    """Load data from data.json file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "User": {},
        "Place": {},
        "Review": {},
        "City": {},
        "Country": {},
        "Amenity": {}
        }


def save_data(data):
    """Save data to data.json file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


class DataManager():
    """Class to manage all Data and CRUD methods"""
    storage = load_data()
    objects = {}

    @classmethod
    def save(self, identifier, data_type, object):
        """Save Data to storage"""
        if data_type not in self.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        self.storage[data_type][identifier] = object.to_dict()
        self.objects[identifier] = object
        save_data(self.storage)

    @classmethod
    def get(self, identifier, data_type):
        """Retrieve Data from storage with given identifier"""
        if data_type not in self.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        return self.objects[identifier]

    @classmethod
    def reload(self, identifier, data_type):
        """Retrieve Data from storage with given identifier"""
        if data_type not in self.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier not in self.storage[data_type]:
            return None
        return self.storage[data_type][identifier]

    @classmethod
    def update(self, identifier, data_type, object):
        """Update data from storage"""
        if data_type not in self.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier in self.storage[data_type]:
            self.storage[data_type][identifier] = object.to_dict()
            self.objects[identifier] = object
        else:
            raise ValueError(f"{data_type} '{identifier}' does not exist")

    @classmethod
    def delete(self, identifier, data_type):
        """Delete Data from storage with identifier"""
        if data_type not in self.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier in self.storage[data_type]:
            del self.storage[data_type][identifier]
            save_data(self.storage)
            del self.objects[identifier]
        else:
            raise ValueError(f"{data_type} '{identifier}' does not exist")

    @classmethod
    def all(self, data_type):
        """Retrieve all Data of given Data type"""
        if data_type not in self.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        return list(self.storage[data_type].values())
