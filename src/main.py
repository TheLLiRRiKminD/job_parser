from classes import HeadHunterAPI, SuperJobAPI, Vacancy,JSONSaverad


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()

# Получение вакансий с разных платформ
hh_vacancies = hh_api.get_vacancies("Python")
superjob_vacancies = superjob_api.get_vacancies("Python")

# Создание экземпляров класса для работы с вакансиями
list_of_vacancis = []
for item_id, vacancy in {**superjob_vacancies, **hh_vacancies}.items():
    list_of_vacancis.append(Vacancy(vacancy["name"], vacancy["url"], vacancy["salary from"], vacancy["salary to"], vacancy["experience"]))
print(list_of_vacancis)
print("jhgvbjkn")
# Сохранение информации о вакансиях в файл
json_saver = JSONSaver() # Принимает путь до файла и если его нет, то создает новый
json_saver.add_vacancy(vacancy)
json_saver.get_vacancies_by_salary("100 000-150 000 руб.") # передавать словарь
json_saver.save_to_file()
json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()


if __name__ == "__main__":
    hh_api.get_vacancies("Python")