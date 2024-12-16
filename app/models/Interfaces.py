from abc import ABC, abstractmethod

class Add(ABC):
    @abstractmethod
    def add_product(self):
        pass

class Delete(ABC):
    @abstractmethod
    def delete_product(self):
        pass

class Buy(ABC):
    @abstractmethod
    def buy_product(self):
        pass

class Archive(ABC):
    @abstractmethod
    def archive_product(self):
        pass