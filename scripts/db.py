from mysql.connector import MySQLConnection
from typing import NamedTuple, List, Any
from get_vars import get_database_password, get_database_host, get_database_name, get_database_user
from dining import DiningHall, Meal


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

    @staticmethod
    def new(dining_hall: DiningHall, meal: Meal, keywords: List[str], recipient: str) -> 'Record':
        return Record(
            dining_hall,
            meal,
            keywords,
            recipient
        )

    def to_string(self) -> str:
        return f"{self.dining_hall.to_string()}, {self.meal.to_string()}, {' '.join(self.keywords)}, {self.recipient}"


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

    def get_records_by_recipient(self, recipient: str) -> List[Record]:
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM records WHERE recipient = %s", (recipient, ))
        results = cursor.fetchall()

        cursor.close()
        return [Record.from_mysql_row(row) for row in results]

    def write_record(self, record: Record):
        cursor = self.connection.cursor()

        add_record = (
            "INSERT INTO records (dining_hall, meal, keywords, recipient) VALUES (%s, %s, %s, %s)")
        record_values = (DiningHall.to_string(record.dining_hall), Meal.to_string(record.meal),
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
