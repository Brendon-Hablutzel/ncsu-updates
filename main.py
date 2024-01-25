import datetime
import sys
from typing import List
from dining import DiningHallData, DiningHall, Meal, string_to_dininghall, string_to_meal
from notify import NotificationSystem


def main(dining_hall: DiningHall, date: datetime.date, meal: Meal, keyword: str, recipients: List[str]):
    print(f"Searching for {keyword} at {dining_hall} on {date} for {meal}")
    print(f"Results, if any, will be sent to {recipients}")

    dishes = DiningHallData.get_food(
        dining_hall, date, meal)

    dish = DiningHallData.find_dish_by_keyword(dishes, keyword)

    notifications = NotificationSystem()

    if dish is not None:
        notifications.send_notification(
            recipients, "Food update", f"A requested dish was found: {dish}")


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 6:
        raise Exception(
            f"incorrect number of arguments passed, expected 6, got {len(args)}: {args}")

    dining_hall = args[1]
    dining_hall = string_to_dininghall(dining_hall)

    date = args[2]
    date = datetime.date.fromisoformat(date)

    meal = args[3]
    meal = string_to_meal(meal)

    keyword = args[4]

    recipients = args[5]
    recipients = recipients.split(",")

    main(dining_hall, date, meal, keyword, recipients)
