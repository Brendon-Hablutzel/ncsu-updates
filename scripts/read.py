import sys
from db import get_db_connection

if __name__ == "__main__":
    data_store = get_db_connection()
    args = sys.argv

    if len(args) == 1:
        print("Fetching all records")
        records = data_store.get_records()
        for record in records:
            print(record)
        data_store.close()

    elif len(args) == 2:
        recipient = args[1]
        print(f"Fetching all records with recipient: {recipient}")
        records = data_store.get_records_by_recipient(recipient)
        for record in records:
            print(record)
        data_store.close()

    else:
        raise Exception(
            f"invalid number of arguments: expected 1 or 2 but got {len(args)}")
