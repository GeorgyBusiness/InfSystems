from src.client import Client
from src.client_rep_db import Client_rep_db
from src.client_rep_db_decorator import Client_rep_db_decorator
from src.db_manager import DB_manager


def test_decorator():
    """
    Демонстрирует использование паттерна Декоратор для фильтрации и сортировки.
    """
    
    # 1. Параметры подключения
    db_params = {
        "host": "localhost",
        "user": "postgres",
        "password": "Cill020Cash!",
        "dbname": "internet_shop",
        "port": "5432"
    }

    try:
        # 2. Создаем Singleton DB_manager
        db_manager = DB_manager(db_params)
        print("✅ Подключение к базе успешно!\n")
        
        # 3. Создаем репозиторий
        repo = Client_rep_db(db_manager)
        
        # 4. Оборачиваем репозиторий в декоратор
        decorated_repo = Client_rep_db_decorator(repo)
        
        # ============= ПРИМЕР 1: Фильтрация по городу =============
        print("--- ПРИМЕР 1: Получить клиентов из города 'Москва' (стр. 1, по 5 на стр.) ---")
        decorated_repo.set_filter('city', 'Москва')
        moscow_clients = decorated_repo.get_k_n_short_list(k=1, n=5)
        print(f"Найдено {len(moscow_clients)} клиентов из Москвы на первой странице:")
        for client in moscow_clients:
            print(f"  - {client}")
        print()
        
        # ============= ПРИМЕР 2: Фильтрация + Сортировка =============
        print("--- ПРИМЕР 2: Клиенты из 'Москвы', отсортированные по фамилии ---")
        decorated_repo.clear_filters()
        decorated_repo.set_filter('city', 'Москва')
        decorated_repo.set_sort('last_name', 'ASC')
        sorted_moscow_clients = decorated_repo.get_k_n_short_list(k=1, n=10)
        print(f"Найдено {len(sorted_moscow_clients)} клиентов (отсортировано по фамилии):")
        for client in sorted_moscow_clients:
            print(f"  - {client}")
        print()
        
        # ============= ПРИМЕР 3: Количество отфильтрованных =============
        print("--- ПРИМЕР 3: Общее количество клиентов из 'Москвы' ---")
        count = decorated_repo.get_count()
        print(f"Всего клиентов из Москвы: {count}\n")
        
        # ============= ПРИМЕР 4: Сбросить фильтры =============
        print("--- ПРИМЕР 4: После сброса фильтров (все клиенты) ---")
        decorated_repo.clear_filters()
        decorated_repo.clear_sort()
        all_clients = decorated_repo.get_k_n_short_list(k=1, n=5)
        total_count = decorated_repo.get_count()
        print(f"Первые 5 клиентов из всех {total_count}:")
        for client in all_clients:
            print(f"  - {client}")
        print()
        
        # ============= ПРИМЕР 5: Chain-вызовы =============
        print("--- ПРИМЕР 5: Chain-вызовы (фильтр + сортировка за раз) ---")
        chain_clients = (decorated_repo
                        .set_filter('city', 'Москва')
                        .set_sort('total_spending', 'DESC')
                        .get_k_n_short_list(k=1, n=5))
        print(f"Клиенты из Москвы, отсортированные по тратам (DESC):")
        for client in chain_clients:
            print(f"  - {client}")
        print()
        
        # ============= ПРИМЕР 6: Обычные методы работают =============
        print("--- ПРИМЕР 6: Обычные методы репозитория работают через декоратор ---")
        client_by_id = decorated_repo.get_by_id(1)
        if client_by_id:
            print(f"Клиент с ID 1: {client_by_id.last_name} {client_by_id.first_name}")
        else:
            print("Клиент с ID 1 не найден")
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    test_decorator()

