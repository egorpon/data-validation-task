import os
import pathlib
import json
import unittest
from datetime import date

from solution import Address, User, load_records


class RecordLoaderTests(unittest.TestCase):
    def setUp(self):
        data = [
            {
                "id": 1,
                "email": "valerabig4len@ukr.net",
                "full_name": "Valera Zmyshenko",
                "gender": "male",
                "date_of_birth": "1975-08-15",
                "addresses": [
                    {
                        "country": "Ukraine",
                        "city": "Kyiv",
                        "postal_code": "01001",
                    },
                    {
                        "country": "Ukraine",
                        "city": "Zhytomyr",
                        "postal_code": "01488",
                    },
                ],
            }
        ]
        self.data_path = pathlib.Path(".test_data.json")
        self._remove_test_files()

        with open(self.data_path, "w") as f:
            f.write(json.dumps(data))

    def tearDown(self):
        self._remove_test_files()

    def _remove_test_files(self):
        try:
            os.remove(self.data_path)
        except Exception:
            # File does not exists
            pass

    def test_data_is_loaded(self):
        data = load_records(str(self.data_path))
        self.assertEqual(len(data), 1)
        record = data[0]
        self.assertIsInstance(record, User)
        self.assertEqual(len(record.addresses), 2)
        for address in record.addresses:
            self.assertIsInstance(address, Address)


class AddressValidatorsTests(unittest.TestCase):
    def test_constructor_works(self):
        data = {
            "country": "Ukraine",
            "city": "Kyiv",
            "postal_code": "10101",
        }
        address = Address(data)
        self.assertEqual(address.country, data["country"])
        self.assertEqual(address.city, data["city"])
        self.assertEqual(address.postal_code, data["postal_code"])

    def test_constructor_works_with_invalid_fields(self):
        data = {
            "country": "ukraine",
            "city": "kyiv",
            "postal_code": "abc",
        }
        address = Address(data)
        self.assertEqual(address.country, data["country"])
        self.assertEqual(address.city, data["city"])
        self.assertEqual(address.postal_code, data["postal_code"])

    def test_valid_address(self):
        data = {
            "country": "Ukraine",
            "city": "Kyiv",
            "postal_code": "10101",
        }
        address = Address(data)
        self.assertTrue(address.is_valid())
        self.assertEqual(len(address.get_invalid_fields()), 0)

    def test_invalid_address(self):
        data = {
            "country": "ukraine",
            "city": "kyiv",
            "postal_code": "abc",
        }
        address = Address(data)
        self.assertFalse(address.is_valid())
        invalid_fields = address.get_invalid_fields()
        for field_name in data.keys():
            self.assertIn(field_name, invalid_fields)

    def test_invalid_city(self):
        data = {
            "country": "Ukraine",
            "city": "kyiv",
            "postal_code": "11111",
        }
        address = Address(data)
        self.assertFalse(address.is_valid())
        self.assertIn("city", address.get_invalid_fields())

    def test_postal_code(self):
        invalid_values = [
            "-3434",
            "234234",
            "abcosdf",
        ]
        for value in invalid_values:
            data = {
                "country": "Ukraine",
                "city": "Kyiv",
                "postal_code": value,
            }
            address = Address(data)
            self.assertFalse(address.is_valid())
            self.assertIn("postal_code", address.get_invalid_fields())


class UserValidatorsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_user = {
            "id": 1,
            "email": "valerabig4len@ukr.net",
            "full_name": "Valera Zmyshenko",
            "gender": "male",
            "date_of_birth": "1975-08-15",
            "addresses": [
                {
                    "country": "Ukraine",
                    "city": "Kyiv",
                    "postal_code": "01001",
                },
                {
                    "country": "Ukraine",
                    "city": "Zhytomyr",
                    "postal_code": "01488",
                },
            ],
        }

    def test_constructor_works(self):
        user = User(self.base_user)
        self.assertEqual(user.email, self.base_user["email"])
        self.assertEqual(user.full_name, self.base_user["full_name"])
        self.assertEqual(user.gender, self.base_user["gender"])
        self.assertEqual(
            user.date_of_birth.isoformat(), self.base_user["date_of_birth"]
        )
        self.assertEqual(len(user.addresses), 2)

    def test_valid_user(self):
        user = User(self.base_user)
        self.assertTrue(user.is_valid())
        self.assertEqual(len(user.get_invalid_fields()), 0)

    def test_invalid_email(self):
        invalid_values = [
            "helloworld",
            "@.hello",
            "ab@.hlo",
            "absc@x.com",
            "abs c@x.com",
        ]
        for email in invalid_values:
            self.base_user["email"] = email
            user = User(self.base_user)
            self.assertFalse(user.is_valid())
            self.assertIn("email", user.get_invalid_fields())

    def test_invalid_full_name(self):
        invalid_values = [
            "James  Clear",
            "James",
            "James-Clear",
            "James Not Clear",
        ]
        for value in invalid_values:
            self.base_user["full_name"] = value
            user = User(self.base_user)
            self.assertFalse(user.is_valid())
            self.assertIn("full_name", user.get_invalid_fields())

    def test_invalid_gender(self):
        invalid_values = [
            "FEMALE",
            "pansexual",
            "MALE",
        ]
        for value in invalid_values:
            self.base_user["gender"] = value
            user = User(self.base_user)
            self.assertFalse(user.is_valid())
            self.assertIn("gender", user.get_invalid_fields())

    def test_invalid_date_of_birth(self):
        self.base_user["date_of_birth"] = "2030-10-15"
        user = User(self.base_user)
        self.assertFalse(user.is_valid())
        self.assertIn("date_of_birth", user.get_invalid_fields())

    def test_invalid_address(self):
        self.base_user["addresses"][0]["city"] = "lower"
        user = User(self.base_user)
        self.assertFalse(user.is_valid())
        self.assertIn("addresses", user.get_invalid_fields())

    def test_no_addresses(self):
        self.base_user["addresses"] = []
        user = User(self.base_user)
        self.assertTrue(user.is_valid())
        self.assertEqual(len(user.get_invalid_fields()), 0)


if __name__ == "__main__":
    unittest.main()
