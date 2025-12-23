from typing import Optional, List, Any
from src.repositories.client_rep_base import Client_rep_base
from src.models.client import Client, ClientShort


class Client_rep_file_decorator:
    """
    Декоратор для добавления фильтрации и сортировки к файловым репозиториям.

    Работает с любым репозиторием, наследуемым от Client_rep_base (JSON, YAML).
    Позволяет фильтровать и сортировать данные в памяти без изменения исходного кода.
    """

    def __init__(self, repo: Client_rep_base):
        """
        Инициализирует декоратор с файловым репозиторием.

        Args:
            repo: объект, наследуемый от Client_rep_base (JSON или YAML репозиторий)
        """
        self._repo = repo
        self._filter_attr: Optional[str] = None
        self._filter_value: Optional[Any] = None
        self._sort_attr: Optional[str] = None
        self._sort_reverse: bool = False

    def set_filter(self, attr_name: str, value: Any) -> 'Client_rep_file_decorator':
        """
        Устанавливает фильтр по атрибуту объекта Client.

        Args:
            attr_name: имя атрибута для фильтрации (например, 'city', 'last_name')
            value: значение для сравнения

        Returns:
            self для chain-вызовов
        """
        self._filter_attr = attr_name
        self._filter_value = value
        return self

    def set_sort(self, attr_name: str, reverse: bool = False) -> 'Client_rep_file_decorator':
        """
        Устанавливает сортировку по атрибуту объекта Client.

        Args:
            attr_name: имя атрибута для сортировки (например, 'last_name', 'total_spending')
            reverse: если True, сортировать в обратном порядке (DESC)

        Returns:
            self для chain-вызовов
        """
        self._sort_attr = attr_name
        self._sort_reverse = reverse
        return self

    def clear_filters(self) -> 'Client_rep_file_decorator':
        """
        Сбрасывает установленные фильтры.

        Returns:
            self для chain-вызовов
        """
        self._filter_attr = None
        self._filter_value = None
        return self

    def clear_sort(self) -> 'Client_rep_file_decorator':
        """
        Сбрасывает установленную сортировку.

        Returns:
            self для chain-вызовов
        """
        self._sort_attr = None
        self._sort_reverse = False
        return self

    def _get_filtered_clients(self) -> List[Client]:
        """
        Получает список клиентов с применением фильтра.

        Returns:
            Список объектов Client после применения фильтра
        """
        clients = list(self._repo._clients)

        # Применяем фильтр, если установлен
        if self._filter_attr is not None and self._filter_value is not None:
            clients = [
                client for client in clients
                if hasattr(client, self._filter_attr) and
                getattr(client, self._filter_attr) == self._filter_value
            ]

        return clients

    def _get_filtered_and_sorted_clients(self) -> List[Client]:
        """
        Получает список клиентов с применением фильтра и сортировки.

        Returns:
            Список объектов Client после применения фильтра и сортировки
        """
        clients = self._get_filtered_clients()

        # Применяем сортировку, если установлена
        if self._sort_attr is not None:
            try:
                clients.sort(
                    key=lambda c: getattr(c, self._sort_attr),
                    reverse=self._sort_reverse
                )
            except AttributeError as e:
                print(f"Ошибка при сортировке: атрибут '{self._sort_attr}' не найден. {e}")

        return clients

    def get_k_n_short_list(self, k: int, n: int) -> List[ClientShort]:
        """
        Возвращает отфильтрованный и отсортированный список ClientShort для k-й страницы.

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

        # Получаем отфильтрованный и отсортированный список
        filtered_sorted_clients = self._get_filtered_and_sorted_clients()

        # Применяем пагинацию
        start_idx = (k - 1) * n
        end_idx = start_idx + n
        page_clients = filtered_sorted_clients[start_idx:end_idx]

        # Преобразуем в ClientShort
        return [ClientShort(client) for client in page_clients]

    def get_count(self) -> int:
        """
        Возвращает количество клиентов ПОСЛЕ применения фильтров.

        Returns:
            int: количество отфильтрованных клиентов
        """
        filtered_clients = self._get_filtered_clients()
        return len(filtered_clients)

    # Методы-делегаты

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

    def sort_by_field(self, field_name: str) -> None:
        """
        Сортирует репозиторий по указанному полю.

        Args:
            field_name: имя поля для сортировки
        """
        self._repo.sort_by_field(field_name)
