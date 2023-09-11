from classes import HeadHunterAPI, SuperJobAPI, Vacancy


# print(list_of_vacancis)
# print("jhgvbjkn")
# Сохранение информации о вакансиях в файл
# json_saver = JSONSaver() # Принимает путь до файла и если его нет, то создает новый
# json_saver.add_vacancy(vacancy)
# json_saver.save_to_file()
# json_saver.delete_vacancy(vacancy)
#
#

def get_by_filter(salary_from, salary_to, keywords):
    json_load = Load
    json_load = [item for item in json_load if item > salary_from and item < salary_to]
    for words in keywords:
        for item in json_load:
            if words in item.tasks:
                [].append()
                [] = list(set([]))


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    platforms = int(
        input("Выберите платформы, с которых хотите получить вакансии:\n1 - HH\n2 - SJ\n3 - обе платформы\n"))
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()

    def get_top_vacancies():
        list_of_vacancis = []
        hh_vacancies = hh_api.get_vacancies(search_query)
        superjob_vacancies = superjob_api.get_vacancies(search_query)
        if platforms == 1:
            for item_id, vacancy in hh_vacancies.items():
                list_of_vacancis.append(
                    Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                            vacancy["experience"],
                            vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями HH
        elif platforms == 2:
            for item_id, vacancy in superjob_vacancies.items():
                list_of_vacancis.append(
                    Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                            vacancy["experience"],
                            vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями SJ
        elif platforms == 3:
            for item_id, vacancy in {**superjob_vacancies, **hh_vacancies}.items():
                list_of_vacancis.append(
                    Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                            vacancy["experience"],
                            vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями обеих платформ

        return list_of_vacancis

    def sort_and_filter_top_vac(list_of_vacancis):
        list_of_vacancis = sorted(list_of_vacancis, key=lambda x: -float(x))
        vacs_set = set()
        for vac in list_of_vacancis:
            for word in filter_words:
                if word in vac.tasks.lower() or word in vac.name.lower():
                    vacs_set.add((vac.name, vac.url, float(vac)))
                else:
                    print("Нет вакансий, соответствующих заданным критериям.")
        print(vacs_set[:top_n])
        return vacs_set

    def print_vacancies():
        pass


if __name__ == "__main__":
    user_interaction()
