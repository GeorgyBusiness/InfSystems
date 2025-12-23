sequenceDiagram
    autonumber
    actor User as Пользователь
    participant App as app.py
    participant AddCtrl as ClientAddController
    participant EditCtrl as ClientEditController
    participant View as ClientView (Unified)

    Note over User, View: Сценарий А: Добавление
    User->>App: GET /add
    App->>AddCtrl: get_form()
    AddCtrl->>View: render_client_form(title="Add", client=None)
    View-->>User: Пустая форма

    Note over User, View: Сценарий Б: Редактирование
    User->>App: GET /edit/1
    App->>EditCtrl: get_edit_form(1)
    EditCtrl->>View: render_client_form(title="Edit", client=obj)
    View-->>User: Предзаполненная форма