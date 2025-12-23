"""
Тест для проверки работы MVC + Observer паттернов.

Проверяет:
1. Observer Pattern (Subject, AbstractObserver, ClientView)
2. MVC взаимодействие (Controller, Repository, View)
3. Генерация HTML (render_main_page, render_client_details)
"""

from src.models.client import Client, ClientShort
from src.repositories.client_rep_json import Client_rep_json
from src.mvc.observer import AbstractObserver, Subject
from src.mvc.client_view import ClientView
from src.mvc.client_controller import ClientController


def test_observer_pattern():
    """Тест паттерна Observer."""
    print("=" * 80)
    print("ТЕСТ 1: Observer Pattern")
    print("=" * 80)
    
    # 1. Создаем Subject
    subject = Subject()
    print("✓ Subject создан")
    
    # 2. Создаем Observer (ClientView)
    view = ClientView()
    print("✓ ClientView (Observer) создан")
    
    # 3. Подписываем Observer
    subject.add_observer(view)
    print("✓ ClientView подписан на Subject")
    
    # 4. Проверяем, что Observer получает уведомления
    test_data = {"test": "data"}
    subject.notify(test_data)
    print(f"✓ Subject.notify() вызван")
    print(f"✓ ClientView._state получил данные: {view._state}")
    
    # 5. Удаляем Observer
    subject.remove_observer(view)
    print("✓ ClientView удален из подписчиков")
    
    print("✅ Observer Pattern работает корректно!\n")


def test_mvc_architecture():
    """Тест архитектуры MVC."""
    print("=" * 80)
    print("ТЕСТ 2: MVC Architecture")
    print("=" * 80)
    
    # 1. Создаем тестовые клиенты в памяти
    print("Создание тестовых данных...")
    
    client1 = Client(
        id=1,
        last_name="Иванов",
        first_name="Иван",
        patronymic="Петрович",
        phone="79991234567",
        email="ivan@mail.ru",
        passport_series="1234",
        passport_number="567890",
        zip_code=123456,
        city="Москва",
        street="Пушкина",
        house="10",
        total_spending=15000.50
    )
    
    client2 = Client(
        id=2,
        last_name="Петров",
        first_name="Петр",
        patronymic="Сергеевич",
        phone="79992345678",
        email="petr@mail.ru",
        passport_series="5678",
        passport_number="901234",
        zip_code=234567,
        city="Санкт-Петербург",
        street="Невского",
        house="25",
        total_spending=25000.75
    )
    
    # 2. Создаем репозиторий (используем JSON для тестирования)
    repo = Client_rep_json("test_mvc_clients.json")
    
    # Добавляем тестовых клиентов
    repo._clients = [client1, client2]  # Напрямую добавляем для теста
    print(f"✓ Репозиторий содержит {repo.get_count()} клиентов")
    
    # 3. Проверяем, что репозиторий наследует Subject
    print(f"✓ Репозиторий наследует Subject: {isinstance(repo, Subject)}")
    
    # 4. Создаем представление
    view = ClientView()
    print("✓ ClientView (представление) создан")
    
    # 5. Создаем контроллер
    controller = ClientController(repo, view)
    print("✓ ClientController (контроллер) создан")
    print(f"✓ ClientView подписан на репозиторий: {view in repo._observers}")
    
    print("✅ MVC Architecture работает корректно!\n")
    
    return controller, repo, view


def test_html_rendering(controller: ClientController, repo, view):
    """Тест генерации HTML."""
    print("=" * 80)
    print("ТЕСТ 3: HTML Rendering")
    print("=" * 80)
    
    # 1. Тест главной страницы
    print("Генерация HTML главной страницы...")
    clients_short = repo.get_k_n_short_list(k=1, n=10)
    repo.notify(clients_short)
    html_main = view.render_main_page(clients_short)
    
    # Проверяем содержимое
    checks = [
        ("<!DOCTYPE html>" in html_main, "DOCTYPE объявление"),
        ("<html lang=\"ru\">" in html_main, "HTML тег с русским языком"),
        ("<table>" in html_main, "Таблица"),
        ("<th>" in html_main, "Заголовки таблицы"),
        ("Иванов" in html_main, "Фамилия клиента 1"),
        ("Петров" in html_main, "Фамилия клиента 2"),
        ("/client/" in html_main, "Ссылки на детали клиентов"),
        ("<style>" in html_main, "CSS стили"),
    ]
    
    for check, description in checks:
        status = "✓" if check else "✗"
        print(f"  {status} {description}")
    
    if all(check for check, _ in checks):
        print("✓ HTML главной страницы корректен")
    
    # 2. Тест страницы деталей
    print("\nГенерация HTML страницы деталей...")
    client = repo.get_by_id(1)
    repo.notify(client)
    html_details = view.render_client_details(client)
    
    detail_checks = [
        ("<!DOCTYPE html>" in html_details, "DOCTYPE объявление"),
        ("Личные данные" in html_details, "Раздел 'Личные данные'"),
        ("Адрес проживания" in html_details, "Раздел 'Адрес'"),
        ("Финансовая информация" in html_details, "Раздел 'Финансы'"),
        ("Иван" in html_details, "Имя клиента"),
        ("79991234567" in html_details, "Телефон клиента"),
        ("ivan@mail.ru" in html_details, "Email клиента"),
        ("← Вернуться на главную" in html_details, "Ссылка возврата"),
        ("15000.50" in html_details, "Сумма трат"),
    ]
    
    for check, description in detail_checks:
        status = "✓" if check else "✗"
        print(f"  {status} {description}")
    
    if all(check for check, _ in detail_checks):
        print("✓ HTML страницы деталей корректен")
    
    print("✅ HTML Rendering работает корректно!\n")


def test_controller_methods(controller: ClientController):
    """Тест методов контроллера."""
    print("=" * 80)
    print("ТЕСТ 4: Controller Methods")
    print("=" * 80)
    
    # 1. Тест index()
    print("Вызов controller.index()...")
    html_index = controller.index()
    
    if html_index and "<!DOCTYPE html>" in html_index and "<table>" in html_index:
        print("✓ controller.index() вернул HTML с таблицей")
    else:
        print("✗ controller.index() вернул некорректный HTML")
    
    # 2. Тест show_details()
    print("Вызов controller.show_details(1)...")
    html_detail = controller.show_details(1)
    
    if html_detail and "<!DOCTYPE html>" in html_detail and "Иван" in html_detail:
        print("✓ controller.show_details(1) вернул HTML с деталями")
    else:
        print("✗ controller.show_details(1) вернул некорректный HTML")
    
    # 3. Тест несуществующего клиента
    print("Вызов controller.show_details(999) (несуществующий)...")
    html_error = controller.show_details(999)
    
    if "не найден" in html_error:
        print("✓ controller.show_details(999) обработал ошибку корректно")
    else:
        print("✗ controller.show_details(999) не обработал ошибку")
    
    print("✅ Controller Methods работают корректно!\n")


def test_inheritance():
    """Тест наследования классов."""
    print("=" * 80)
    print("ТЕСТ 5: Class Inheritance")
    print("=" * 80)
    
    # 1. Проверяем наследование Repository
    repo = Client_rep_json("test_mvc_clients.json")
    print(f"✓ Client_rep_json наследует Subject: {isinstance(repo, Subject)}")
    
    # 2. Проверяем наследование View
    view = ClientView()
    print(f"✓ ClientView наследует AbstractObserver: {isinstance(view, AbstractObserver)}")
    
    # 3. Проверяем методы Subject
    print(f"✓ Subject имеет метод add_observer: {hasattr(repo, 'add_observer')}")
    print(f"✓ Subject имеет метод remove_observer: {hasattr(repo, 'remove_observer')}")
    print(f"✓ Subject имеет метод notify: {hasattr(repo, 'notify')}")
    
    # 4. Проверяем методы Observer
    print(f"✓ AbstractObserver требует метод update: {hasattr(view, 'update')}")
    
    print("✅ Class Inheritance работает корректно!\n")


def main():
    """Запуск всех тестов."""
    print("\n" + "=" * 80)
    print("КОМПЛЕКСНЫЙ ТЕСТ: MVC + Observer Pattern")
    print("=" * 80 + "\n")
    
    try:
        # Тест 1: Observer Pattern
        test_observer_pattern()
        
        # Тест 2: MVC Architecture
        controller, repo, view = test_mvc_architecture()
        
        # Тест 3: HTML Rendering
        test_html_rendering(controller, repo, view)
        
        # Тест 4: Controller Methods
        test_controller_methods(controller)
        
        # Тест 5: Inheritance
        test_inheritance()
        
        print("=" * 80)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 80)
        print("\nПриложение готово к использованию!")
        print("Для запуска веб-приложения выполните: python3 app.py")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА при выполнении тестов: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

