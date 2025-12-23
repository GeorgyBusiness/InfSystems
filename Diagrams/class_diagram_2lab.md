classDiagram
    class Client_rep_base {
        <<abstract>>
        #List~Client~ _clients
        +file_path: string
        +get_by_id(id: int) Client
        +add(client: Client)
        +replace_by_id(id: int, client: Client)
        +delete_by_id(id: int)
        +get_k_n_short_list(k: int, n: int) List~ClientShort~
        +sort_by_field(field: string)
        +get_count() int
        #_load_from_file()* 
        #_save_to_file()*
    }

    class Client_rep_json {
        #_load_from_file()
        #_save_to_file()
    }

    class Client_rep_yaml {
        #_load_from_file()
        #_save_to_file()
    }

    class Client_rep_db {
        -DB_manager db_manager
        +get_by_id(id: int) Client
        +add(client: Client)
        +replace_by_id(id: int, client: Client)
        +delete_by_id(id: int)
        +get_k_n_short_list(k: int, n: int) List~ClientShort~
        +get_count() int
    }

    class Client_rep_db_adapter {
        -Client_rep_db db_repository
        +get_by_id(id: int) Client
        +add(client: Client)
        +replace_by_id(id: int, client: Client)
        +delete_by_id(id: int)
        +get_k_n_short_list(k: int, n: int) List~ClientShort~
        +get_count() int
        #_load_from_file()
        #_save_to_file()
    }

    class DB_manager {
        <<singleton>>
        -psycopg2.connection conn
        +execute_query(sql, params, fetch, commit)
        +execute_query_single(sql, params)
        +close()
    }

    Client_rep_base <|-- Client_rep_json : наследует
    Client_rep_base <|-- Client_rep_yaml : наследует
    Client_rep_base <|-- Client_rep_db_adapter : наследует
    Client_rep_db_adapter --> Client_rep_db : использует
    Client_rep_db --> DB_manager : использует
    Client_rep_base o-- Client : хранит список