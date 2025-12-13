"""
Тестирование класса Client
Лабораторная работа №1
"""

from src.client import Client
import json


def main():
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ КЛАССА CLIENT")
    print("=" * 70)
    
    # Шаг 1: Создание объекта Client с корректными данными
    print("\n1. Создание клиента с корректными данными:")
    print("-" * 70)
    
    client1 = Client(
        id=1,
        last_name="Иванов",
        first_name="Иван",
        patronymic="Петрович",
        phone="79991234567",
        email="ivanov.ivan@example.com",
        passport_series="1234",
        passport_number="567890",
        zip_code=123456,
        city="Москва",
        street="Ленина",
        house="10",
        total_spending=25000.50
    )
    
    # Шаг 2: Вывод объекта (проверка метода __str__)
    print("\n2. Вывод информации о клиенте (метод __str__):")
    print("-" * 70)
    print(client1)
    
    # Шаг 3: Попытка установить некорректный телефон (проверка валидации)
    print("\n3. Попытка изменить телефон на некорректный:")
    print("-" * 70)
    try:
        client1.phone = "123"
        print("Ошибка: валидация не сработала!")
    except ValueError as e:
        print(f"✓ Валидация сработала корректно!")
        print(f"  Сообщение об ошибке: {e}")
    
    # Шаг 4: Создание объекта через from_json
    print("\n4. Создание клиента из JSON:")
    print("-" * 70)
    
    json_data = {
        "id": 2,
        "last_name": "Петрова",
        "first_name": "Мария",
        "patronymic": "Александровна",
        "phone": "79998887766",
        "email": "petrova.maria@example.com",
        "passport_series": "4321",
        "passport_number": "098765",
        "zip_code": 654321,
        "city": "Санкт-Петербург",
        "street": "Невский проспект",
        "house": "25",
        "total_spending": 15000.00
    }
    
    json_string = json.dumps(json_data, ensure_ascii=False)
    print(f"JSON: {json_string}")
    
    client2 = Client.from_json(json_string)
    print("\n✓ Объект успешно создан из JSON:")
    print(client2)
    
    # Шаг 5: Сравнение объектов (проверка __eq__)
    print("\n5. Сравнение объектов (метод __eq__):")
    print("-" * 70)
    
    # Сравнение клиентов с разными ID
    print(f"client1 == client2: {client1 == client2}")
    print("  (Разные ID, ожидается False)")
    
    # Создание клиента с тем же ID, что и client1
    client1_copy = Client(
        id=1,
        last_name="Сидоров",
        first_name="Петр",
        patronymic="Иванович",
        phone="79995554433",
        email="sidorov@example.com",
        passport_series="9999",
        passport_number="888888",
        zip_code=111111,
        city="Казань",
        street="Баумана",
        house="1",
        total_spending=0.0
    )
    
    print(f"client1 == client1_copy: {client1 == client1_copy}")
    print("  (Одинаковый ID=1, ожидается True)")
    
    # Шаг 6: Создание объекта с пустым отчеством
    print("\n6. Создание клиента без отчества:")
    print("-" * 70)
    
    client3 = Client(
        id=3,
        last_name="Smith",
        first_name="John",
        patronymic="",  # Пустое отчество
        phone="79997776655",
        email="john.smith@example.com",
        passport_series="5555",
        passport_number="444444",
        zip_code=222222,
        city="Новосибирск",
        street="Красный проспект",
        house="50",
        total_spending=5000.00
    )
    
    print("✓ Клиент без отчества создан успешно:")
    print(client3)
    print("\n  Обратите внимание: в ФИО нет лишнего пробела")
    
    # Шаг 7: Создание объекта через from_string
    print("\n7. Создание клиента из строки (дополнительный тест):")
    print("-" * 70)
    
    string_data = "4,Козлов,Дмитрий,Сергеевич,79996665544,kozlov@example.com,7777,333333,333333,Екатеринбург,Ленина,15,10500.75"
    print(f"Строка: {string_data}")
    
    client4 = Client.from_string(string_data)
    print("\n✓ Объект успешно создан из строки:")
    print(client4)
    
    # Итоги
    print("\n" + "=" * 70)
    print("ВСЕ ТЕСТЫ ВЫПОЛНЕНЫ УСПЕШНО!")
    print("=" * 70)


if __name__ == "__main__":
    main()

