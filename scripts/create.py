import sys
from db import get_db_connection, DiningHall, Meal, Record

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception(
            f"invalid number of arguments: expected 5, got {len(sys.argv)}")

    dining_hall = sys.argv[1]
    dining_hall = DiningHall.from_string(dining_hall)

    meal = sys.argv[2]
    meal = Meal.from_string(meal)

    keywords = sys.argv[3]
    keywords = keywords.split(",")

    recipient = sys.argv[4]

    record = Record.new(dining_hall, meal, keywords, recipient)

    data_store = get_db_connection()

    print(f"Creating a new record: {record.to_string()}")

    data_store.write_record(record)

    data_store.close()
