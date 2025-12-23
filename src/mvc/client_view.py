"""
Представление (View) для отображения информации о клиентах.

Генерирует HTML-контент для веб-приложения на основе данных,
полученных от контроллера.
"""

from typing import Any, List, Optional, Dict
from src.mvc.observer import AbstractObserver
from src.models.client import Client, ClientShort


class ClientView(AbstractObserver):
    """
    Представление для отображения клиентов.
    
    Реализует паттерн Observer для получения уведомлений об изменениях
    и генерирует HTML для веб-интерфейса.
    """
    
    def __init__(self) -> None:
        """Инициализирует представление с пустым состоянием."""
        self._state: Optional[Any] = None
    
    def update(self, data: Any) -> None:
        """
        Обновляет состояние представления при изменении данных в репозитории.
        
        Args:
            data: Данные об изменении из репозитория
        """
        self._state = data
    
    def _get_base_html(self, title: str, content: str) -> str:
        """
        Возвращает базовый HTML шаблон со стилями.
        
        Args:
            title: Заголовок страницы
            content: Содержимое страницы
            
        Returns:
            HTML-строка
        """
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }}
        th {{
            background-color: #007bff;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
            font-weight: 500;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #007bff;
            font-weight: 500;
        }}
        .info-box {{
            background-color: white;
            border-left: 4px solid #007bff;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .info-row label {{
            font-weight: 600;
            color: #333;
            min-width: 200px;
        }}
        .info-row span {{
            color: #666;
        }}
        .info-row:last-child {{
            border-bottom: none;
        }}
        .no-data {{
            text-align: center;
            color: #999;
            padding: 40px;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>"""
    
    def render_main_page(self, clients_short: List[ClientShort]) -> str:
        """
        Генерирует HTML главной страницы со списком клиентов.
        
        Args:
            clients_short: Список объектов ClientShort для отображения
            
        Returns:
            HTML-строка главной страницы
        """
        if not clients_short:
            content = '<h1>Список клиентов</h1><div class="no-data">Нет данных</div>'
            return self._get_base_html('Клиенты', content)
        
        # Генерируем строки таблицы
        table_rows = ""
        for client in clients_short:
            table_rows += f"""
        <tr>
            <td>{client.id}</td>
            <td>{client.fullname}</td>
            <td>{client.contact}</td>
            <td>{client.total_spending:.2f} ₽</td>
            <td>
                <a href="/client/{client.id}" target="_blank" style="margin-right: 10px;">Подробнее</a>
                <a href="/edit/{client.id}" style="margin-right: 10px;">Редактировать</a>
                <a href="/delete/{client.id}" style="color: #dc3545; margin-right: 10px;" onclick="return confirm('Вы уверены, что хотите удалить этого клиента?');">Удалить</a>
            </td>
        </tr>
"""
        
        table_html = f"""<h1>Список клиентов</h1>
    <div style="margin-bottom: 20px;">
        <a href="/add" style="display: inline-block; padding: 10px 20px; background-color: #28a745; color: white; border-radius: 4px; text-decoration: none; font-weight: 600;">+ Добавить нового клиента</a>
    </div>
    
    <div style="background-color: white; padding: 15px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <form method="GET" action="/" style="display: flex; gap: 10px; flex-wrap: wrap; align-items: flex-end;">
            <div style="display: flex; flex-direction: column;">
                <label for="filter_city" style="font-weight: 600; margin-bottom: 5px; color: #333; font-size: 14px;">Фильтр по городу:</label>
                <input type="text" id="filter_city" name="filter_city" placeholder="Например: Москва" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px; min-width: 150px;">
            </div>
            
            <div style="display: flex; flex-direction: column;">
                <label for="sort_by" style="font-weight: 600; margin-bottom: 5px; color: #333; font-size: 14px;">Сортировать по:</label>
                <select id="sort_by" name="sort_by" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    <option value="">-- Выберите поле --</option>
                    <option value="id">ID</option>
                    <option value="last_name">Фамилия</option>
                    <option value="total_spending">Траты</option>
                </select>
            </div>
            
            <div style="display: flex; flex-direction: column;">
                <label for="sort_order" style="font-weight: 600; margin-bottom: 5px; color: #333; font-size: 14px;">Порядок:</label>
                <select id="sort_order" name="sort_order" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    <option value="ASC">По возрастанию (ASC)</option>
                    <option value="DESC">По убыванию (DESC)</option>
                </select>
            </div>
            
            <button type="submit" style="padding: 8px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; font-weight: 600; cursor: pointer;">🔍 Применить</button>
            <a href="/" style="padding: 8px 20px; background-color: #6c757d; color: white; border-radius: 4px; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center;">✕ Сбросить</a>
        </form>
    </div>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>ФИО</th>
                <th>Контакт</th>
                <th>Траты</th>
                <th>Действия</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>"""
        
        return self._get_base_html('Клиенты', table_html)
    
    def render_client_details(self, client: Client) -> str:
        """
        Генерирует HTML страницы с подробной информацией о клиенте.
        
        Args:
            client: Объект Client с полной информацией
            
        Returns:
            HTML-строка с деталями клиента
        """
        if not client:
            content = '<h1>Детали клиента</h1><div class="no-data">Клиент не найден</div>'
            return self._get_base_html('Детали клиента', content)
        
        details_html = f"""<a href="/" class="back-link">← Вернуться на главную</a>
    <h1>Детали клиента (ID: {client.id})</h1>
    <div class="info-box">
        <h2>Личные данные</h2>
        <div class="info-row">
            <label>ФИО:</label>
            <span>{client.last_name} {client.first_name} {client.patronymic}</span>
        </div>
        <div class="info-row">
            <label>Телефон:</label>
            <span><a href="tel:{client.phone}">{client.phone}</a></span>
        </div>
        <div class="info-row">
            <label>Email:</label>
            <span><a href="mailto:{client.email}">{client.email}</a></span>
        </div>
        <div class="info-row">
            <label>Паспорт:</label>
            <span>{client.passport_series} {client.passport_number}</span>
        </div>
    </div>
    <div class="info-box">
        <h2>Адрес проживания</h2>
        <div class="info-row">
            <label>Почтовый индекс:</label>
            <span>{client.zip_code}</span>
        </div>
        <div class="info-row">
            <label>Город:</label>
            <span>{client.city}</span>
        </div>
        <div class="info-row">
            <label>Улица:</label>
            <span>{client.street}</span>
        </div>
        <div class="info-row">
            <label>Дом:</label>
            <span>{client.house}</span>
        </div>
    </div>
    <div class="info-box">
        <h2>Финансовая информация</h2>
        <div class="info-row">
            <label>Общие траты:</label>
            <span style="font-size: 18px; font-weight: 600; color: #28a745;">{client.total_spending:.2f} ₽</span>
        </div>
    </div>"""
        
        return self._get_base_html(f'Клиент {client.last_name}', details_html)
    
    def render_client_form(self, title: str, button_text: str, action_url: str, client: Optional[Client] = None, errors: Optional[List[str]] = None) -> str:
        """
        Генерирует универсальную HTML форму для добавления или редактирования клиента.
        
        Параметры title, button_text и action_url позволяют переиспользовать форму
        для разных операций (Add/Edit).
        
        Args:
            title: Заголовок формы (например, "Добавление клиента" или "Редактирование клиента")
            button_text: Текст на кнопке отправки (например, "Создать" или "Сохранить изменения")
            action_url: URL для отправки формы (например, "/add" или "/edit/1")
            client: Объект Client для предзаполнения формы (если None - форма пустая для добавления)
            errors: Список ошибок валидации (если есть)
            
        Returns:
            HTML-строка с формой
        """
        # Если передан client, используем его данные; иначе пустые значения
        last_name = client.last_name if client else ''
        first_name = client.first_name if client else ''
        patronymic = client.patronymic if client else ''
        phone = client.phone if client else ''
        email = client.email if client else ''
        passport_series = client.passport_series if client else ''
        passport_number = client.passport_number if client else ''
        zip_code = str(client.zip_code) if client else ''
        city = client.city if client else ''
        street = client.street if client else ''
        house = client.house if client else ''
        total_spending = f"{client.total_spending:.2f}" if client else '0.00'
        
        # Генерируем блок ошибок, если они есть
        errors_html = ""
        if errors:
            errors_list = "".join([f"<li>{error}</li>" for error in errors])
            errors_html = f"""<div style="background-color: #f8d7da; color: #721c24; padding: 12px; border: 1px solid #f5c6cb; border-radius: 4px; margin-bottom: 20px;">
        <strong>❌ Ошибки при заполнении формы:</strong>
        <ul style="margin: 10px 0 0 0;">
            {errors_list}
        </ul>
    </div>"""
        
        form_html = f"""<a href="/" style="display: inline-block; margin-bottom: 20px; color: #007bff; font-weight: 500;">← Вернуться на главную</a>
    <h1>{title}</h1>
    {errors_html}
    <form method="POST" action="{action_url}" style="background-color: white; padding: 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
        <fieldset style="border: none; margin: 0; padding: 0;">
            <legend style="font-size: 18px; font-weight: 600; margin-bottom: 20px; color: #333;">Личные данные</legend>
            
            <div style="margin-bottom: 15px;">
                <label for="last_name" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Фамилия *</label>
                <input type="text" id="last_name" name="last_name" value="{last_name}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label for="first_name" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Имя *</label>
                <input type="text" id="first_name" name="first_name" value="{first_name}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label for="patronymic" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Отчество</label>
                <input type="text" id="patronymic" name="patronymic" value="{patronymic}" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label for="phone" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Телефон (7XXXXXXXXXX) *</label>
                <input type="tel" id="phone" name="phone" value="{phone}" placeholder="79991234567" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label for="email" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email *</label>
                <input type="email" id="email" name="email" value="{email}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
        </fieldset>
        
        <fieldset style="border: none; margin: 30px 0 0 0; padding: 20px 0 0 0; border-top: 2px solid #eee;">
            <legend style="font-size: 18px; font-weight: 600; margin-bottom: 20px; color: #333;">Паспортные данные</legend>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                <div>
                    <label for="passport_series" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Серия (4 цифры) *</label>
                    <input type="text" id="passport_series" name="passport_series" value="{passport_series}" placeholder="1234" maxlength="4" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
                </div>
                <div>
                    <label for="passport_number" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Номер (6 цифр) *</label>
                    <input type="text" id="passport_number" name="passport_number" value="{passport_number}" placeholder="567890" maxlength="6" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
                </div>
            </div>
        </fieldset>
        
        <fieldset style="border: none; margin: 30px 0 0 0; padding: 20px 0 0 0; border-top: 2px solid #eee;">
            <legend style="font-size: 18px; font-weight: 600; margin-bottom: 20px; color: #333;">Адрес проживания</legend>
            
            <div style="margin-bottom: 15px;">
                <label for="zip_code" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Почтовый индекс (6 цифр) *</label>
                <input type="text" id="zip_code" name="zip_code" value="{zip_code}" placeholder="123456" maxlength="6" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label for="city" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Город *</label>
                <input type="text" id="city" name="city" value="{city}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label for="street" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Улица *</label>
                <input type="text" id="street" name="street" value="{street}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label for="house" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Номер дома *</label>
                <input type="text" id="house" name="house" value="{house}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
        </fieldset>
        
        <fieldset style="border: none; margin: 30px 0 0 0; padding: 20px 0 0 0; border-top: 2px solid #eee;">
            <legend style="font-size: 18px; font-weight: 600; margin-bottom: 20px; color: #333;">Финансовая информация</legend>
            
            <div style="margin-bottom: 15px;">
                <label for="total_spending" style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Общие траты (₽) *</label>
                <input type="number" id="total_spending" name="total_spending" value="{total_spending}" step="0.01" min="0" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;">
            </div>
        </fieldset>
        
        <div style="margin-top: 30px; display: flex; gap: 10px;">
            <button type="submit" style="padding: 12px 30px; background-color: #007bff; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer;">✓ {button_text}</button>
            <a href="/" style="padding: 12px 30px; background-color: #6c757d; color: white; border-radius: 4px; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center;">✕ Отмена</a>
        </div>
    </form>"""
        
        return self._get_base_html(title, form_html)


