# Welcome to test task for Senior Python Developer Position at "The Startup (TM)"
## About this project
You have data from database, stored in `data.json` file in root directory.
You were tasked to validate data according to new company rules.


## Tasks
1. Load data from `data.json` file to our program
2. Implement `is_valid` and `get_invalid_fields` methods for `User` and `Address`

## Challenge Rules

- Follow type annotations, if return type is `list[str]` you MUST return list with strings
- You need to modify **ONLY** `solution.py` file
- You can implement any additional methods/functions/classes if you want
- You can add `print` statements in any part of code outside of `solution.py` for debug purposes
- You can modify `data.json` file to test possible cases of invalid data


## How to test your solution
run test cases with
```sh
python test.py
```
output should be OK at the end


Run `main.py` to see how your solution will be used
```sh
python main.py
```


## Validation rules

### User
#### email
- must contain `@`
- must contain `.`
- words should be at least 2 characters long. Minimum valid email: `ab@cd.ef`
- no `" "` (spaces) allowed

#### full_name
- must be 2 words only, separated by space

#### gender
- either `male` or `female`

#### date_of_birth
- any date in the past

#### addressss
- all addresses must be valid

### Address


#### country
- must start with capital letter

#### city
- must start with capital letter

#### postal_code
- must have len of 5 characters
- only digits are allowed
