import os
from src.client import Client
from src.client_rep_json import Client_rep_json
from src.client_rep_yaml import Client_rep_yaml
from src.client_rep_file_decorator import Client_rep_file_decorator


def test_json_decorator():
    """Демонстрирует использование декоратора с JSON репозиторием."""
    
    print("=" * 60)
    print("ТЕСТ ДЕКОРАТОРА С JSON РЕПОЗИТОРИЕМ")
    print("=" * 60)
    
    json_file = "test_clients.json"
    
    try:
        # 1. Создаем репозиторий JSON
        json_repo = Client_rep_json(json_file)
        print(f"✅ Загружено {json_repo.get_count()} клиентов из JSON")
        
        # 2. Оборачиваем в декоратор
        decorated_repo = Client_rep_file_decorator(json_repo)
        
        # ============= ПРИМЕР 1: Фильтрация по городу =============
        print("\n--- ПРИМЕР 1: Клиенты из города 'Москва' (стр. 1, по 3 на стр.) ---")
        decorated_repo.set_filter('city', 'Москва')
        moscow_clients = decorated_repo.get_k_n_short_list(k=1, n=3)
        print(f"Найдено {len(moscow_clients)} клиентов из Москвы:")
        for client in moscow_clients:
            print(f"  - {client}")
        
        # ============= ПРИМЕР 2: Фильтрация + Сортировка =============
        print("\n--- ПРИМЕР 2: Клиенты из 'Москвы', отсортированные по фамилии (ASC) ---")
        decorated_repo.set_sort('last_name', reverse=False)
        sorted_moscow = decorated_repo.get_k_n_short_list(k=1, n=10)
        print(f"Найдено {len(sorted_moscow)} клиентов (отсортировано):")
        for client in sorted_moscow:
            print(f"  - {client}")
        
        # ============= ПРИМЕР 3: Количество отфильтрованных =============
        print("\n--- ПРИМЕР 3: Общее количество клиентов из 'Москвы' ---")
        count = decorated_repo.get_count()
        print(f"Всего отфильтрованных: {count}")
        
        # ============= ПРИМЕР 4: Сбросить фильтры =============
        print("\n--- ПРИМЕР 4: После сброса фильтров (все клиенты) ---")
        decorated_repo.clear_filters()
        decorated_repo.clear_sort()
        all_clients = decorated_repo.get_k_n_short_list(k=1, n=5)
        total_count = decorated_repo.get_count()
        print(f"Первые 5 из всех {total_count}:")
        for client in all_clients:
            print(f"  - {client}")
        
        # ============= ПРИМЕР 5: Сортировка по тратам (DESC) =============
        print("\n--- ПРИМЕР 5: Сортировка по сумме трат (DESC) ---")
        decorated_repo.set_sort('total_spending', reverse=True)
        rich_clients = decorated_repo.get_k_n_short_list(k=1, n=5)
        print(f"Клиенты с наибольшей суммой трат:")
        for client in rich_clients:
            print(f"  - {client}")
        
        # ============= ПРИМЕР 6: Chain-вызовы =============
        print("\n--- ПРИМЕР 6: Chain-вызовы (фильтр + сортировка за раз) ---")
        chain_clients = (decorated_repo
                        .clear_filters()
                        .clear_sort()
                        .set_filter('city', 'Санкт-Петербург')
                        .set_sort('last_name', reverse=False)
                        .get_k_n_short_list(k=1, n=5))
        print(f"Клиенты из Санкт-Петербурга, отсортированные по фамилии:")
        for client in chain_clients:
            print(f"  - {client}")
        
        print("\n✅ JSON декоратор работает отлично!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def test_yaml_decorator():
    """Демонстрирует использование декоратора с YAML репозиторием."""
    
    print("\n" + "=" * 60)
    print("ТЕСТ ДЕКОРАТОРА С YAML РЕПОЗИТОРИЕМ")
    print("=" * 60)
    
    yaml_file = "test_clients.yaml"
    
    try:
        # 1. Создаем репозиторий YAML
        yaml_repo = Client_rep_yaml(yaml_file)
        print(f"✅ Загружено {yaml_repo.get_count()} клиентов из YAML")
        
        # 2. Оборачиваем в декоратор
        decorated_repo = Client_rep_file_decorator(yaml_repo)
        
        # ============= ПРИМЕР 1: Фильтрация по городу =============
        print("\n--- ПРИМЕР 1: Клиенты из города 'Москва' ---")
        decorated_repo.set_filter('city', 'Москва')
        moscow_clients = decorated_repo.get_k_n_short_list(k=1, n=3)
        count = decorated_repo.get_count()
        print(f"Найдено {count} клиентов из Москвы")
        if moscow_clients:
            for client in moscow_clients:
                print(f"  - {client}")
        
        # ============= ПРИМЕР 2: Сортировка по ID (DESC) =============
        print("\n--- ПРИМЕР 2: Сортировка по ID (DESC) ---")
        decorated_repo.clear_filters()
        decorated_repo.set_sort('id', reverse=True)
        sorted_clients = decorated_repo.get_k_n_short_list(k=1, n=5)
        print(f"Клиенты, отсортированные по ID (от большего к меньшему):")
        for client in sorted_clients:
            print(f"  - {client}")
        
        print("\n✅ YAML декоратор работает отлично!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def test_comparison():
    """Демонстрирует, что оба декоратора работают одинаково."""
    
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ: JSON vs YAML с декораторами")
    print("=" * 60)
    
    json_file = "test_clients.json"
    yaml_file = "test_clients.yaml"
    
    try:
        # Проверяем что оба файла существуют и содержат данные
        json_repo = Client_rep_json(json_file)
        yaml_repo = Client_rep_yaml(yaml_file)
        
        json_count = json_repo.get_count()
        yaml_count = yaml_repo.get_count()
        
        print(f"\nКлиентов в JSON: {json_count}")
        print(f"Клиентов в YAML: {yaml_count}")
        
        if json_count == yaml_count:
            print("✅ Оба репозитория содержат одинаковое количество данных")
            
            # Сравниваем результаты фильтрации
            json_decorated = Client_rep_file_decorator(json_repo)
            yaml_decorated = Client_rep_file_decorator(yaml_repo)
            
            json_decorated.set_filter('city', 'Москва')
            yaml_decorated.set_filter('city', 'Москва')
            
            json_moscow = json_decorated.get_count()
            yaml_moscow = yaml_decorated.get_count()
            
            print(f"\nКлиентов из Москвы в JSON (с фильтром): {json_moscow}")
            print(f"Клиентов из Москвы в YAML (с фильтром): {yaml_moscow}")
            
            if json_moscow == yaml_moscow:
                print("✅ Фильтрация работает одинаково на обоих форматах!")
            else:
                print("⚠️  Результаты фильтрации отличаются")
        else:
            print("⚠️  Репозитории содержат разное количество данных")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    # Запускаем все тесты
    test_json_decorator()
    test_yaml_decorator()
    test_comparison()
    
    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print("=" * 60)

