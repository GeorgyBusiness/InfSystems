sequenceDiagram
    autonumber
    actor User as Пользователь
    participant App as app.py (Flask)
    participant Ctrl as ClientAddController
    participant Model as Client (Model)
    participant Repo as Client_rep_db_adapter
    participant View as ClientView

    Note over User, View: Отображение формы
    User->>App: GET /add
    App->>Ctrl: get_form()
    Ctrl->>View: render_add_client_page()
    View-->>Ctrl: HTML (Пустая форма)
    Ctrl-->>App: HTML Response
    App-->>User: Страница добавления

    Note over User, View: Сохранение данных
    User->>App: POST /add (form data)
    App->>Ctrl: save_client(data)
    
    Note over Ctrl, Model: Валидация (из ЛР1)
    Ctrl->>Model: Создание объекта для проверки
    alt Данные некорректны (ValueError)
        Model-->>Ctrl: Ошибка валидации
        Ctrl->>View: render_add_client_page(errors, data)
        View-->>Ctrl: HTML (Форма с ошибками)
        Ctrl-->>User: Отображение ошибок
    else Данные верны
        Model-->>Ctrl: Объект создан успешно
        Ctrl->>Repo: add(client_object)
        Repo-->>Ctrl: Успех (Объект с ID)
        Ctrl-->>App: True
        App-->>User: Redirect to "/"
    end