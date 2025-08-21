from solution import load_records


def main():
    records = load_records("data.json")
    print(f"loaded {len(records)} records")

    for user in records:
        print(f"\nuser: {user}")
        is_valid = user.is_valid()
        print("all fields valid?:", is_valid)
        if not is_valid:
            print("invalid fields:", user.get_invalid_fields())
        else:
            print(f"data for user {user.email} is valid")


if __name__ == "__main__":
    main()
