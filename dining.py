import datetime
import requests
from enum import Enum
from typing import List, Union
from bs4 import BeautifulSoup, Tag


DINING_API_BASE_URL = "https://dining.ncsu.edu/wp-admin/admin-ajax.php?action=ncdining_ajax_menu_results"


class Meal(Enum):
    DINNER = "dinner"
    LUNCH = "lunch"
    BREAKFAST = "breakfast"


def string_to_meal(name: str) -> Meal:
    if name == "dinner":
        return Meal.DINNER
    elif name == "lunch":
        return Meal.LUNCH
    elif name == "breakfast":
        return Meal.BREAKFAST
    else:
        raise Exception(f"invalid meal name: {name}")


# stores the id associated with each dining hall
class DiningHall(Enum):
    FOUNTAIN = 45


def string_to_dininghall(name: str) -> DiningHall:
    if name == "fountain":
        return DiningHall.FOUNTAIN
    else:
        raise Exception(f"invalid dining hall name: {name}")


class DiningHallData:

    @staticmethod
    def get_food(dining_hall: DiningHall, date: datetime.date, meal: Meal) -> List[str]:
        date_str = date.isoformat()

        url = f"{DINING_API_BASE_URL}&date={date_str}&meal={meal.value}&pid={dining_hall.value}"
        food_data = requests.get(url)

        parsed = BeautifulSoup(food_data.text, "html.parser")
        categories: List[Tag] = parsed.find_all(class_="dining-menu-category")

        all_dishes: list[str] = []

        for category in categories:
            dish_list = category.find("ul")
            if dish_list is None:
                raise Exception("no dishes list found")

            dish_names: List[str] = []

            dishes = dish_list.find_all("li")  # type: ignore
            for dish in dishes:  # type: ignore
                try:
                    dish_names.append(dish.find("a").text)  # type: ignore
                except:
                    raise Exception(
                        "unable to find and extract text from dishes")

            all_dishes.extend(dish_names)

        return all_dishes

    @staticmethod
    def find_dish_by_keyword(dish_names: List[str], keyword: str) -> Union[str, None]:
        keyword = keyword.lower()

        for dish in dish_names:
            dish = dish.lower()
            if keyword in dish:
                return dish

        return None
