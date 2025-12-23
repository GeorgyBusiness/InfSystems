"""
Контроллер (Controller) для управления логикой приложения.

Связывает репозиторий (Model) с представлением (View) и управляет
обработкой запросов пользователя.
"""

from typing import Optional, Dict, List, Union
from src.repositories.client_rep_base import Client_rep_base
from src.mvc.client_view import ClientView
from src.models.client import Client


class ClientController:
    """
    Контроллер для управления клиентами.
    
    Взаимодействует с репозиторием для получения данных и передает их
    представлению для отображения. Реализует логику приложения.
    """
    
    def __init__(self, repo: Client_rep_base, view: ClientView) -> None:
        """
        Инициализирует контроллер с репозиторием и представлением.
        
        Args:
            repo: Объект репозитория для доступа к данным
            view: Объект представления для отображения результатов
        """
        self.repo = repo
        self.view = view
        
        # Подписываем представление на изменения в репозитории
        self.repo.add_observer(self.view)
    
    def index(self) -> str:
        """
        Обрабатывает главную страницу с списком клиентов.
        
        Получает первую страницу клиентов (по 10 на странице) из репозитория
        и возвращает HTML представление.
        
        Returns:
            HTML-строка главной страницы
        """
        try:
            # Получаем первую страницу с 10 клиентами
            clients_short = self.repo.get_k_n_short_list(k=1, n=10)
            
            # Уведомляем наблюдателей об обновлении данных
            self.repo.notify(clients_short)
            
            # Возвращаем HTML
            return self.view.render_main_page(clients_short)
        except Exception as e:
            return f"<h1>Ошибка</h1><p>Не удалось загрузить список клиентов: {e}</p>"
    
    def show_details(self, client_id: int) -> str:
        """
        Обрабатывает страницу с подробной информацией о клиенте.
        
        Получает клиента по ID из репозитория и возвращает HTML представление.
        
        Args:
            client_id: Уникальный идентификатор клиента
            
        Returns:
            HTML-строка со страницей деталей клиента
        """
        try:
            # Получаем клиента по ID
            client = self.repo.get_by_id(client_id)
            
            if not client:
                return f"<h1>Ошибка</h1><p>Клиент с ID {client_id} не найден</p>"
            
            # Уведомляем наблюдателей об обновлении данных
            self.repo.notify(client)
            
            # Возвращаем HTML
            return self.view.render_client_details(client)
        except Exception as e:
            return f"<h1>Ошибка</h1><p>Не удалось загрузить информацию о клиенте: {e}</p>"


class ClientAddController:
    """
    Контроллер для добавления новых клиентов.
    
    Управляет отображением формы добавления и обработкой данных формы
    с валидацией через класс Client.
    """
    
    def __init__(self, repo: Client_rep_base, view: ClientView) -> None:
        """
        Инициализирует контроллер добавления с репозиторием и представлением.
        
        Args:
            repo: Объект репозитория для сохранения данных
            view: Объект представления для отображения формы
        """
        self.repo = repo
        self.view = view
        
        # Подписываем представление на изменения в репозитории
        self.repo.add_observer(self.view)
    
    def get_form(self) -> str:
        """
        Возвращает HTML страницу с пустой формой добавления клиента.
        
        Returns:
            HTML-строка с пустой формой
        """
        return self.view.render_add_client_page()
    
    def save_client(self, form_data: Dict[str, str]) -> Union[bool, str]:
        """
        Пытается сохранить нового клиента на основе данных формы.
        
        Использует валидацию из класса Client (ЛР1):
        - Проверка телефона (7XXXXXXXXXX)
        - Проверка email
        - Проверка ФИО
        - Проверка паспортных данных
        - Проверка адреса и индекса
        - Проверка трат
        
        Args:
            form_data: Словарь с данными из формы
            
        Returns:
            True если клиент успешно сохранен
            HTML-строка с формой и ошибками если валидация не прошла
        """
        errors: List[str] = []
        
        try:
            # Преобразуем данные формы в нужные типы
            last_name = form_data.get('last_name', '').strip()
            first_name = form_data.get('first_name', '').strip()
            patronymic = form_data.get('patronymic', '').strip()
            phone = form_data.get('phone', '').strip()
            email = form_data.get('email', '').strip()
            passport_series = form_data.get('passport_series', '').strip()
            passport_number = form_data.get('passport_number', '').strip()
            zip_code_str = form_data.get('zip_code', '').strip()
            city = form_data.get('city', '').strip()
            street = form_data.get('street', '').strip()
            house = form_data.get('house', '').strip()
            total_spending_str = form_data.get('total_spending', '0.00').strip()
            
            # Преобразуем числовые поля
            try:
                zip_code = int(zip_code_str)
            except (ValueError, TypeError):
                zip_code = 0
            
            try:
                total_spending = float(total_spending_str)
            except (ValueError, TypeError):
                total_spending = 0.0
            
            # Пытаемся создать объект Client - валидация произойдет в конструкторе
            # Используем 1 как временный ID, база данных заменит его на реальный
            new_client = Client(
                id=1,
                last_name=last_name,
                first_name=first_name,
                patronymic=patronymic,
                phone=phone,
                email=email,
                passport_series=passport_series,
                passport_number=passport_number,
                zip_code=zip_code,
                city=city,
                street=street,
                house=house,
                total_spending=total_spending
            )
            
            # Валидация прошла, добавляем клиента в репозиторий
            self.repo.add(new_client)
            
            # Уведомляем наблюдателей
            self.repo.notify(new_client)
            
            return True
        
        except ValueError as e:
            # Ошибка валидации из класса Client
            error_message = str(e)
            errors.append(error_message)
            
            # Возвращаем форму с ошибками и введенными данными
            return self.view.render_add_client_page(
                errors=errors,
                form_data=form_data
            )
        except Exception as e:
            # Неожиданная ошибка
            errors.append(f"Неожиданная ошибка: {str(e)}")
            return self.view.render_add_client_page(
                errors=errors,
                form_data=form_data
            )


class ClientEditController:
    """
    Контроллер для редактирования существующих клиентов.
    
    Управляет отображением формы редактирования и обработкой обновлений
    с валидацией через класс Client.
    """
    
    def __init__(self, repo: Client_rep_base, view: ClientView) -> None:
        """
        Инициализирует контроллер редактирования с репозиторием и представлением.
        
        Args:
            repo: Объект репозитория для получения и обновления данных
            view: Объект представления для отображения формы
        """
        self.repo = repo
        self.view = view
        
        # Подписываем представление на изменения в репозитории
        self.repo.add_observer(self.view)
    
    def get_edit_form(self, client_id: int) -> str:
        """
        Возвращает HTML страницу с формой редактирования клиента.
        
        Получает клиента по ID и отображает форму с его текущими данными.
        
        Args:
            client_id: ID клиента для редактирования
            
        Returns:
            HTML-строка с предзаполненной формой редактирования
        """
        try:
            # Получаем клиента по ID
            client = self.repo.get_by_id(client_id)
            
            if not client:
                return f"<h1>Ошибка</h1><p>Клиент с ID {client_id} не найден</p>"
            
            # Уведомляем наблюдателей об обновлении данных
            self.repo.notify(client)
            
            # Возвращаем форму редактирования
            return self.view.render_edit_client_page(client)
        except Exception as e:
            return f"<h1>Ошибка</h1><p>Не удалось загрузить форму редактирования: {e}</p>"
    
    def update_client(self, client_id: int, form_data: Dict[str, str]) -> Union[bool, str]:
        """
        Пытается обновить данные клиента на основе данных формы.
        
        Использует валидацию из класса Client (ЛР1):
        - Все поля проверяются как при добавлении
        - При валидации вызывает repo.replace_by_id()
        
        Args:
            client_id: ID клиента для обновления
            form_data: Словарь с новыми данными из формы
            
        Returns:
            True если клиент успешно обновлен
            HTML-строка с формой и ошибками если валидация не прошла
        """
        errors: List[str] = []
        
        try:
            # Получаем текущего клиента (для использования его ID)
            current_client = self.repo.get_by_id(client_id)
            
            if not current_client:
                return f"<h1>Ошибка</h1><p>Клиент с ID {client_id} не найден</p>"
            
            # Преобразуем данные формы в нужные типы
            last_name = form_data.get('last_name', '').strip()
            first_name = form_data.get('first_name', '').strip()
            patronymic = form_data.get('patronymic', '').strip()
            phone = form_data.get('phone', '').strip()
            email = form_data.get('email', '').strip()
            passport_series = form_data.get('passport_series', '').strip()
            passport_number = form_data.get('passport_number', '').strip()
            zip_code_str = form_data.get('zip_code', '').strip()
            city = form_data.get('city', '').strip()
            street = form_data.get('street', '').strip()
            house = form_data.get('house', '').strip()
            total_spending_str = form_data.get('total_spending', '0.00').strip()
            
            # Преобразуем числовые поля
            try:
                zip_code = int(zip_code_str)
            except (ValueError, TypeError):
                zip_code = 0
            
            try:
                total_spending = float(total_spending_str)
            except (ValueError, TypeError):
                total_spending = 0.0
            
            # Пытаемся создать объект Client с новыми данными - валидация произойдет в конструкторе
            # Используем тот же ID, что и у текущего клиента
            updated_client = Client(
                id=client_id,
                last_name=last_name,
                first_name=first_name,
                patronymic=patronymic,
                phone=phone,
                email=email,
                passport_series=passport_series,
                passport_number=passport_number,
                zip_code=zip_code,
                city=city,
                street=street,
                house=house,
                total_spending=total_spending
            )
            
            # Валидация прошла, обновляем клиента в репозитории
            self.repo.replace_by_id(client_id, updated_client)
            
            # Уведомляем наблюдателей
            self.repo.notify(updated_client)
            
            return True
        
        except ValueError as e:
            # Ошибка валидации из класса Client
            error_message = str(e)
            errors.append(error_message)
            
            # Возвращаем форму с ошибками и текущими данными клиента
            try:
                current_client = self.repo.get_by_id(client_id)
                if current_client:
                    return self.view.render_edit_client_page(
                        current_client,
                        errors=errors
                    )
            except Exception:
                pass
            
            return f"<h1>Ошибка</h1><p>Ошибка валидации: {error_message}</p>"
        
        except Exception as e:
            # Неожиданная ошибка
            errors.append(f"Неожиданная ошибка: {str(e)}")
            try:
                current_client = self.repo.get_by_id(client_id)
                if current_client:
                    return self.view.render_edit_client_page(
                        current_client,
                        errors=errors
                    )
            except Exception:
                pass
            
            return f"<h1>Ошибка</h1><p>Ошибка обновления: {str(e)}</p>"

