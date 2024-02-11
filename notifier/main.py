from typing import Iterable
from notify import NotificationSystem
from datastore import get_db_connection, Record, initialize_cache, Cache
import itertools


def notify_recipient(
    recipient: str,
    recipient_records: Iterable[Record],
    notifications: NotificationSystem,
    cache: Cache
):
    text = ""

    for record in recipient_records:
        for keyword in record.keywords:

            dishes = cache.get_dishes(record.dining_hall, record.meal, keyword)

            if len(dishes) > 0:
                keywords = [f"'{keyword}'" for keyword in record.keywords]
                plural = "es" if len(dishes) > 1 else ""
                text += f"{len(dishes)} dish{plural} at {record.dining_hall.to_string().capitalize()} for {record.meal.to_string()} matching {', '.join(keywords)}: {', '.join(dish[2] for dish in dishes)}\n\n"

    notifications.send_notification(recipient, "Food Update", text)


def main():
    notifications = NotificationSystem()

    data_store = get_db_connection()

    cache = initialize_cache()

    records = data_store.get_records()

    records = itertools.groupby(
        records, key=lambda record: record.recipient)

    for (recipient, recipient_records) in records:
        notify_recipient(recipient, recipient_records,
                         notifications, cache)


if __name__ == "__main__":
    main()
