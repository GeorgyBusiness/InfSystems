import yaml
import os
from src.repositories.client_rep_base import Client_rep_base
from src.models.client import Client


class Client_rep_yaml(Client_rep_base):
    """
    Класс для управления коллекцией объектов Client с сохранением в YAML формате.

    Наследует общую логику от Client_rep_base и реализует специфичные методы
    для работы с YAML.
    """

    def _load_from_file(self) -> None:
        """
        Загружает данные из YAML файла в приватный список _clients.

        Если файл не найден или пуст, инициализирует пустой список.
        """
        if not os.path.exists(self.file_path):
            self._clients = []
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self._clients = []

                if data is None:
                    return

                if isinstance(data, list):
                    for client_dict in data:
                        try:
                            client = Client(**client_dict)
                            self._clients.append(client)
                        except (ValueError, TypeError) as e:
                            print(f"Ошибка при загрузке клиента: {e}")
        except (yaml.YAMLError, IOError) as e:
            print(f"Ошибка при чтении файла {self.file_path}: {e}")
            self._clients = []

    def _save_to_file(self) -> None:
        """
        Сохраняет всю коллекцию _clients в YAML файл.

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
                yaml.dump(clients_data, f, allow_unicode=True, sort_keys=False)
        except IOError as e:
            print(f"Ошибка при сохранении в файл {self.file_path}: {e}")
