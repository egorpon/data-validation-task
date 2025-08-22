import json
from abc import ABC, abstractmethod
from datetime import date
import re
from  datetime import datetime


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

    def __init__(self, data: dict) -> None: 
        self.country = data.get('country','')
        self.city = data.get('city','')
        self.postal_code = data.get('postal_code','')

    def __repr__(self) -> str: 
        return f"{self.country}, {self.city}, {self.postal_code}"

    def is_valid(self) -> bool: 
        return all([self.is_city_valid(), self.is_country_valid(), self.is_postal_code_valid()])

    def get_invalid_fields(self) -> list[str]: 
        invalid_fields = {
            "city":self.is_city_valid(),
            "country":self.is_country_valid(),
            "postal_code":self.is_postal_code_valid()}
        
        return [field for field, value in invalid_fields.items() if not value]

    def is_country_valid(self) -> bool: 
        return bool(re.fullmatch(r'^[A-Z][a-z]+$',self.country))
        

    def is_city_valid(self) -> bool:
        return bool(re.fullmatch(r'^[A-Z][a-z]+$',self.city))
            

    def is_postal_code_valid(self) -> bool: 
        return bool(re.fullmatch(r'^\d{5}$',self.postal_code))



class User(Validationable):
    id: int
    email: str
    full_name: str
    gender: str
    date_of_birth: date
    addresses: list[Address]

    def __init__(self, data: dict) -> None: 
        self.email = data.get('email','')
        self.full_name = data.get('full_name','')
        self.gender = data.get('gender','')
        self.addresses = [Address(addr) for addr in data.get('addresses',[])]
        dob_str = data.get('date_of_birth','')
        if dob_str:
            self.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        else:
            self.date_of_birth = None

    def __repr__(self) -> str: 
        return (f"Email: {self.email}\n"
                f"Full name: {self.full_name}\n" 
                f"Gender: {self.gender}\n"
                f"Date of birth: {self.date_of_birth}\n"
                f"Addresses:\n     {'\n     '.join(str(addr) for addr in self.addresses)}")
    
    def is_valid(self) -> bool: 
        return all([self.is_email_valid(),self.is_full_name_valid(), self.is_gender_valid(), self.is_date_of_birth_valid(), self.is_addresses_valid()])

    def get_invalid_fields(self) -> list[str]: 
        invalid_fields = {
            "email" : self.is_email_valid(),
            "full_name": self.is_full_name_valid(),
            "gender" : self.is_gender_valid(),
            "date_of_birth": self.is_date_of_birth_valid(),
            "addresses": self.is_addresses_valid()

        }
        return [field for field, value in invalid_fields.items() if not value]


    def is_email_valid(self) -> bool: 
        return bool(re.fullmatch(r'^\w{2,}@[a-zA-z]{2,}\.[a-zA-z]{2,}$',self.email))
       


    def is_full_name_valid(self) -> bool: 
        return bool(re.fullmatch(r'^[a-zA-z]+\s{1}+[a-zA-z]+$',self.full_name))
            


    def is_gender_valid(self) -> bool: 
        return self.gender in ['male', 'female']



    def is_date_of_birth_valid(self) -> bool:
        return self.date_of_birth is not None and self.date_of_birth < datetime.now().date()
            


    def is_addresses_valid(self) -> bool: 
        return all([address.is_valid() for address in self.addresses])


def load_records(filename: str) -> list[User]:
    with open(filename) as f:
        data = json.load(f)
        return [User(user) for user in data]
    
