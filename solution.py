import json
from abc import ABC, abstractmethod
from datetime import date
import re

class Validationable(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        """
        Return `True` if all fields valid
        """

    @abstractmethod
    def get_invalid_fields(self) -> list[str]:
        """
        Return list with invalid field names,
        empty list if all fields valid
        """


class Address(Validationable):
    country: str
    city: str
    postal_code: str

    def __init__(self, data: dict) -> None: ...

    def is_valid(self) -> bool: ...

    def get_invalid_fields(self) -> list[str]: ...

    def is_country_valid(self) -> bool: ...

    def is_city_valid(self) -> bool: ...

    def is_postal_code_valid(self) -> bool: ...


class User(Validationable):
    id: int
    email: str
    full_name: str
    gender: str
    date_of_birth: date
    addresses: list[Address]

    def __init__(self, data: dict) -> None: 
        self.email = data.get('email')
        self.full_name = data.get('full_name')
        self.gender = data.get('gender')
        self.date_of_birth = data.get('date_of_birth')
        self.addresses = data.get("addresses")

    def __str__(self) -> str: 
        return f"email: {self.email} full name: {self.full_name} gender: {self.gender} date of birth: {self.date_of_birth} addresses: {self.addresses}"
    
    def is_valid(self) -> bool: ...

    def get_invalid_fields(self) -> list[str]: ...

#     ### User
# #### email
# - must contain `@`
# - must contain `.`
# - words should be at least 2 characters long. Minimum valid email: `ab@cd.ef`
# - no `" "` (spaces) allowed

    def is_email_valid(self) -> bool: 
        if re.fullmatch(r'^\w{2,}+@[a=zA-z]{2,}+\.[a-zA-z]{2,}+$',self.email):
            return True
        return False

    def is_full_name_valid(self) -> bool: ...

    def is_gender_valid(self) -> bool: ...

    def is_date_of_birth_valid(self) -> bool: ...

    def is_addresses_valid(self) -> bool: ...


def load_records(filename: str) -> list[User]:
    with open(filename) as f:
        data = json.load(f)
        return data[0]
    
user = User(load_records('data.json'))
print(user)
user.is_email_valid()