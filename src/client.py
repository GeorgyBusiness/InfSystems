import re
import json


class ClientBase:
    """
    Базовый класс для всех клиентских сущностей.
    
    Содержит общую функциональность: управление ID и статические методы валидации.
    """
    
    def __init__(self, id: int):
        """
        Инициализирует базовый объект с ID.
        
        Args:
            id: уникальный идентификатор клиента
        """
        self.id = id
    
    # Статические методы валидации
    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверка email с помощью регулярного выражения."""
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Проверка формата телефона 7XXXXXXXXXX (11 цифр, начинается с 7)."""
        if not isinstance(phone, str):
            return False
        pattern = r'^7\d{10}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def validate_name(name: str) -> bool:
        """Проверка что строка не пустая и состоит из букв (допускаются пробелы и дефисы)."""
        if not isinstance(name, str) or not name.strip():
            return False
        # Разрешаем буквы (включая кириллицу), пробелы и дефисы
        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$'
        return re.match(pattern, name) is not None

    # Геттеры и сеттеры для id
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int):
            raise ValueError(f"ID должен быть целым числом, получено: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"ID должен быть положительным числом, получено: {value}")
        self._id = value


class Client(ClientBase):
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
        # Вызываем конструктор родителя для инициализации id
        super().__init__(id)
        
        # Используем свойства (сеттеры) для автоматической валидации
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.phone = phone
        self.email = email
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.zip_code = zip_code
        self.city = city
        self.street = street
        self.house = house
        self.total_spending = total_spending

    def __repr__(self) -> str:
        """
        Возвращает строку, которая выглядит как вызов конструктора.
        
        Returns:
            str: представление объекта в виде "Client(id=1, last_name='Ivanov', ...)"
        """
        return (
            f"Client("
            f"id={self.id}, "
            f"last_name={self.last_name!r}, "
            f"first_name={self.first_name!r}, "
            f"patronymic={self.patronymic!r}, "
            f"phone={self.phone!r}, "
            f"email={self.email!r}, "
            f"passport_series={self.passport_series!r}, "
            f"passport_number={self.passport_number!r}, "
            f"zip_code={self.zip_code}, "
            f"city={self.city!r}, "
            f"street={self.street!r}, "
            f"house={self.house!r}, "
            f"total_spending={self.total_spending}"
            f")"
        )

    @classmethod
    def from_json(cls, json_str: str):
        """
        Создает объект Client из JSON строки.
        
        Args:
            json_str: JSON строка с данными клиента
            
        Returns:
            Client: новый объект клиента
        """
        data = json.loads(json_str)
        return cls(**data)

    @classmethod
    def from_string(cls, str_data: str, delimiter: str = ','):
        """
        Создает объект Client из строки с разделителем.
        
        Args:
            str_data: строка с данными в формате "id,last_name,first_name,..."
            delimiter: разделитель (по умолчанию запятая)
            
        Returns:
            Client: новый объект клиента
        """
        parts = str_data.split(delimiter)
        
        if len(parts) != 13:
            raise ValueError(f"Ожидается 13 полей, получено: {len(parts)}")
        
        # Приводим типы данных
        return cls(
            id=int(parts[0]),
            last_name=parts[1].strip(),
            first_name=parts[2].strip(),
            patronymic=parts[3].strip(),
            phone=parts[4].strip(),
            email=parts[5].strip(),
            passport_series=parts[6].strip(),
            passport_number=parts[7].strip(),
            zip_code=int(parts[8]),
            city=parts[9].strip(),
            street=parts[10].strip(),
            house=parts[11].strip(),
            total_spending=float(parts[12])
        )

    # Геттеры и сеттеры для last_name
    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not self.validate_name(value):
            raise ValueError(f"Фамилия должна быть непустой строкой из букв, получено: '{value}'")
        self._last_name = value

    # Геттеры и сеттеры для first_name
    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not self.validate_name(value):
            raise ValueError(f"Имя должно быть непустой строкой из букв, получено: '{value}'")
        self._first_name = value

    # Геттеры и сеттеры для patronymic
    @property
    def patronymic(self) -> str:
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value: str):
        # Отчество может быть пустой строкой (если у клиента его нет)
        if not isinstance(value, str):
            raise ValueError(f"Отчество должно быть строкой, получено: {type(value).__name__}")
        if value and not self.validate_name(value):
            raise ValueError(f"Отчество должно состоять из букв, получено: '{value}'")
        self._patronymic = value

    # Геттеры и сеттеры для phone
    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        if not self.validate_phone(value):
            raise ValueError(f"Телефон должен быть в формате 7XXXXXXXXXX, получено: '{value}'")
        self._phone = value

    # Геттеры и сеттеры для email
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not self.validate_email(value):
            raise ValueError(f"Неверный формат email, получено: '{value}'")
        self._email = value

    # Геттеры и сеттеры для passport_series
    @property
    def passport_series(self) -> str:
        return self._passport_series

    @passport_series.setter
    def passport_series(self, value: str):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 4:
            raise ValueError(f"Серия паспорта должна быть строкой из 4 цифр, получено: '{value}'")
        self._passport_series = value

    # Геттеры и сеттеры для passport_number
    @property
    def passport_number(self) -> str:
        return self._passport_number

    @passport_number.setter
    def passport_number(self, value: str):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 6:
            raise ValueError(f"Номер паспорта должен быть строкой из 6 цифр, получено: '{value}'")
        self._passport_number = value

    # Геттеры и сеттеры для zip_code
    @property
    def zip_code(self) -> int:
        return self._zip_code

    @zip_code.setter
    def zip_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError(f"Почтовый индекс должен быть целым числом, получено: {type(value).__name__}")
        if value < 100000 or value > 999999:
            raise ValueError(f"Почтовый индекс должен быть 6-значным числом, получено: {value}")
        self._zip_code = value

    # Геттеры и сеттеры для city
    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str):
        if not self.validate_name(value):
            raise ValueError(f"Город должен быть непустой строкой из букв, получено: '{value}'")
        self._city = value

    # Геттеры и сеттеры для street
    @property
    def street(self) -> str:
        return self._street

    @street.setter
    def street(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Улица должна быть непустой строкой, получено: '{value}'")
        self._street = value

    # Геттеры и сеттеры для house
    @property
    def house(self) -> str:
        return self._house

    @house.setter
    def house(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Номер дома должен быть непустой строкой, получено: '{value}'")
        self._house = value

    # Геттеры и сеттеры для total_spending
    @property
    def total_spending(self) -> float:
        return self._total_spending

    @total_spending.setter
    def total_spending(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Сумма трат должна быть числом, получено: {type(value).__name__}")
        if value < 0:
            raise ValueError(f"Сумма трат не может быть отрицательной, получено: {value}")
        self._total_spending = float(value)

    def __str__(self) -> str:
        """Возвращает строковое представление объекта Client."""
        # Формируем ФИО (без лишнего пробела, если отчество пустое)
        if self.patronymic:
            full_name = f"{self.last_name} {self.first_name} {self.patronymic}"
        else:
            full_name = f"{self.last_name} {self.first_name}"
        
        return (
            f"Client ID: {self.id}\n"
            f"ФИО: {full_name}\n"
            f"Телефон: {self.phone}\n"
            f"Email: {self.email}\n"
            f"Паспорт: {self.passport_series} {self.passport_number}\n"
            f"Адрес: {self.zip_code}, г. {self.city}, ул. {self.street}, д. {self.house}\n"
            f"Общая сумма покупок: {self.total_spending:.2f} руб."
        )

    def __eq__(self, other) -> bool:
        """Сравнивает два объекта Client на равенство."""
        if not isinstance(other, Client):
            return False
        
        # Если у обоих объектов есть валидный id, сравниваем по id
        if hasattr(self, '_id') and hasattr(other, '_id'):
            if self._id is not None and self._id > 0 and other._id is not None and other._id > 0:
                return self._id == other._id
        
        # Иначе сравниваем по email и phone (уникальные идентификаторы)
        return self.email == other.email and self.phone == other.phone


class ClientShort(ClientBase):
    """
    Краткая версия данных клиента для упрощенного представления.
    
    Содержит только основную информацию: ID, ФИО (сокращенно),
    один контакт и сумму трат.
    """
    
    def __init__(self, client: Client):
        """
        Создает краткую версию клиента.
        
        Args:
            client: объект типа Client
        """
        # Вызываем конструктор родителя для инициализации id
        super().__init__(client.id)
        
        self._total_spending = client.total_spending
        
        # Формируем полное имя в виде "Фамилия И.О." или "Фамилия И."
        if client.patronymic:
            # Если есть отчество: "Фамилия И.О."
            self._fullname = (
                f"{client.last_name} "
                f"{client.first_name[0]}."
                f"{client.patronymic[0]}."
            )
        else:
            # Если отчества нет: "Фамилия И."
            self._fullname = f"{client.last_name} {client.first_name[0]}."
        
        # Берем телефон, если его нет (что невозможно по валидации), берем email
        self._contact = client.phone if client.phone else client.email
    
    @property
    def fullname(self) -> str:
        """Возвращает полное имя в формате 'Фамилия И.О.' или 'Фамилия И.'"""
        return self._fullname
    
    @property
    def contact(self) -> str:
        """Возвращает основной контакт (телефон или email)."""
        return self._contact
    
    @property
    def total_spending(self) -> float:
        """Возвращает общую сумму трат клиента."""
        return self._total_spending
    
    def __str__(self) -> str:
        """Возвращает краткое строковое представление объекта ClientShort."""
        return (
            f"ShortClient: {self.fullname}, "
            f"Связь: {self.contact}, "
            f"Баланс: {self.total_spending}"
        )
