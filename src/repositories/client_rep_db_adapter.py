from typing import List, Optional
from src.repositories.client_rep_base import Client_rep_base
from src.repositories.client_rep_db import Client_rep_db
from src.models.client import Client, ClientShort


class Client_rep_db_adapter(Client_rep_base):
    """
    Адаптер для включения Client_rep_db в иерархию репозиториев.
    
    Адаптирует интерфейс базы данных (Client_rep_db) к интерфейсу
    Client_rep_base, позволяя работать с БД через общий интерфейс.
    """
    
    def __init__(self, db_repository: Client_rep_db):
        """
        Инициализирует адаптер с объектом репозитория БД.
        
        Args:
            db_repository: объект Client_rep_db для работы с базой данных
        """
        self.db_repository = db_repository
        # Инициализируем список (хотя БД не использует его напрямую)
        self._clients: List[Client] = []
    
    def _load_from_file(self) -> None:
        """
        Пустая реализация (не требуется для БД).
        
        БД не работает с файлами, поэтому этот метод остается пустым.
        """
        pass
    
    def _save_to_file(self) -> None:
        """
        Пустая реализация (не требуется для БД).
        
        БД не работает с файлами, поэтому этот метод остается пустым.
        """
        pass
    
    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Возвращает объект Client по ID, используя репозиторий БД.
        
        Args:
            client_id: уникальный идентификатор клиента
            
        Returns:
            Client объект или None
        """
        return self.db_repository.get_by_id(client_id)
    
    def add(self, client: Client) -> None:
        """
        Добавляет новый объект Client, используя репозиторий БД.
        
        Args:
            client: объект Client для добавления
        """
        self.db_repository.add(client)
    
    def replace_by_id(self, client_id: int, new_client: Client) -> None:
        """
        Заменяет объект Client по ID, используя репозиторий БД.
        
        Args:
            client_id: ID клиента для замены
            new_client: новый объект Client с новыми данными
        """
        self.db_repository.replace_by_id(client_id, new_client)
    
    def delete_by_id(self, client_id: int) -> None:
        """
        Удаляет объект Client по ID, используя репозиторий БД.
        
        Args:
            client_id: ID клиента для удаления
        """
        self.db_repository.delete_by_id(client_id)
    
    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort]:
        """
        Возвращает список из n объектов ClientShort для k-й страницы,
        используя репозиторий БД.
        
        Args:
            k: номер страницы (начиная с 1)
            n: размер страницы (количество элементов)
            
        Returns:
            Список объектов ClientShort размером до n элементов
        """
        return self.db_repository.get_k_n_short_list(k, n)
    
    def get_count(self) -> int:
        """
        Возвращает общее количество клиентов, используя репозиторий БД.
        
        Returns:
            int: количество клиентов
        """
        return self.db_repository.get_count()

