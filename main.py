from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import time
import os
import pandas


def find_for_coin_by_name(name, coins, prices, market_caps):
    for item in coins:
        if item == name:
            index_for_searching = coins.index(item)
            price = prices[index_for_searching]
            market_cap = market_caps[index_for_searching]
            print(f"Найдено: {name} - {price} - {market_cap}")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    cls()
    while True:
        pages = int(input("Введите кол-во страниц: "))
        if pages > 0:
            break
        else:
            print("Строго больше нуля")
            time.sleep(0.5)
            cls()
    options = webdriver.EdgeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    service = Service('./msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=options)
    try:
        driver.get("https://coinmarketcap.com/?page=1")
    except Exception:
        print("Страница не найдена")
        return 0
    cls()
    list_of_files = []
    page = 1
    print("Парсинг HTML кода...")
    while page != (pages + 1):
        cls()
        for scroll_px in range(100, 2600, 400):
            ActionChains(driver).scroll(0, 0, 0, scroll_px).perform()
            time.sleep(0.1)
        with open(f"./data/page-{page}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        list_of_files.append(f"./data/page-{page}.html")
        page += 1
        try:
            driver.get(f"https://coinmarketcap.com" + f"/?page={page}")
        except Exception as e:
            print(f"Страница {page} не найдена")
            return 0

    driver.quit()
    print("Анализ данных...")
    list_of_coins_name = []
    list_of_coins_price = []
    list_of_coins_market_cap = []
    for number in list_of_files:
        with open(number, encoding="utf-8") as file:
            src = file.read()
            soup = BeautifulSoup(src, "lxml")
            list_of_coins = soup.find("tbody").find_all("tr")
            for coin in list_of_coins:
                if coin.find_all("td")[1].find("p") is None:
                    continue
                if coin.find_all("td")[2].find("p") is None:
                    continue
                if coin.find_all("td")[3].find("span") is None:
                    continue
                if coin.find_all("td")[6].find("p") is None:
                    continue
                index = coin.find_all("td")[1].find("p").text
                name = coin.find_all("td")[2].find("p").text
                price = coin.find_all("td")[3].find("span").text
                market_cap = coin.find_all("td")[6].find("p").find_all("span")[-1].text
                list_of_coins_name.append(name)
                list_of_coins_price.append(price)
                list_of_coins_market_cap.append(market_cap)

    for file in list_of_files:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
        os.remove(path)
    cls()
    coins_dict = {'Name': list_of_coins_name, 'Price': list_of_coins_price, 'Market cap': list_of_coins_market_cap}
    try:
        data_frame = pandas.DataFrame(coins_dict)
        data_frame.to_csv('data.csv')
    except Exception:
        print("Ошибка, при создании файла")
    else:
        print("Файл с данными создан")
    while True:
        cls()
        print(f"Всего записей {len(list_of_coins_name)}")
        print(f"1. Поиск по названию")
        print(f"2. Вывод криптовалют")
        print(f"0. Выход")
        command = int(input("Command: "))
        if command == 1:
            cls()
            name_for_find = input("Введите название криптовалюты: ")
            if name_for_find not in list_of_coins_name:
                print("Ошибка! Этого коина нет в списке")
                time.sleep(0.5)
                continue
            find_for_coin_by_name(name_for_find, list_of_coins_name, list_of_coins_price, list_of_coins_market_cap)
            temp = input("Нажмите Enter для выхода")
        elif command == 2:
            cls()
            print("Name - Price - Market cap")
            for item in range(len(list_of_coins_name)):
                print(f"{item + 1} - {list_of_coins_name[item]} - {list_of_coins_price[item]} - {list_of_coins_market_cap[item]}")
            temp = input("Нажмите Enter для выхода")
        elif command == 0:
            return 0
        else:
            continue


if __name__ == '__main__':
    main()
