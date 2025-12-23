from typing import Optional, List, Dict, Any, Tuple
from src.repositories.client_rep_db import Client_rep_db
from src.models.client import Client, ClientShort


class Client_rep_db_decorator:
    """
    Декоратор для добавления фильтрации и сортировки к репозиторию БД.
    
    Позволяет строить динамические SQL-запросы с фильтрами и сортировкой,
    не изменяя исходный код Client_rep_db. Использует паттерн Decorator.
    """
    
    def __init__(self, repo: Client_rep_db):
        """
        Инициализирует декоратор с объектом репозитория БД.
        
        Args:
            repo: объект Client_rep_db для работы с БД
        """
        self._repo = repo
        self._filters: Dict[str, Any] = {}
        self._sort_field: Optional[str] = None
        self._sort_order: str = 'ASC'
    
    def set_filter(self, field: str, value: Any) -> 'Client_rep_db_decorator':
        """
        Устанавливает фильтр для поля.
        
        Args:
            field: имя поля для фильтрации
            value: значение для фильтрации
            
        Returns:
            self для chain-вызовов
        """
        self._filters[field] = value
        return self
    
    def set_sort(self, field: str, order: str = 'ASC') -> 'Client_rep_db_decorator':
        """
        Устанавливает поле и направление сортировки.
        
        Args:
            field: имя поля для сортировки
            order: направление сортировки ('ASC' или 'DESC')
            
        Returns:
            self для chain-вызовов
        """
        if order.upper() not in ('ASC', 'DESC'):
            raise ValueError("order должен быть 'ASC' или 'DESC'")
        self._sort_field = field
        self._sort_order = order.upper()
        return self
    
    def clear_filters(self) -> 'Client_rep_db_decorator':
        """
        Сбрасывает все установленные фильтры.
        
        Returns:
            self для chain-вызовов
        """
        self._filters = {}
        return self
    
    def clear_sort(self) -> 'Client_rep_db_decorator':
        """
        Сбрасывает сортировку.
        
        Returns:
            self для chain-вызовов
        """
        self._sort_field = None
        self._sort_order = 'ASC'
        return self
    
    def _build_where_clause(self) -> Tuple[str, Tuple]:
        """
        Строит WHERE клаузу на основе установленных фильтров.
        
        Returns:
            Кортеж (where_clause, params) где where_clause - SQL фрагмент,
            а params - параметры для подстановки
        """
        if not self._filters:
            return '', ()
        
        where_parts = []
        params = []
        
        for field, value in self._filters.items():
            where_parts.append(f"{field} = %s")
            params.append(value)
        
        where_clause = " WHERE " + " AND ".join(where_parts)
        return where_clause, tuple(params)
    
    def _build_order_clause(self) -> str:
        """
        Строит ORDER BY клаузу на основе установленной сортировки.
        
        Returns:
            SQL фрагмент с ORDER BY или пустая строка
        """
        if self._sort_field is None:
            return ""
        
        return f" ORDER BY {self._sort_field} {self._sort_order}"
    
    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort]:
        """
        Возвращает отфильтрованный и отсортированный список ClientShort.
        
        Строит динамический SQL-запрос с учетом фильтров и сортировки.
        
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
        
        # Строим SQL запрос
        sql = "SELECT * FROM clients"
        where_clause, where_params = self._build_where_clause()
        sql += where_clause
        sql += self._build_order_clause()
        sql += " LIMIT %s OFFSET %s"
        
        # Параметры включают где-фильтры и пагинацию
        params = where_params + (n, offset)
        
        try:
            rows = self._repo.db_manager.execute_query(sql, params, fetch=True)
            
            if not rows:
                return []
            
            clients = []
            for row in rows:
                row = dict(row)
                row['total_spending'] = float(row['total_spending'])
                clients.append(Client(**row))
            return [ClientShort(client) for client in clients]
        except Exception as e:
            print(f"Ошибка при получении отфильтрованного списка клиентов: {e}")
            return []
    
    def get_count(self) -> int:
        """
        Возвращает количество отфильтрованных клиентов.
        
        Returns:
            int: количество клиентов, соответствующих фильтрам
        """
        # Строим SQL запрос
        sql = "SELECT COUNT(*) as count FROM clients"
        where_clause, where_params = self._build_where_clause()
        sql += where_clause
        
        try:
            result = self._repo.db_manager.execute_query_single(sql, where_params)
            return result['count'] if result else 0
        except Exception as e:
            print(f"Ошибка при подсчете отфильтрованных клиентов: {e}")
            return 0
    
    # Методы, которые просто перенаправляют в репозиторий
    
    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Возвращает объект Client по ID.
        
        Args:
            client_id: уникальный идентификатор клиента
            
        Returns:
            Client объект или None
        """
        return self._repo.get_by_id(client_id)
    
    def add(self, client: Client) -> None:
        """
        Добавляет новый объект Client.
        
        Args:
            client: объект Client для добавления
        """
        self._repo.add(client)
    
    def replace_by_id(self, client_id: int, new_client: Client) -> None:
        """
        Заменяет объект Client по ID.
        
        Args:
            client_id: ID клиента для замены
            new_client: новый объект Client с новыми данными
        """
        self._repo.replace_by_id(client_id, new_client)
    
    def delete_by_id(self, client_id: int) -> None:
        """
        Удаляет объект Client по ID.
        
        Args:
            client_id: ID клиента для удаления
        """
        self._repo.delete_by_id(client_id)

