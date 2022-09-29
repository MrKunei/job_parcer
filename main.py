from utils import *
from random import choices

def main() -> None:
    print("Привет! Найдем подходящую вакансию вместе на сайтах HH и Superjob!")
    job = input("Введите название профессии:\n>>> ")
    print("Отлично, начинаем поиск. Можем вместе наблюдать как обрабатываются данные")
    cleaning_json_file(job)

    print("Начинаем парсить сайт HH")
    parcing_page(job, HH, "HH")

    print("Начинаем парсить сайт Superjob")
    parcing_page(job, Superjob, "Superjob")

    data = read_json_file(job)
    print(f"Сбор данных закончен!\nВсего было найдено {len(data)} вакансий.\n")

    while True:
        print("Выберите № дальнейшего действия:\n"
              "1. Вывести топ 10 вакансий с самыми большими зарплатами.\n"
              "2. Вывести первые 20 вакансий.\n"
              "3. Вывести случайные 15 вакансий.\n"
              "4. Выйти.")
        user = int(input(">>> "))
        if user == 1:
            res = sorted(data, key=lambda v: v['salary'], reverse=True)[:10]
            print_info(res)

        if user == 2:
            res = data[:20]
            print_info(res)

        if user == 3:
            res = choices(data, k=15)
            print_info(res)

        if user == 4:
            break


def print_info(res) -> None:
    for r in res:
        print(f"Вакансия: {r['title']}\n"
              f"Ссылка: {r['urls']}\n"
              f"Уровень дохода: {r['salary']} руб.\n"
              f"Описание: {r['description']}\n")


if __name__ == '__main__':
    main()




