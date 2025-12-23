from src.models.client import Client
from src.repositories.client_rep_db import Client_rep_db
from src.core.db_manager import DB_manager


def test_database():
    # 1. Твои параметры подключения (замени на свои)
    db_params = {
        "host": "localhost",
        "user": "postgres",
        "password": "Cill020Cash!",  # <--- ВСТАВЬ ПАРОЛЬ ТУТ
        "dbname": "internet_shop",
        "port": "5432"
    }

    try:
        # 2. Создаем Singleton DB_manager
        db_manager = DB_manager(db_params)
        print("✅ Подключение к базе успешно!")
        
        # 3. Инициализируем репозиторий с DB_manager
        repo = Client_rep_db(db_manager)

        # 4. Создаем тестового клиента (ID ставим любой, база его заменит)
        new_client = Client(
            id=1,
            last_name="Тестовый",
            first_name="Георгий",
            patronymic="Программистович",
            phone="79998887766",
            email="georgiy_test@mail.ru",
            passport_series="1234",
            passport_number="567890",
            zip_code=123456,
            city="Москва",
            street="Пушкина",
            house="10",
            total_spending=500.50
        )

        # 5. Проверяем добавление (Add)
        print("\n--- Добавление клиента ---")
        repo.add(new_client)
        print(f"Клиент добавлен! База присвоила ему ID: {new_client.id}")

        # 6. Проверяем получение по ID (Get by ID)
        print("\n--- Получение клиента по ID ---")
        fetched_client = repo.get_by_id(new_client.id)
        if fetched_client:
            print(f"Найден клиент: {fetched_client.last_name} {fetched_client.first_name}")
        else:
            print("❌ Ошибка: клиент не найден после добавления")

        # 7. Проверяем количество (Get Count)
        count = repo.get_count()
        print(f"\nВсего клиентов в базе: {count}")

        # 8. Проверяем краткий список (Get k, n short list)
        print("\n--- Проверка пагинации (краткий список) ---")
        short_list = repo.get_k_n_short_list(k=1, n=5)
        for short in short_list:
            print(f"- {short}")

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    test_database()
