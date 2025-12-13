# ER-диаграмма базы данных (ЛР1)

```mermaid
erDiagram
    %% --- Таблица Клиентов ---
    CLIENTS {
        int id PK
        varchar last_name "Фамилия"
        varchar first_name "Имя"
        varchar patronymic "Отчество"
        varchar phone "Телефон 7XXXXXXXXXX"
        varchar email
        varchar passport_series
        varchar passport_number
        int zip_code
        varchar city
        varchar street
        varchar house
        decimal total_spending "Сумма для VIP"
    }

    %% --- Таблица Товаров ---
    PRODUCTS {
        int id PK
        varchar name
        decimal price
        varchar unit "кг, шт, л"
        int stock_quantity
    }

    %% --- Таблица Заказов ---
    ORDERS {
        int id PK
        int client_id FK
        datetime created_at
        datetime delivery_date
        varchar status
    }

    %% --- Состав заказа (Многие-ко-многим) ---
    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price_at_moment "Цена покупки"
    }

    %% --- Связи (Relationships) ---
    %% Один клиент делает много заказов (||--o{)
    CLIENTS ||--o{ ORDERS : places

    %% Один заказ содержит много позиций (||--|{)
    ORDERS ||--|{ ORDER_ITEMS : contains

    %% Один товар может быть во многих позициях заказов (||--o{)
    PRODUCTS ||--o{ ORDER_ITEMS : included_in