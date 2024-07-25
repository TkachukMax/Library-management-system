from pprint import pprint
from db_connection import DataBase
from books import Books

db = DataBase()

print("Library management systems")


def call_search(attribute):
    """
    Performs a search in the database based on the specified attribute and user input.

    Args:
        attribute (str): The attribute to search by (e.g., title, author, year).

    Returns:
        None: Prints the search results or a message if no results are found.
    """

    title = input('\nВвод для поиска:  ')
    fetch_description = True
    res = db.execute_sql_query(Books().search_object(attribute, title), fetch_description)

    if res:
        pprint(res)
    else:
        print("По данному запросу ничего не найдено")


def main_menu():
    """
        Displays the main menu and handles user input for various actions in the library management system.

        Returns:
            None
    """
    while True:
        ask = input('''\nВведите номер желаемого действия:
        1. Отобразить все книги,
        2. Поиск книги,
        3. Добавление книги,
        4. Удаление книги,
        5. Изменение статуса книги,
        6. Выйти.
        Поле ввода: ''')
        if ask == '1' or ask == 'Отобразить все книги':
            pprint(db.execute_sql_query(Books().show_all_object(), True))
            continue

        elif ask == '2' or ask == 'Поиск книги':
            while True:
                attr_ask = input('''\nВведите номер желаемого параметра поиска:
                1. Название,
                2. Автор, 
                3. Год издания.
                4. Назад
                Поле ввода: ''')

                if attr_ask == '1' or attr_ask == 'Название':
                    call_search("title")
                    break

                elif attr_ask == '2' or attr_ask == 'Автор':
                    call_search("author")
                    break

                elif attr_ask == '3' or attr_ask == 'Год издания':
                    call_search("year")
                    break

                elif attr_ask == '4' or attr_ask == 'Назад':
                    break

                else:
                    print('\nПоиск по данному параметру невозможен.')
                    continue

        elif ask == '3' or ask == 'Добавление книги':
            title = input('\nВведите название книги:')
            author = input('\nВведите фамилию автора:')
            year = input('\nВведите год издания в виде числа:')
            fetch_description = False
            db.execute_sql_query(Books().create_object(title, author, year), fetch_description)
            continue

        elif ask == '4' or ask == 'Удаление книги':
            object_id = input('\nВведите id книги:')
            fetch_description = True

            check = db.execute_sql_query(Books().presence_object_by_id(object_id), fetch_description)
            check_result = check[0]['exists']

            if check_result:
                fetch_description = False
                db.execute_sql_query(Books().delete_object(object_id), fetch_description)
            else:
                print('\n Книги с таким id нет в библиотеке')
            continue

        elif ask == '5' or ask == 'Изменение статуса книги':
            object_id = input('\nВведите id книги:')
            fetch_description = True

            check = db.execute_sql_query(Books().presence_object_by_id(object_id), fetch_description)
            check_result = check[0]['exists']

            if check_result:
                fetch_description = False
                status = input('\nВведите статус книги(в наличии/выдана):')

                if status == "в наличии" or status == "В наличии" or status == "выдана" or status == "Выдана":
                    db.execute_sql_query(Books().change_status(object_id, status), fetch_description)
                    continue
                else:
                    print("Неверно введён статус")
                    continue

            else:
                print('\n Книги с таким id нет в библиотеке')
                continue

        else:
            break


if __name__ == "__main__":
    main_menu()
