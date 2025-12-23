classDiagram
    %% Базовые интерфейсы паттерна Наблюдатель
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

    %% Модели данных
    class ClientBase {
        +int id
        +validate_phone(phone)$
        +validate_email(email)$
    }
    class Client {
        +last_name: str
        +phone: str
        ...
        +from_json(json)$
    }

    %% Репозитории (Data Layer)
    class Client_rep_base {
        <<abstract>>
        +add(client)
        +get_k_n_short_list()
    }

    class Client_rep_db_adapter {
        -db_repository: Client_rep_db
        +add(client)
    }

    %% MVC - Вид
    class ClientView {
        +render_main_page(clients)
        +render_client_details(client)
        +render_add_client_page(errors, data)
        +update(data)
    }

    %% MVC - Контроллеры
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

    %% Связи
    AbstractObserver <|-- ClientView
    Subject <|-- Client_rep_base
    Client_rep_base <|-- Client_rep_db_adapter
    
    ClientBase <|-- Client
    
    ClientController o-- Client_rep_base
    ClientController o-- ClientView
    
    ClientAddController o-- Client_rep_base
    ClientAddController o-- ClientView
    
    %% Показываем, что контроллер создает модель для валидации
    ClientAddController ..> Client : creates & validates