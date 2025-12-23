"""
Flask Web Application для управления клиентами.

Использует паттерны MVC и Observer для структурирования приложения.
"""

from flask import Flask, render_template_string, request, redirect, url_for
from src.core.db_manager import DB_manager
from src.repositories.client_rep_db import Client_rep_db
from src.repositories.client_rep_db_adapter import Client_rep_db_adapter
from src.mvc.client_view import ClientView
from src.mvc.client_controller import ClientController, ClientAddController, ClientEditController, ClientDeleteController


# Параметры подключения к базе данных
DB_PARAMS = {
    "host": "localhost",
    "user": "postgres",
    "password": "Cill020Cash!",
    "dbname": "internet_shop",
    "port": "5432"
}


def create_app() -> Flask:
    """
    Создает и конфигурирует Flask приложение.
    
    Returns:
        Настроенное Flask приложение
    """
    app = Flask(__name__)
    
    # Инициализируем компоненты MVC
    try:
        # 1. Создаем Singleton DB_manager
        db_manager = DB_manager(DB_PARAMS)
        
        # 2. Создаем репозиторий с адаптером
        base_repo = Client_rep_db(db_manager)
        repo = Client_rep_db_adapter(base_repo)
        
        # 3. Создаем представление
        view = ClientView()
        
        # 4. Создаем контроллер чтения (он подписывает представление)
        controller = ClientController(repo, view)
        
        # 5. Создаем контроллер добавления
        add_controller = ClientAddController(repo, view)
        
        # 6. Создаем контроллер редактирования
        edit_controller = ClientEditController(repo, view)
        
        # 7. Создаем контроллер удаления
        delete_controller = ClientDeleteController(repo)
        
    except Exception as e:
        print(f"❌ Ошибка инициализации приложения: {e}")
        return app
    
    @app.route('/')
    def index():
        """
        Главная страница со списком всех клиентов.
        
        Поддерживает параметры запроса для фильтрации и сортировки:
        - filter_city: фильтр по городу
        - sort_by: поле для сортировки (id, last_name, total_spending)
        - sort_order: порядок сортировки (ASC или DESC)
        
        Returns:
            HTML представление главной страницы
        """
        # Получаем параметры запроса
        params = request.args.to_dict() if request.args else None
        
        # Передаем параметры в контроллер
        return render_template_string(controller.index(params))
    
    @app.route('/client/<int:client_id>')
    def show_client(client_id: int):
        """
        Страница с подробной информацией о клиенте.
        
        Args:
            client_id: ID клиента для отображения
            
        Returns:
            HTML представление деталей клиента
        """
        return render_template_string(controller.show_details(client_id))
    
    @app.route('/add', methods=['GET', 'POST'])
    def add_client():
        """
        Страница добавления нового клиента.
        
        GET: отображает пустую форму добавления
        POST: обрабатывает отправленную форму с данными нового клиента
        
        Returns:
            На GET: HTML форма добавления
            На POST успешное добавление: редирект на главную
            На POST ошибка валидации: форма с сообщениями об ошибках
        """
        if request.method == 'POST':
            # Собираем данные из формы
            form_data = {
                'last_name': request.form.get('last_name', ''),
                'first_name': request.form.get('first_name', ''),
                'patronymic': request.form.get('patronymic', ''),
                'phone': request.form.get('phone', ''),
                'email': request.form.get('email', ''),
                'passport_series': request.form.get('passport_series', ''),
                'passport_number': request.form.get('passport_number', ''),
                'zip_code': request.form.get('zip_code', ''),
                'city': request.form.get('city', ''),
                'street': request.form.get('street', ''),
                'house': request.form.get('house', ''),
                'total_spending': request.form.get('total_spending', '0.00'),
            }
            
            # Пытаемся сохранить клиента
            result = add_controller.save_client(form_data)
            
            if result is True:
                # Успешное сохранение, редирект на главную
                return redirect(url_for('index'))
            else:
                # Ошибка валидации, возвращаем форму с ошибками
                return render_template_string(result)
        
        # GET: отображаем пустую форму
        return render_template_string(add_controller.get_form())
    
    @app.route('/edit/<int:client_id>', methods=['GET', 'POST'])
    def edit_client(client_id: int):
        """
        Страница редактирования данных клиента.
        
        GET: отображает форму редактирования с текущими данными
        POST: обрабатывает отправленную форму с обновленными данными
        
        Args:
            client_id: ID клиента для редактирования
            
        Returns:
            На GET: HTML форма редактирования с текущими данными
            На POST успешное обновление: редирект на главную
            На POST ошибка валидации: форма с сообщениями об ошибках
        """
        if request.method == 'POST':
            # Собираем новые данные из формы
            form_data = {
                'last_name': request.form.get('last_name', ''),
                'first_name': request.form.get('first_name', ''),
                'patronymic': request.form.get('patronymic', ''),
                'phone': request.form.get('phone', ''),
                'email': request.form.get('email', ''),
                'passport_series': request.form.get('passport_series', ''),
                'passport_number': request.form.get('passport_number', ''),
                'zip_code': request.form.get('zip_code', ''),
                'city': request.form.get('city', ''),
                'street': request.form.get('street', ''),
                'house': request.form.get('house', ''),
                'total_spending': request.form.get('total_spending', '0.00'),
            }
            
            # Пытаемся обновить клиента
            result = edit_controller.update_client(client_id, form_data)
            
            if result is True:
                # Успешное обновление, редирект на главную
                return redirect(url_for('index'))
            else:
                # Ошибка валидации, возвращаем форму с ошибками
                return render_template_string(result)
        
        # GET: отображаем форму редактирования
        return render_template_string(edit_controller.get_edit_form(client_id))
    
    @app.route('/delete/<int:client_id>')
    def delete_client(client_id: int):
        """
        Удаляет клиента по ID и перенаправляет на главную страницу.
        
        Args:
            client_id: ID клиента для удаления
            
        Returns:
            Редирект на главную страницу (/)
        """
        # Удаляем клиента
        success = delete_controller.delete_client(client_id)
        
        # В любом случае редирект на главную
        return redirect(url_for('index'))
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("🚀 Запуск Flask приложения...")
    print("📍 Приложение доступно по адресу: http://localhost:5001")
    print("🔗 Главная страница: http://localhost:5001/")
    print("📄 Пример деталей клиента: http://localhost:5001/client/1")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

