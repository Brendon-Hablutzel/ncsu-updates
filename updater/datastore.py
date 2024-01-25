from mysql.connector import MySQLConnection
import os
from typing import NamedTuple, List, Any
from dining import DiningHall, Meal

SCHEMA_FILE = "schema.sql"


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
    def __init__(self):
        self.connection = MySQLConnection(
            user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_ROOT_PASSWORD"), host=os.getenv("DB_HOSTNAME"), database=os.getenv("MYSQL_DATABASE")
        )

        cursor = self.connection.cursor()

        with open(SCHEMA_FILE, "r") as f:
            schema = f.read()
            cursor.execute(schema)

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
        record_values: tuple[str] = (DiningHall.to_string(record.dining_hall), Meal.to_string(record.meal),
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
