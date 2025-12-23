import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any


class DB_manager:
    """
    Singleton класс для управления подключением к PostgreSQL базе данных.
    
    Обеспечивает единое соединение со всей программой и предоставляет
    метод для выполнения SQL запросов с контролем над курсором и транзакциями.
    """
    
    _instance: Optional['DB_manager'] = None
    
    def __new__(cls, db_params: Optional[Dict[str, Any]] = None) -> 'DB_manager':
        """
        Реализует паттерн Singleton через __new__.
        
        При первом вызове создает единственный экземпляр класса.
        При последующих вызовах возвращает существующий экземпляр.
        
        Args:
            db_params: словарь с параметрами подключения к БД
                      (используется только при первом создании)
        
        Returns:
            Единственный экземпляр класса DB_manager
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_params: Optional[Dict[str, Any]] = None):
        """
        Инициализирует менеджер БД с параметрами подключения.
        
        Инициализация происходит только при первом создании экземпляра,
        последующие вызовы игнорируют параметры.
        
        Args:
            db_params: словарь с параметрами подключения
                      (host, user, password, dbname, port - опционально)
        """
        # Инициализируем только если это первый вызов
        if not hasattr(self, 'conn'):
            if db_params is None:
                raise ValueError("db_params обязателен при первом создании DB_manager")
            self.conn = psycopg2.connect(**db_params)
    
    def execute_query(
        self,
        sql: str,
        params: Optional[tuple] = None,
        fetch: bool = False,
        commit: bool = False
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Выполняет SQL запрос с контролем над курсором и транзакциями.
        
        Args:
            sql: SQL запрос с плейсхолдерами %s
            params: кортеж параметров для подстановки в запрос
            fetch: если True, возвращает результат запроса
            commit: если True, выполняет коммит после запроса
        
        Returns:
            Список словарей (при fetch=True) или None
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql, params or ())
                
                result = None
                if fetch:
                    result = cursor.fetchall()
                
                if commit:
                    self.conn.commit()
                
                return result
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Ошибка при выполнении SQL запроса: {e}")
            raise
    
    def execute_query_single(
        self,
        sql: str,
        params: Optional[tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Выполняет SQL запрос и возвращает одну строку.
        
        Args:
            sql: SQL запрос с плейсхолдерами %s
            params: кортеж параметров для подстановки в запрос
        
        Returns:
            Словарь с данными строки или None
        """
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Ошибка при выполнении SQL запроса: {e}")
            raise
    
    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
    
    def __del__(self) -> None:
        """Гарантирует закрытие соединения при удалении объекта."""
        self.close()

