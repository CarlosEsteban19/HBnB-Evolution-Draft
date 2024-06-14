import json
import os

DATA_FILE = "data.json"


def load_data():
    """Load data from data.json file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            storage = {
                "User": {},
                "Place": {},
                "Review": {},
                "City": {},
                "Country": {},
                "Amenity": {}
            }
            objects = {}

            for data_type, items in loaded_data.items():
                for identifier, obj_data in items.items():
                    if data_type == "User":
                        from Models.user import User
                        obj = User.from_dict(obj_data)
                    elif data_type == "Place":
                        from Models.place import Place
                        obj = Place.from_dict(obj_data)
                    elif data_type == "Review":
                        from Models.review import Review
                        obj = Review.from_dict(obj_data)
                    elif data_type == "City":
                        from Models.city import City
                        obj = City.from_dict(obj_data)
                    elif data_type == "Amenity":
                        from Models.amenity import Amenity
                        obj = Amenity.from_dict(obj_data)

                    storage[data_type][identifier] = obj_data
                    objects[identifier] = obj

            return storage, objects
    return {
        "User": {},
        "Place": {},
        "Review": {},
        "City": {},
        "Country": {},
        "Amenity": {}
        }, {}


def save_data(data):
    """Save data to data.json file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


class DataManager():
    """Class to manage all Data and CRUD methods"""
    storage, objects = load_data()

    @classmethod
    def save(cls, identifier, data_type, object):
        """Save Data to storage"""
        if data_type not in cls.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        cls.storage[data_type][identifier] = object.to_dict()
        cls.objects[identifier] = object
        save_data(cls.storage)

    @classmethod
    def get(cls, identifier, data_type):
        """Retrieve Data from storage with given identifier"""
        if data_type not in cls.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        return cls.objects[identifier]

    @classmethod
    def reload(cls, identifier, data_type):
        """Retrieve Data from storage with given identifier"""
        if data_type not in cls.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier not in cls.storage[data_type]:
            return None
        return cls.storage[data_type][identifier]

    @classmethod
    def update(cls, identifier, data_type, object):
        """Update data from storage"""
        if data_type not in cls.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier in cls.storage[data_type]:
            cls.storage[data_type][identifier] = object.to_dict()
            cls.objects[identifier] = object
        else:
            raise ValueError(f"{data_type} '{identifier}' does not exist")

    @classmethod
    def delete(cls, identifier, data_type):
        """Delete Data from storage with identifier"""
        if data_type not in cls.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        if identifier in cls.storage[data_type]:
            del cls.storage[data_type][identifier]
            save_data(cls.storage)
            del cls.objects[identifier]
        else:
            raise ValueError(f"{data_type} '{identifier}' does not exist")

    @classmethod
    def all(cls, data_type):
        """Retrieve all Data of given Data type"""
        if data_type not in cls.storage:
            raise ValueError(f"Unsupported data type: {data_type}")
        return list(cls.storage[data_type].values())
