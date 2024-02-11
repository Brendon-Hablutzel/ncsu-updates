from mysql.connector import MySQLConnection
from typing import NamedTuple, List, Any, Tuple
from dining import DiningHall, Meal, DiningHallData
from get_vars import get_database_host, get_database_name, get_database_password, get_database_user
import datetime


class Record(NamedTuple):
    dining_hall: DiningHall
    meal: Meal
    keywords: List[str]
    recipient: str

    @staticmethod
    def from_mysql_row(row: Any) -> 'Record':
        return Record(
            DiningHall.from_string(row[0]),
            Meal.from_string(row[1]),
            row[2].split(","),
            row[3]
        )


class DataStore:
    def __init__(self, user: str, password: str, host: str, database: str):
        self.connection = MySQLConnection(
            user=user, password=password, host=host, database=database
        )

        cursor = self.connection.cursor()

        self.connection.commit()
        cursor.close()

    def close(self):
        self.connection.close()

    def get_records(self) -> List[Record]:
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM records")
        results = cursor.fetchall()

        cursor.close()
        return [Record.from_mysql_row(row) for row in results]

    def write_record(self, record: Record):
        cursor = self.connection.cursor()

        add_record = (
            "INSERT INTO records (dining_hall, meal, keywords, recipient) VALUES (%s, %s, %s, %s)")
        record_values: tuple[str, str, str, str] = (DiningHall.to_string(record.dining_hall), Meal.to_string(record.meal),
                                                    ','.join(record.keywords), record.recipient)

        cursor.execute(add_record, record_values)
        self.connection.commit()
        cursor.close()

    def delete_records(self, recipient: str):
        cursor = self.connection.cursor()

        delete_records = ("DELETE FROM records WHERE recipient = %s")
        data = tuple(recipient)

        cursor.execute(delete_records, data)
        self.connection.commit()
        cursor.close()


def get_db_connection() -> DataStore:
    return DataStore(
        get_database_user(),
        get_database_password(),
        get_database_host(),
        get_database_name()
    )


class Cache:
    def __init__(self):
        self.dishes: list[tuple[DiningHall, Meal, str]] = []
        self.stored: list[tuple[DiningHall, Meal]] = []
        self.current_date = datetime.date.today()

    def load_data(self, dining_hall: DiningHall, meal: Meal):
        if (dining_hall, meal) not in self.stored:
            dishes = DiningHallData.get_food(
                dining_hall, self.current_date, meal)
            for dish in dishes:
                self.dishes.append((dining_hall, meal, dish))
            self.stored.append((dining_hall, meal))

    def has_data(self, dining_hall: DiningHall, meal: Meal) -> bool:
        return (dining_hall, meal) in self.stored

    def get_dishes(self, dining_hall: DiningHall, meal: Meal, keyword: str) -> List[Tuple[DiningHall, Meal, str]]:
        if self.has_data(dining_hall, meal):
            return [
                dish for dish in self.dishes if dish[0] == dining_hall and dish[1] == meal and keyword in dish[2].lower()
            ]
        else:
            self.load_data(dining_hall, meal)
            return self.get_dishes(dining_hall, meal, keyword)


def initialize_cache() -> Cache:
    return Cache()
