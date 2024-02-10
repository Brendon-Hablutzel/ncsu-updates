import os


def get_database_name():
    return get_var("MYSQL_DATABASE")


def get_database_host():
    return get_var("MYSQL_HOST")


def get_database_user():
    return get_var("MYSQL_USER")


def get_database_password():
    return get_var("MYSQL_PASSWORD")


def get_var(name: str) -> str:
    var = os.getenv(name)
    if var is None:
        raise Exception(f"environment variable {name} not set")
    else:
        return var
