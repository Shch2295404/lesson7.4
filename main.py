from selenium import webdriver  # Импортируем библиотеку для работы с Selenium WebDriver
from selenium.webdriver.firefox.service import Service  # Импортируем Service для настройки WebDriver
from selenium.webdriver.firefox.options import Options  # Импортируем Options для настройки параметров WebDriver
from selenium.webdriver.common.by import By  # Импортируем By для выбора элементов на странице


def initialize_driver():
    """
    Инициализирует Selenium WebDriver с использованием Firefox.
    """
    geckodriver_path = 'C:/Users/geckodriver/geckodriver.exe'  # Путь к geckodriver
    service = Service(geckodriver_path)  # Создаем объект Service для geckodriver
    options = Options()  # Настраиваем параметры WebDriver
    options.headless = True  # Включаем режим без отображения окна браузера
    options.add_argument('--headless')  # Дублируем параметр headless
    options.add_argument('--disable-gpu')  # Отключаем использование GPU
    options.add_argument('--window-size=1920,1080')  # Устанавливаем размер окна браузера
    driver = webdriver.Firefox(service=service, options=options)  # Создаем объект WebDriver
    return driver  # Возвращаем объект драйвера


def search_wikipedia(driver, query):
    """
    Выполняет поиск статьи в Википедии по указанному запросу.

    :param driver: Объект WebDriver.
    :param query: Запрос для поиска в Википедии.
    :return: Обновленный объект WebDriver или None, если статья не найдена.
    """
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"  # Формируем URL-адрес статьи
    driver.get(url)  # Загружаем страницу
    if "Википедия не имеет статьи с таким названием" in driver.page_source:  # Проверяем наличие статьи
        return None
    return driver


def list_paragraphs(driver):
    """
    Выводит параграфы текущей статьи, по одному за раз.

    :param driver: Объект WebDriver.
    """
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")  # Находим все элементы <p>
    for para in paragraphs:
        print(para.text[:500] + '...')  # Выводим первые 500 символов текста
        input("Нажмите Enter для продолжения...\n")  # Ожидаем действия пользователя


def list_links(driver):
    """
    Выводит связанные страницы, указанные в разделе "hatnote" статьи.

    :param driver: Объект WebDriver.
    """
    links = []  # Список для хранения связанных страниц
    for element in driver.find_elements(By.TAG_NAME, "div"):  # Находим все элементы <div>
        cl = element.get_attribute("class")  # Получаем класс элемента
        if cl == "hatnote navigation-not-searchable":  # Проверяем класс элемента
            links.append(element)  # Добавляем элемент в список

    for link in links:
        print(link.text)  # Выводим текст ссылок


def main():
    """
    Основная функция программы, запускает работу с Selenium и взаимодействие с пользователем.
    """
    driver = initialize_driver()  # Инициализируем WebDriver

    query = input("Введите запрос: ")  # Получаем запрос от пользователя

    driver = search_wikipedia(driver, query)  # Выполняем поиск статьи
    if not driver:  # Если статья не найдена
        print("Страница не найдена.")
        return

    while True:
        # Выводим меню действий
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        choice = input("Введите номер действия: ")  # Получаем выбор пользователя

        if choice == '1':
            list_paragraphs(driver)  # Выводим параграфы
        elif choice == '2':
            print("Связанные страницы:")
            list_links(driver)  # Выводим связанные страницы
            new_query = input("Введите название связанной страницы: ")  # Получаем новый запрос
            driver = search_wikipedia(driver, new_query)  # Переходим на новую страницу
            if not driver:  # Если новая страница не найдена
                print("Страница не найдена.")
                return
        elif choice == '3':
            print("Выход из программы.")  # Завершаем программу
            break
        else:
            print("Неправильный выбор. Пожалуйста, попробуйте снова.")  # Обрабатываем неверный ввод

    driver.quit()  # Закрываем WebDriver


if __name__ == "__main__":
    main()  # Запускаем основную функцию, если скрипт запущен напрямую
