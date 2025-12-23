sequenceDiagram
    autonumber
    actor User as Пользователь
    participant App as app.py (Flask)
    participant Ctrl as ClientController
    participant Repo as Client_rep_db_adapter
    participant View as ClientView

    User->>App: GET / (Главная страница)
    App->>Ctrl: index()
    
    Note over Ctrl, Repo: Получение данных
    Ctrl->>Repo: get_k_n_short_list(1, 20)
    Repo-->>Ctrl: List[ClientShort]
    
    Note over Ctrl, Repo: Паттерн Наблюдатель (Notify)
    Ctrl->>Repo: notify(clients_data)
    Repo->>View: update(clients_data)
    View-->>Repo: Подтверждение получения
    
    Note over Ctrl, View: Формирование интерфейса
    Ctrl->>View: render_main_page(clients_data)
    View-->>Ctrl: HTML String (Table)
    
    Ctrl-->>App: HTML Response
    App-->>User: Отображение страницы в браузере