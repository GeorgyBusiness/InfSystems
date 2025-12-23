import json
import os
from src.repositories.client_rep_base import Client_rep_base
from src.models.client import Client


class Client_rep_json(Client_rep_base):
    """
    Класс для управления коллекцией объектов Client с сохранением в JSON формате.
    
    Наследует общую логику от Client_rep_base и реализует специфичные методы
    для работы с JSON.
    """
    
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

