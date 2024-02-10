import datetime
from typing import List
from dining import DiningHallData, DiningHall, Meal
from notify import NotificationSystem
from datastore import get_db_connection
import logging


def notify(dining_hall: DiningHall, date: datetime.date, meal: Meal, keywords: List[str], recipient: str):
    logging.info(
        f"Searching for {keywords} at {dining_hall} on {date} for {meal}; results, if any, will be sent to {recipient}")

    dishes = DiningHallData.get_food(
        dining_hall, date, meal)

    dishes = DiningHallData.find_dishes_by_keywords(dishes, keywords)

    notifications = NotificationSystem()

    try:
        if len(dishes) > 0:
            logging.info(f"Sending: {dishes} to {recipient}")

            notifications.send_notification(
                recipient, "Food update", f"Requested dishes were found: {', '.join(dishes)}")
    except Exception as e:
        raise Exception(f"Error sending notification: {e}")
    finally:
        notifications.close()


def main():
    current_date = datetime.date.today()

    data_store = get_db_connection()

    records = data_store.get_records()

    data_store.close()

    for record in records:
        notify(record.dining_hall, current_date, record.meal,
               record.keywords, record.recipient)


if __name__ == "__main__":
    main()
