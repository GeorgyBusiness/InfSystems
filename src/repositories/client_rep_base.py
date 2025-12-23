from abc import ABC, abstractmethod
import os
from typing import Optional, List
from src.models.client import Client, ClientShort
from src.mvc.observer import Subject


class Client_rep_base(Subject, ABC):
    """
    Абстрактный базовый класс для управления коллекцией объектов Client.

    Содержит общую логику CRUD операций, сортировки и постраничной выдачи.
    Подклассы должны реализовать методы _load_from_file и _save_to_file
    для работы с конкретными форматами (JSON, YAML и т.д.).
    """

    def __init__(self, file_path: Optional[str] = None):
        """
        Инициализирует репозиторий с путем к файлу.

        Args:
            file_path: путь к файлу для хранения данных (опционально, для адаптеров БД)
        """
        super().__init__()
        self.file_path = file_path
        self._clients: List[Client] = []
        if file_path is not None:
            self._load_from_file()

    @abstractmethod
    def _load_from_file(self) -> None:
        """
        Загружает данные из файла в приватный список _clients.

        Должна быть реализована в подклассе для работы с конкретным форматом.
        """
        pass

    @abstractmethod
    def _save_to_file(self) -> None:
        """
        Сохраняет всю коллекцию _clients в файл.

        Должна быть реализована в подклассе для работы с конкретным форматом.
        """
        pass

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

        Для файловых репозиториев генерирует новый ID вычислением
        (максимальный существующий ID + 1). Для БД репозиториев (adapter)
        этот метод не вызывается напрямую, вместо этого используется
        Client_rep_db.add() который получает ID через RETURNING.

        Args:
            client: объект Client для добавления
        """
        if self._clients:
            # Находим максимальный ID в списке
            max_id = max(c.id for c in self._clients)
            client.id = max_id + 1
        else:
            # Если список пуст, начиная с ID = 1
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
