from enum import Enum


class Meal(Enum):
    DINNER = "dinner"
    LUNCH = "lunch"
    BREAKFAST = "breakfast"

    @staticmethod
    def from_string(name: str) -> 'Meal':
        if name == "dinner":
            return Meal.DINNER
        elif name == "lunch":
            return Meal.LUNCH
        elif name == "breakfast":
            return Meal.BREAKFAST
        else:
            raise Exception(f"invalid meal name: {name}")

    def to_string(self) -> str:
        return self.value


# stores the id associated with each dining hall
class DiningHall(Enum):
    FOUNTAIN = 45

    @staticmethod
    def from_string(name: str) -> 'DiningHall':
        if name == "fountain":
            return DiningHall.FOUNTAIN
        else:
            raise Exception(f"invalid dining hall name: {name}")

    def to_string(self) -> str:
        if self == DiningHall.FOUNTAIN:
            return "fountain"
        else:
            raise Exception(f"invalid dining hall state")
