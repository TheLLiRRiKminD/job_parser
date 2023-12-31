import json
from abc import ABC, abstractmethod

import requests, os
from dotenv import load_dotenv

load_dotenv()


class API_Connect(ABC):

    @abstractmethod
    def __init__(self, vacancies_url: str):
        self.vacancies_url = vacancies_url

    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass


class Saver(ABC):

    @abstractmethod
    def __init__(self, name_of_file):
        self.name_of_file = name_of_file

    @abstractmethod
    def save_to_file(self):
        pass


class HeadHunterAPI(API_Connect):
    """
    Получает ключевое слово и делает запрос по API на площадку для поиска работы
    """

    def __init__(self):
        self.vacancies_url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self, keyword: str):
        params = {
            "text": keyword,
            "per_page": 20,
        }
        response_HH = requests.get(self.vacancies_url, params=params)
        ids_HH = [item["id"] for item in response_HH.json()["items"]]
        dict_vacancies = {}
        for item_id in ids_HH:
            get_vac = requests.get(f"{self.vacancies_url}{item_id}").json()
            if get_vac["salary"] is None:
                salary_from = None
                salary_to = None
            else:
                salary_from = get_vac["salary"]["from"]
                salary_to = get_vac["salary"]["to"]
            dict_vacancies[item_id] = {"name": get_vac["name"], "salary from": salary_from,
                                       "salary to": salary_to, "url": get_vac["alternate_url"],
                                       "experience": get_vac["experience"]['name'], "tasks": get_vac["description"]}
        return dict_vacancies


class SuperJobAPI(API_Connect):

    def __init__(self):
        self.vacancies_url = "https://api.superjob.ru/2.0/vacancies/"

    def get_vacancies(self, keyword: str):
        params = {
            "keyword": keyword,
            "count": 20,
        }
        headers = {
            "X-Api-App-Id": os.getenv("SJ_API"),
            "Authorization": os.getenv("Authorization"),
            "Content-Type": os.getenv("Content-Type"),
        }
        response_SJ = requests.get(self.vacancies_url, params=params, headers=headers)
        ids_SJ = [item["id"] for item in response_SJ.json()["objects"]]
        dict_vacancies = {}
        for item_id in ids_SJ:
            get_vac = requests.get(f"{self.vacancies_url}{item_id}", headers=headers).json()
            dict_vacancies[item_id] = {"name": get_vac["profession"], "salary from": get_vac["payment_from"],
                                       "salary to": get_vac["payment_to"], "url": get_vac["link"],
                                       "experience": get_vac["experience"]["title"],
                                       "tasks": get_vac["vacancyRichText"]}
        return dict_vacancies


class Vacancy:

    def __init__(self, id_vac: int, name: str, url: str, salary_from: int, salary_to: int, experience: str, tasks: str):
        try:
            self.id_vac = id_vac
            self.name = name
            self.url = url
            self.salary_from = salary_from
            self.salary_to = salary_to
            self.experience = experience
            self.tasks = tasks
        except IndexError:
            self.name = None
            self.url = None
            self.salary_from = None
            self.salary_to = None
            self.experience = None
            self.tasks = None

    def __float__(self):
        self.salary_to = None if not self.salary_to else self.salary_to
        self.salary_from = None if not self.salary_from else self.salary_from
        if self.salary_from is not None and self.salary_to is not None:
            return float((self.salary_from + self.salary_to) / 2)
        elif self.salary_from is not None and self.salary_to is None:
            return float(self.salary_from)
        elif self.salary_from is None and self.salary_to is not None:
            return float(self.salary_to)
        else:
            return 0.0

    def __ge__(self, other):
        if isinstance(other, Vacancy):
            return float(self) >= float(other)
        elif isinstance(other, int):
            return float(self) >= other
        else:
            raise ValueError("Несравниваемые объекты")

    def __le__(self, other):
        if isinstance(other, Vacancy):
            return float(self) <= float(other)
        elif isinstance(other, int):
            return float(self) <= other
        else:
            raise ValueError("Несравниваемые объекты")

    def to_dict(self):
        return {'name': self.name,"url": self.url,"salary": self.__float__(),
                "experience": self.experience,"tasks": self.tasks}


class JSONSaver(Saver):
    """Создает файл с ключевым словом вакансии"""

    def __init__(self, name_of_file):
        self.name_of_file = name_of_file

    def save_to_file(self, list_of_vacancies):
        list_of_dicts = [vac.to_dict() for vac in list_of_vacancies]
        try:
            content = json.loads(f"{self.name_of_file}.json")
        except json.decoder.JSONDecodeError:
            content = []
        content += list_of_dicts
        with open(f"{self.name_of_file}.json", "a",) as outfile:
            json.dump(list_of_dicts, outfile)
            print("Запись в файл прошла успешно")
