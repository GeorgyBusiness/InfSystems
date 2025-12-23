classDiagram
    %% --- ПАТТЕРН НАБЛЮДАТЕЛЬ (OBSERVER) ---
    class AbstractObserver {
        <<abstract>>
        +update(data)*
    }

    class Subject {
        -_observers: List
        +add_observer(observer)
        +remove_observer(observer)
        +notify(data)
    }

    %% --- МОДЕЛИ ДАННЫХ (CORE MODELS) ---
    class ClientBase {
        +int id
        +validate_phone(phone)$
        +validate_email(email)$
        +validate_name(name)$
    }

    class Client {
        +last_name: str
        +first_name: str
        +phone: str
        +email: str
        +total_spending: float
        ...
        +from_json(json)$
        +from_string(str)$
    }

    class ClientShort {
        +fullname: str
        +contact: str
        +total_spending: float
    }

    %% --- РЕПОЗИТОРИИ (DATA ACCESS LAYER) ---
    class Client_rep_base {
        <<abstract>>
        #_clients: List
        +get_by_id(id)
        +add(client)
        +replace_by_id(id, client)
        +delete_by_id(id)
        +get_k_n_short_list(k, n)
        #_load_from_file()*
    }

    class Client_rep_db_adapter {
        -db_repo: Client_rep_db
        +get_by_id(id)
        +add(client)
        +replace_by_id(id, client)
        +delete_by_id(id)
    }

    class Client_rep_db {
        -db_manager: DB_manager
        +get_by_id(id)
        +add(client)
        +delete_by_id(id)
    }

    class DB_manager {
        <<singleton>>
        -conn: connection
        +execute_query()
        +execute_query_single()
    }

    %% --- MVC: ВИД (VIEW) ---
    class ClientView {
        +last_data: Any
        +update(data)
        +render_main_page(clients)
        +render_client_details(client)
        +render_client_form(title, button_text, action_url, client, errors)
    }

    %% --- MVC: КОНТРОЛЛЕРЫ (CONTROLLERS) ---
    class ClientController {
        -repo: Client_rep_base
        -view: ClientView
        +index()
        +show_details(id)
    }

    class ClientAddController {
        -repo: Client_rep_base
        -view: ClientView
        +get_form()
        +save_client(data)
    }

    class ClientEditController {
        -repo: Client_rep_base
        -view: ClientView
        +get_edit_form(id)
        +update_client(id, data)
    }

    class ClientDeleteController {
        -repo: Client_rep_base
        +delete_client(id)
    }

    %% --- СВЯЗИ (RELATIONSHIPS) ---
    
    %% Реализация Observer
    AbstractObserver <|-- ClientView : реализует
    Subject <|-- Client_rep_base : наследует (Observable)
    
    %% Иерархия Репозиториев
    Client_rep_base <|-- Client_rep_db_adapter
    Client_rep_db_adapter --> Client_rep_db : адаптирует
    Client_rep_db --> DB_manager : использует
    
    %% Иерархия Моделей
    ClientBase <|-- Client
    ClientBase <|-- ClientShort
    
    %% MVC Агрегация (Контроллеры знают о Repo и View)
    ClientController o-- Client_rep_base
    ClientController o-- ClientView
    
    ClientAddController o-- Client_rep_base
    ClientAddController o-- ClientView
    
    ClientEditController o-- Client_rep_base
    ClientEditController o-- ClientView

    ClientDeleteController o-- Client_rep_base
    
    %% Зависимости (Использование классов)
    ClientAddController ..> Client : создает/валидирует
    ClientEditController ..> Client : создает/валидирует
    ClientView ..> ClientShort : отображает список
    ClientView ..> Client : отображает анкету