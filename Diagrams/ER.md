// Таблица Клиентов (Наша главная сущность)
Table clients {
  id int [pk, increment] // Первичный ключ
  last_name varchar [note: 'Фамилия']
  first_name varchar [note: 'Имя']
  patronymic varchar [note: 'Отчество']
  phone varchar [unique, note: 'Телефон 7XXXXXXXXXX']
  email varchar [unique]
  passport_series varchar
  passport_number varchar
  zip_code int
  city varchar
  street varchar
  house varchar
  total_spending decimal [note: 'Сумма покупок для VIP статуса']
}

// Таблица Товаров
Table products {
  id int [pk, increment]
  name varchar
  price decimal
  unit varchar [note: 'кг, шт, л']
  stock_quantity int
}

// Таблица Заказов
Table orders {
  id int [pk, increment]
  client_id int [ref: > clients.id] // Связь с клиентом
  created_at datetime
  delivery_date datetime
  status varchar
}

// Таблица Состава заказа (Многие ко многим)
Table order_items {
  id int [pk, increment]
  order_id int [ref: > orders.id] // Ссылка на заказ
  product_id int [ref: > products.id] // Ссылка на товар
  quantity int
  price_at_moment decimal [note: 'Цена на момент покупки']
}