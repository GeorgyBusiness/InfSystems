sequenceDiagram
    autonumber
    actor User as Пользователь
    participant App as app.py (Flask)
    participant Ctrl as ClientDeleteController
    participant Repo as Client_rep_db_adapter
    participant DB as PostgreSQL

    User->>User: Нажимает "Удалить" и подтверждает (JS Confirm)
    User->>App: GET /delete/1
    App->>Ctrl: delete_client(1)
    
    Note over Ctrl, DB: Процесс удаления
    Ctrl->>Repo: delete_by_id(1)
    Repo->>DB: DELETE FROM clients WHERE id = 1
    DB-->>Repo: OK (Rows affected)
    Repo-->>Ctrl: Успех
    
    Ctrl-->>App: Сигнал завершения
    App-->>User: Redirect to "/" (Обновленный список)