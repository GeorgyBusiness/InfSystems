class Client:
    def __init__(
        self,
        id: int,
        last_name: str,
        first_name: str,
        patronymic: str,
        phone: str,
        email: str,
        passport_series: str,
        passport_number: str,
        zip_code: int,
        city: str,
        street: str,
        house: str,
        total_spending: float
    ):
        self._id = id
        self._last_name = last_name
        self._first_name = first_name
        self._patronymic = patronymic
        self._phone = phone
        self._email = email
        self._passport_series = passport_series
        self._passport_number = passport_number
        self._zip_code = zip_code
        self._city = city
        self._street = street
        self._house = house
        self._total_spending = total_spending

    # Геттеры и сеттеры для id
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    # Геттеры и сеттеры для last_name
    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        self._last_name = value

    # Геттеры и сеттеры для first_name
    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._first_name = value

    # Геттеры и сеттеры для patronymic
    @property
    def patronymic(self) -> str:
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value: str):
        self._patronymic = value

    # Геттеры и сеттеры для phone
    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value

    # Геттеры и сеттеры для email
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    # Геттеры и сеттеры для passport_series
    @property
    def passport_series(self) -> str:
        return self._passport_series

    @passport_series.setter
    def passport_series(self, value: str):
        self._passport_series = value

    # Геттеры и сеттеры для passport_number
    @property
    def passport_number(self) -> str:
        return self._passport_number

    @passport_number.setter
    def passport_number(self, value: str):
        self._passport_number = value

    # Геттеры и сеттеры для zip_code
    @property
    def zip_code(self) -> int:
        return self._zip_code

    @zip_code.setter
    def zip_code(self, value: int):
        self._zip_code = value

    # Геттеры и сеттеры для city
    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str):
        self._city = value

    # Геттеры и сеттеры для street
    @property
    def street(self) -> str:
        return self._street

    @street.setter
    def street(self, value: str):
        self._street = value

    # Геттеры и сеттеры для house
    @property
    def house(self) -> str:
        return self._house

    @house.setter
    def house(self, value: str):
        self._house = value

    # Геттеры и сеттеры для total_spending
    @property
    def total_spending(self) -> float:
        return self._total_spending

    @total_spending.setter
    def total_spending(self, value: float):
        self._total_spending = value

