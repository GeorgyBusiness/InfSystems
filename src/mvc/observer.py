"""
Паттерн Observer для поддержки Publish-Subscribe между репозиторием и представлением.
"""

from abc import ABC, abstractmethod
from typing import Any, List


class AbstractObserver(ABC):
    """
    Абстрактный класс Наблюдателя (Observer).
    
    Определяет интерфейс для всех конкретных наблюдателей,
    которые должны реагировать на уведомления от Subject.
    """
    
    @abstractmethod
    def update(self, data: Any) -> None:
        """
        Вызывается Subject для уведомления наблюдателя об изменении состояния.
        
        Args:
            data: Данные об изменении (может быть любой тип)
        """
        pass


class Subject:
    """
    Издатель (Subject) - класс, за которым наблюдают.
    
    Поддерживает список зарегистрированных наблюдателей
    и уведомляет их об изменениях состояния.
    """
    
    def __init__(self) -> None:
        """Инициализирует пустой список наблюдателей."""
        self._observers: List[AbstractObserver] = []
    
    def add_observer(self, observer: AbstractObserver) -> None:
        """
        Регистрирует наблюдателя.
        
        Args:
            observer: Объект, реализующий интерфейс AbstractObserver
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer: AbstractObserver) -> None:
        """
        Удаляет наблюдателя из списка.
        
        Args:
            observer: Объект для удаления
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, data: Any) -> None:
        """
        Уведомляет всех наблюдателей об изменении состояния.
        
        Args:
            data: Данные для передачи наблюдателям
        """
        for observer in self._observers:
            observer.update(data)

