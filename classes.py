from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as BS
from typing import Any
import requests
import re


class Engine(ABC):
    def __init__(self, text: str, num_page: int):
        self._text = text
        self._num_page = num_page

    @property
    def text(self):
        return self._text

    @property
    def num_page(self):
        return self._num_page

    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):

    def get_request(self) -> list:
        """
        Получает данные с API и возвращает нужные поля.
        """
        par = {"text": self.text, 'area': '113', 'per_page': '100',
               'page': self.num_page}
        response = requests.get(f"https://api.hh.ru/vacancies", params=par)
        data = response.json()['items']
        return data


class Superjob(Engine):

    def get_request(self) -> list:
        """
        Парсит страницу через BS
        """
        par = {'keywords': self.text, 'page': self.num_page}
        url = f"https://russia.superjob.ru/vacancy/search/"
        r = requests.get(url, params=par)
        soup = BS(r.text, "html.parser")

        data = soup.find_all('div', class_='_8zbxf f-test-vacancy-item _3HN9U hi8Rr _3E2-y _1k9rz')
        return data


class Vacancy():

    def __init__(self, data: Any, website: str):
        self.data = data
        self.website = website

        self._title = self.set_title()
        self._salary = self.set_salary()
        self._url = self.set_url()
        self._description = self.set_descriptoin()

    @property
    def title(self):
        return self._title

    @property
    def salary(self):
        return self._salary

    @property
    def url(self):
        return self._url

    @property
    def description(self):
        return self._description

    def set_title(self) -> str:
        if self.website == "HH":
            return self.data['name']

        if self.website == "Superjob":
            return \
            self.data.contents[0].contents[0].contents[3].contents[0].contents[0].text

    def set_url(self) -> str:
        if self.website == "HH":
            return self.data['alternate_url']

        if self.website == "Superjob":
            urls = self.data.contents[0].contents[0].contents[3].a['href']
            return f"https://russia.superjob.ru{urls}"

    def set_salary(self) -> int:
        if self.website == "HH":
            salary = self.data['salary']
            if salary is None:
                return 0
            if salary['from'] is None:
                return 0
            if salary['currency'] == "USD":
                return salary['from'] * 60

            return salary['from']

        if self.website == "Superjob":
            salary = \
            self.data.contents[0].contents[0].contents[3].contents[0].contents[1].text
            res = re.compile("от | | до|до |руб.|\/месяц")
            salary = re.sub(res, "", salary)

            if "По договорённости" in salary:
                return 0
            elif "—" in salary:
                salary = salary.split("—")
                return int(salary[0])
            else:
                return int(salary)

    def set_descriptoin(self) -> str:
        if self.website == "HH":
            res = re.compile("<highlighttext>|<\/highlighttext>")
            if self.data['snippet']['responsibility'] is None:
                descript = re.sub(res, "", self.data['snippet']['requirement'])
                return descript
            if self.data['snippet']['requirement'] is None:
                descript = re.sub(res, "",
                                  self.data['snippet']['responsibility'])
                return descript
            description = f"{self.data['snippet']['responsibility']} " \
                          f"{self.data['snippet']['requirement']}"
            return re.sub(res, "", description)

        if self.website == "Superjob":
            return self.data.contents[0].contents[0].contents[5].text

    # def __repr__(self) -> str:
    #     return f"Вакансия: {self.title}.\n" \
    #            f"Уровень дохода: {self.salary}.\n" \
    #            f"Ссылка: {self.url}.\n" \
    #            f"Описание: {self.description}.\n"

