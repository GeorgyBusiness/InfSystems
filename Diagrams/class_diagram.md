# Диаграмма классов (ЛР1)

```mermaid
classDiagram
    note "Иерархия классов сущности Client"

    %% --- Базовый класс ---
    class ClientBase {
        #int _id
        +int id
        +validate_email(email: str) bool$
        +validate_phone(phone: str) bool$
        +validate_name(name: str) bool$
    }

    %% --- Полная версия (Full) ---
    class Client {
        #str _last_name
        #str _first_name
        #str _patronymic
        #str _phone
        #str _email
        #str _passport_series
        #str _passport_number
        #int _zip_code
        #str _city
        #str _street
        #str _house
        #float _total_spending
        
        %% Фабричные методы и магия
        +from_json(json_str: str) Client$
        +from_string(str_data: str) Client$
        +__str__() str
        +__repr__() str
        +__eq__(other: object) bool
    }

    %% --- Краткая версия (Short/DTO) ---
    class ClientShort {
        #str _fullname
        #str _contact
        #float _total_spending
        
        %% Свойства только для чтения
        +str fullname
        +str contact
        +float total_spending
        
        +__init__(client: Client)
        +__str__() str
    }

    %% --- Связи ---
    %% Наследование (Inheritance)
    ClientBase <|-- Client
    ClientBase <|-- ClientShort

    %% Зависимость (Dependency) - ClientShort создается из Client
    ClientShort ..> Client : uses in __init__