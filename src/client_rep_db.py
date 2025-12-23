import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any
from src.client import Client, ClientShort


class Client_rep_db:
    """
    Класс для управления коллекцией объектов Client в PostgreSQL базе данных.
    
    Работает напрямую с таблицей clients в базе данных,
    предоставляя CRUD операции и функции поиска/сортировки.
    """
    
    def __init__(self, db_params: Dict[str, Any]):
        """
        Инициализирует репозиторий с параметрами подключения к БД.
        
        Args:
            db_params: словарь с параметрами подключения
                      (host, user, password, dbname, port - опционально)
        """
        self.conn = psycopg2.connect(**db_params)
    
    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Возвращает объект Client по ID из БД или None, если не найден.
        
        Args:
            client_id: уникальный идентификатор клиента
            
        Returns:
            Client объект или None
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
                row = cursor.fetchone()
                
                if row:
                    return Client(**dict(row))
                return None
        except psycopg2.Error as e:
            print(f"Ошибка при выборе клиента по ID: {e}")
            return None
    
    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort]:
        """
        Возвращает список из n объектов класса ClientShort для k-й страницы.
        
        Использует LIMIT и OFFSET для постраничного получения данных из БД.
        
        Args:
            k: номер страницы (начиная с 1)
            n: размер страницы (количество элементов)
            
        Returns:
            Список объектов ClientShort размером до n элементов
        """
        if k < 1:
            raise ValueError("Номер страницы должен быть >= 1")
        if n < 1:
            raise ValueError("Размер страницы должен быть >= 1")
        
        offset = (k - 1) * n
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM clients ORDER BY id LIMIT %s OFFSET %s",
                    (n, offset)
                )
                rows = cursor.fetchall()
                
                clients = [Client(**dict(row)) for row in rows]
                return [ClientShort(client) for client in clients]
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка клиентов: {e}")
            return []
    
    def add(self, client: Client) -> None:
        """
        Добавляет новый объект Client в БД.
        
        База данных генерирует ID автоматически. Полученный ID записывается
        в объект client.
        
        Args:
            client: объект Client для добавления
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """INSERT INTO clients 
                       (last_name, first_name, patronymic, phone, email, 
                        passport_series, passport_number, zip_code, city, 
                        street, house, total_spending)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       RETURNING id""",
                    (
                        client.last_name,
                        client.first_name,
                        client.patronymic,
                        client.phone,
                        client.email,
                        client.passport_series,
                        client.passport_number,
                        client.zip_code,
                        client.city,
                        client.street,
                        client.house,
                        client.total_spending,
                    )
                )
                result = cursor.fetchone()
                if result:
                    client.id = result['id']
                
                self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Ошибка при добавлении клиента: {e}")
    
    def replace_by_id(self, client_id: int, new_client: Client) -> None:
        """
        Обновляет данные клиента по ID в БД.
        
        Args:
            client_id: ID клиента для обновления
            new_client: новый объект Client с новыми данными
            
        Raises:
            ValueError: если клиент с указанным ID не найден
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE clients 
                       SET last_name=%s, first_name=%s, patronymic=%s, phone=%s, 
                           email=%s, passport_series=%s, passport_number=%s, 
                           zip_code=%s, city=%s, street=%s, house=%s, 
                           total_spending=%s
                       WHERE id = %s""",
                    (
                        new_client.last_name,
                        new_client.first_name,
                        new_client.patronymic,
                        new_client.phone,
                        new_client.email,
                        new_client.passport_series,
                        new_client.passport_number,
                        new_client.zip_code,
                        new_client.city,
                        new_client.street,
                        new_client.house,
                        new_client.total_spending,
                        client_id,
                    )
                )
                
                if cursor.rowcount == 0:
                    raise ValueError(f"Клиент с ID {client_id} не найден")
                
                self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Ошибка при обновлении клиента: {e}")
    
    def delete_by_id(self, client_id: int) -> None:
        """
        Удаляет клиента из БД по ID.
        
        Args:
            client_id: ID клиента для удаления
            
        Raises:
            ValueError: если клиент с указанным ID не найден
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
                
                if cursor.rowcount == 0:
                    raise ValueError(f"Клиент с ID {client_id} не найден")
                
                self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Ошибка при удалении клиента: {e}")
    
    def get_count(self) -> int:
        """
        Возвращает общее количество клиентов в БД.
        
        Returns:
            int: количество клиентов
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM clients")
                result = cursor.fetchone()
                return result[0] if result else 0
        except psycopg2.Error as e:
            print(f"Ошибка при подсчете клиентов: {e}")
            return 0

