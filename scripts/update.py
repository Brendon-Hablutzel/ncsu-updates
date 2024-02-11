import sys
from db import get_db_connection, DiningHall, Meal

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception(
            f"invalid number of argumets, expected 5, got {len(sys.argv)}")

    dining_hall = sys.argv[1]
    dining_hall = DiningHall.from_string(dining_hall)

    meal = sys.argv[2]
    meal = Meal.from_string(meal)

    keywords = sys.argv[3]
    keywords = keywords.split(",")

    recipient = sys.argv[4]

    data_store = get_db_connection()

    print("Updating record...")

    data_store.update_record(dining_hall, meal, keywords, recipient)

    data_store.close()

    print("Done")
