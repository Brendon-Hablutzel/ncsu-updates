import sys
from db import get_db_connection

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception(
            f"invalid number of arguments, expected 2, got {len(sys.argv)}")

    recipient = sys.argv[1]

    data_store = get_db_connection()

    print(f"Deleting all records with recipient: {recipient}")

    data_store.delete_records(recipient)

    data_store.close()

    print("Done")
