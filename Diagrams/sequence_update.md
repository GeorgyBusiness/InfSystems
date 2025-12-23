sequenceDiagram
    autonumber
    actor User as Пользователь
    participant App as app.py (Flask)
    participant Ctrl as ClientEditController
    participant Model as Client (Model)
    participant Repo as Client_rep_db_adapter
    participant View as ClientView

    User->>App: GET /edit/1
    App->>Ctrl: get_edit_form(1)
    Ctrl->>Repo: get_by_id(1)
    Repo-->>Ctrl: Объект Client
    Ctrl->>View: render_edit_client_page(client)
    View-->>User: Форма с данными клиента

    User->>App: POST /edit/1 (новые данные)
    App->>Ctrl: update_client(1, data)
    Note over Ctrl, Model: Валидация изменений
    Ctrl->>Model: Создание объекта Client
    alt Ошибка в данных
        Model-->>Ctrl: ValueError
        Ctrl->>View: render_edit_client_page(errors)
        View-->>User: Форма с текстом ошибки
    else Данные корректны
        Model-->>Ctrl: Успех
        Ctrl->>Repo: replace_by_id(1, new_client)
        Repo-->>Ctrl: OK
        Ctrl-->>App: True
        App-->>User: Redirect to "/"
    end