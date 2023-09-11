from classes import HeadHunterAPI, SuperJobAPI, Vacancy


# Создание экземпляра класса для работы с API сайтов с вакансиями


# print(list_of_vacancis)
# print("jhgvbjkn")
# Сохранение информации о вакансиях в файл
# json_saver = JSONSaver() # Принимает путь до файла и если его нет, то создает новый
# json_saver.add_vacancy(vacancy)
# json_saver.save_to_file()
# json_saver.delete_vacancy(vacancy)
#
#
def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    platforms = int(input("Выберите платформы, с которых хотите получить вакансии:\n1 - HH\n2 - SJ\n3 - обе платформы\n"))
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    list_of_vacancis = []
    hh_vacancies = hh_api.get_vacancies(search_query)
    superjob_vacancies = superjob_api.get_vacancies(search_query)
    if platforms == 1:
        for item_id, vacancy in hh_vacancies.items():
            list_of_vacancis.append(
                Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                        vacancy["experience"], vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями HH
    elif platforms == 2:
        for item_id, vacancy in superjob_vacancies.items():
            list_of_vacancis.append(
                Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                        vacancy["experience"], vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями SJ
    elif platforms == 3:
        for item_id, vacancy in {**superjob_vacancies, **hh_vacancies}.items():
            list_of_vacancis.append(
                Vacancy(item_id, vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"],
                        vacancy["experience"], vacancy["tasks"]))  # Создание экземпляров класса для работы с вакансиями обеих платформ
    sorted(list_of_vacancis, key=lambda x: x.__float__)
    print(list_of_vacancis[0].__dict__)




    # filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
    #
    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return
    #
    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)
    #

if __name__ == "__main__":
    user_interaction()
