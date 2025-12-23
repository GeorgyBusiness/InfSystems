import json
import os
from typing import Optional, List
from src.client import Client, ClientShort


class Client_rep_json:
    """
    Класс для управления коллекцией объектов Client с сохранением в JSON формате.
    
    Предоставляет операции чтения, создания, обновления и удаления объектов,
    а также функции сортировки и постраничной выдачи данных.
    """
    
    def __init__(self, file_path: str):
        """
        Инициализирует репозиторий с путем к JSON файлу.
        
        Args:
            file_path: путь к JSON файлу для хранения данных
        """
        self.file_path = file_path
        self._clients: List[Client] = []
        self._load_from_file()
    
    def _load_from_file(self) -> None:
        """
        Загружает данные из JSON файла в приватный список _clients.
        
        Если файл не найден или пуст, инициализирует пустой список.
        """
        if not os.path.exists(self.file_path):
            self._clients = []
            return
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    self._clients = []
                    return
                
                data = json.loads(content)
                self._clients = []
                
                if isinstance(data, list):
                    for client_dict in data:
                        try:
                            client = Client(**client_dict)
                            self._clients.append(client)
                        except (ValueError, TypeError) as e:
                            print(f"Ошибка при загрузке клиента: {e}")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при чтении файла {self.file_path}: {e}")
            self._clients = []
    
    def _save_to_file(self) -> None:
        """
        Сохраняет всю коллекцию _clients в JSON файл.
        
        Преобразует объекты Client в словари перед сохранением.
        """
        clients_data = []
        for client in self._clients:
            client_dict = {
                'id': client.id,
                'last_name': client.last_name,
                'first_name': client.first_name,
                'patronymic': client.patronymic,
                'phone': client.phone,
                'email': client.email,
                'passport_series': client.passport_series,
                'passport_number': client.passport_number,
                'zip_code': client.zip_code,
                'city': client.city,
                'street': client.street,
                'house': client.house,
                'total_spending': client.total_spending,
            }
            clients_data.append(client_dict)
        
        try:
            os.makedirs(os.path.dirname(self.file_path) or '.', exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(clients_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка при сохранении в файл {self.file_path}: {e}")
    
    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Возвращает объект Client по ID или None, если не найден.
        
        Args:
            client_id: уникальный идентификатор клиента
            
        Returns:
            Client объект или None
        """
        for client in self._clients:
            if client.id == client_id:
                return client
        return None
    
    def add(self, client: Client) -> None:
        """
        Добавляет новый объект Client в список.
        
        Генерирует новый ID (максимальный существующий + 1),
        устанавливает его объекту и сохраняет в файл.
        
        Args:
            client: объект Client для добавления
        """
        if self._clients:
            max_id = max(c.id for c in self._clients)
            client.id = max_id + 1
        else:
            client.id = 1
        
        self._clients.append(client)
        self._save_to_file()
    
    def replace_by_id(self, client_id: int, new_client: Client) -> None:
        """
        Заменяет объект Client по ID на новый объект.
        
        Находит объект по ID и заменяет его данные новым объектом,
        сохраняет в файл.
        
        Args:
            client_id: ID клиента для замены
            new_client: новый объект Client с новыми данными
            
        Raises:
            ValueError: если клиент с указанным ID не найден
        """
        for i, client in enumerate(self._clients):
            if client.id == client_id:
                new_client.id = client_id
                self._clients[i] = new_client
                self._save_to_file()
                return
        
        raise ValueError(f"Клиент с ID {client_id} не найден")
    
    def delete_by_id(self, client_id: int) -> None:
        """
        Удаляет объект Client по ID и обновляет файл.
        
        Args:
            client_id: ID клиента для удаления
            
        Raises:
            ValueError: если клиент с указанным ID не найден
        """
        for i, client in enumerate(self._clients):
            if client.id == client_id:
                self._clients.pop(i)
                self._save_to_file()
                return
        
        raise ValueError(f"Клиент с ID {client_id} не найден")
    
    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort]:
        """
        Возвращает список из n объектов класса ClientShort для k-й страницы.
        
        Например, если k=2, n=10, вернет элементы с индексом 10 по 19.
        
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
        
        start_idx = (k - 1) * n
        end_idx = start_idx + n
        
        page_clients = self._clients[start_idx:end_idx]
        return [ClientShort(client) for client in page_clients]
    
    def sort_by_field(self, field_name: str) -> None:
        """
        Сортирует список _clients по указанному полю и сохраняет порядок в файл.
        
        Args:
            field_name: имя поля для сортировки (например, 'last_name')
            
        Raises:
            ValueError: если поле не существует в объекте Client
        """
        # Проверяем, что поле существует
        if not self._clients:
            return
        
        if not hasattr(self._clients[0], field_name):
            raise ValueError(
                f"Поле '{field_name}' не найдено в объекте Client. "
                f"Доступные поля: id, last_name, first_name, patronymic, phone, email, "
                f"passport_series, passport_number, zip_code, city, street, house, total_spending"
            )
        
        self._clients.sort(key=lambda client: getattr(client, field_name))
        self._save_to_file()
    
    def get_count(self) -> int:
        """
        Возвращает общее количество клиентов в списке.
        
        Returns:
            int: количество клиентов
        """
        return len(self._clients)

