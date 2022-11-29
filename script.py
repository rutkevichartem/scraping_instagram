from selenium import webdriver
from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
from vhod import username, password, username1, password1, username2, password2, username3, password3
import time
import random
from selenium.common.exceptions import NoSuchElementException
import os


class InstagramBot:
    def __init__(self):
        # вы также можете импортировать SoftwareEngine, HardwareType, SoftwareType, Popularity из random_user_agent.params
        # вы также можете установить необходимое количество пользовательских агентов, указав `limit` в качестве параметра
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=120)
        # Получить случайную строку пользовательского агента.
        user_agent = user_agent_rotator.get_random_user_agent()
        # options
        options = webdriver.ChromeOptions()
        # отключение вебдрайвера для инстаграм
        options.add_argument("start-maximized")
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(executable_path=r'..\chromedriver\chromedriver.exe', options=options)
        # self.browser.delete_all_cookies()
        self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        stealth(
            self.browser,
            user_agent=user_agent,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=False
        )

    def test(self):
        browser = self.browser
        browser.get("https://bot.sannysoft.com/")

    # метод для закрытия браузера
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # метод авторизации
    def login(self, username, password):
        browser = self.browser
        browser.get('https://www.instagram.com')
        print('Идет авторизация в инстаграме...')
        time.sleep(random.randrange(2, 5))

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(random.randrange(2, 5))

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random.randrange(4, 8))

        password_input.send_keys(Keys.ENTER)
        time.sleep(random.randrange(8, 12))

    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # метод собирает количество подписчиков, аватарка, последние 20 постов пользователя
    def get_followers_ava_posts(self, *userpages):
        browser = self.browser
        count_ac = 0
        for userpage in userpages:
            file_name = userpage.split("/")[-1]
            count_ac += 1
            print(f'Переходим по ссылке на аккаунт {count_ac}.')
            browser.get(userpage)
            time.sleep(random.randrange(3, 5))
            for request in browser.requests:
                if request.response:
                    print(
                        request.url,
                        request.response.status_code,
                        request.response.headers['Content-Type']
                    )
            try:
                # проверка на существование аккаунта и закрытость
                wrong_userpage = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/h2"
                if self.xpath_exists(wrong_userpage):
                    print(f"Такого аккаунта {count_ac}: {file_name} не существует, проверьте URL\n")
                else:
                    # создаём папку с именем пользователя
                    if os.path.exists(f"{file_name}"):
                        print(f"Папка аккаунта {count_ac}: {file_name} у нас уже существует, сохраняем новые данные!")
                    else:
                        print(f"Создаём папку аккаунта {count_ac}: {file_name} и сохраняем данные.")
                        os.mkdir(file_name)

                    private_user = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/div/article/div[1]/div/h2"
                    if self.xpath_exists(private_user):
                        print(f'{file_name} - приватный аккаунт, сохраняем аватар')
                        ava_img_src = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/div/div/span/img'
                        # сохраняем изображение
                        if self.xpath_exists(ava_img_src):
                            img_src_url = browser.find_element(By.XPATH, ava_img_src).get_attribute("src")
                            get_img = requests.get(img_src_url)
                            with open(f"{file_name}/{file_name}_Аватар.jpg", "wb") as img_file:
                                img_file.write(get_img.content)
                            time.sleep(2)
                            print(f"Аватарка {file_name} успешно скачана!")
                            with open(f"{file_name}/{file_name}_закрытый_аккаунт.txt", "w") as file:
                                file.write(f'{file_name} - private user ')
                        print(f"Закончили с аккаунтом {count_ac}: {file_name}.\n")
                        continue

                    ava_img_src = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/div/div/span/img'
                    if not self.xpath_exists(ava_img_src):
                        time.sleep(2)
                        img_src_url = browser.find_element(By.XPATH, ava_img_src).get_attribute("src")
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_Аватар.jpg", "wb") as img_file:
                            img_file.write(get_img.content)
                        time.sleep(1)
                        print(f"Аватарка {file_name} успешно скачана!")
                    # сохраняем изображение
                    if self.xpath_exists(ava_img_src):
                        img_src_url = browser.find_element(By.XPATH, ava_img_src).get_attribute("src")
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_Аватар.jpg", "wb") as img_file:
                            img_file.write(get_img.content)
                        time.sleep(1)
                        print(f"Аватарка {file_name} успешно скачана!")

                    # Сохраняем кол-во подписчиков
                    elements_ = browser.find_elements(By.XPATH, "//span[@title]")
                    for element in elements_:
                        followers = element.get_attribute("title")
                        if ',' in followers:
                            followers = ''.join(followers.split(','))
                            with open(f"{file_name}/{file_name}_количество_подписчиков.txt", "w") as file:
                                file.write(followers)
                        else:
                            with open(f"{file_name}/{file_name}_количество_подписчиков.txt", "w") as file:
                                file.write(followers)
                    print(f"Сохраняем кол-во подписчиков {file_name}.")
                    # собираем пользовательские ссылки на посты аккаунта
                    posts_urls = []
                    hrefs = browser.find_elements(By.TAG_NAME, 'a')
                    hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                    for href in hrefs:
                        posts_urls.append(href)
                        # сохраняем ссылки на последние 20 постов
                    print(f"Сохраняем список 20 последних постов {file_name}.")
                    with open(f'{file_name}/{file_name}_20_последних_постов.txt', 'w') as file:
                        for post_url in posts_urls[0: 20]:
                            file.write(post_url + "\n")

                    # Список элементов двадцати последних постов для наведения на них курсора
                    posts_20_hover = [
                        "//div[@class='_ac7v _aang'][1]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][1]/div[@class='_aabd _aa8k _aanf'][2]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][1]/div[@class='_aabd _aa8k _aanf'][3]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][2]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][2]/div[@class='_aabd _aa8k _aanf'][2]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][2]/div[@class='_aabd _aa8k _aanf'][3]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][3]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][3]/div[@class='_aabd _aa8k _aanf'][2]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][3]/div[@class='_aabd _aa8k _aanf'][3]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][4]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][4]/div[@class='_aabd _aa8k _aanf'][2]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][4]/div[@class='_aabd _aa8k _aanf'][3]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][5]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][5]/div[@class='_aabd _aa8k _aanf'][2]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][5]/div[@class='_aabd _aa8k _aanf'][3]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][6]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][6]/div[@class='_aabd _aa8k _aanf'][2]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][6]/div[@class='_aabd _aa8k _aanf'][3]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][7]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']",
                        "//div[@class='_ac7v _aang'][7]/div[@class='_aabd _aa8k _aanf'][2]//div[@class='_aagu']"
                    ]
                    print(f"Сохраняем количество коментов каждого поста:")
                    with open(f"{file_name}/{file_name}_кол_коментов.txt", "w") as file:
                        file.close()
                    num = 0
                    # Наведение курсора на каждый пост и сбор кол-ва коментов
                    for post in posts_20_hover:
                        if not self.xpath_exists(post):
                            print(f'Посты закончились, следующего поста нет.')
                            break
                        time.sleep(random.randrange(1, 2))
                        hover = browser.find_element(By.XPATH, post)
                        ActionChains(browser).move_to_element(hover).perform()
                        num += 1
                        if not self.xpath_exists("//li[@class='_abpm'][2]//span"):
                            print(f'В {num} посте данных о количестве коментов нет! идем дальше.')
                            with open(f"{file_name}/{file_name}_кол_коментов.txt", "a") as file:
                                file.write(f"post{num}: no comments.\n")
                            continue
                        num_comments = browser.find_element(By.XPATH, "//li[@class='_abpm'][2]//span").text
                        if ',' in num_comments:
                            num_comments = ''.join(num_comments.split(','))
                            with open(f"{file_name}/{file_name}_кол_коментов.txt", "a") as file:
                                file.write(f"post{num}: {num_comments}.\n")
                        else:
                            with open(f"{file_name}/{file_name}_кол_коментов.txt", "a") as file:
                                file.write(f"post{num}: {num_comments}.\n")
                        print(f"Сохраняем количество коментов поста {num}")

                    print(f"Открываем каждый пост {file_name} и сохраняем: дату публикации, кол-во лайков.")
                    # Открываем посты по очереди и сохраняем с каждого время и дату публикации, кол-во лайков
                    post = "//div[@class='_ac7v _aang'][1]/div[@class='_aabd _aa8k _aanf'][1]//div[@class='_aagu']"
                    if not self.xpath_exists(post):
                        print(f'Посты закончились, следующего поста нет.')
                        break
                    hover = browser.find_element(By.XPATH, post)
                    # наводим курсор и немного замираем на первом посте
                    ActionChains(browser).move_to_element(hover).perform()
                    xpath_post = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]"
                    xpath_post1 = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/div[2]/article/div/div/div[1]/div[1]"
                    # кликаем на него
                    if not self.xpath_exists(xpath_post):
                        browser.find_element(By.XPATH, xpath_post1).click()
                    else:
                        browser.find_element(By.XPATH, xpath_post).click()
                    with open(f'{file_name}/{file_name}_Дата_публикации_и_лайки.txt', 'w') as file:
                        file.close()
                    num = 0
                    for i in range(20):
                        time.sleep(random.randrange(1, 3))
                        for request in browser.requests:
                            if request.response:
                                print(
                                    request.url,
                                    request.response.status_code,
                                    request.response.headers['Content-Type'],
                                    request.body
                                )
                        num += 1
                        xpath = "//a[@class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd']/div[@class='_aacl _aaco _aacw _aacx _aada _aade']/span"
                        # проверка на наличие лайков
                        if not self.xpath_exists('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/div/time'):
                            print(f"Пост {num} не загрузился, даем больше времени.")
                            time.sleep(random.randrange(3, 6))
                            if not self.xpath_exists(
                                    '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/div/time'):
                                print(f"Пост {num} не загрузился, даем больше времени.")
                                time.sleep(random.randrange(4, 7))
                                if not self.xpath_exists(xpath):
                                    if not self.xpath_exists(
                                            '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/div/time'):
                                        print(f"Пост {num} так и не смог загрузиться.")
                                        button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
                                        hover = browser.find_element(By.XPATH, button_xpath)
                                        ActionChains(browser).move_to_element(hover).perform()
                                        browser.find_element(By.XPATH, button_xpath).click()
                                        continue
                                    print(f'В {num} посте данных о количестве лайков нет! идем дальше.')
                                    time_elements = browser.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                                    time_ = time_elements.replace('T', '  time: ')
                                    with open(f'{file_name}/{file_name}_Дата_публикации_и_лайки.txt', 'a') as file:
                                        file.write(f"Post {num} data public: {time_}; No likes\n")
                                    # наводим курсор и немного замираем на кнопке перехода на след пост и кликаем ее
                                    if not self.xpath_exists(
                                            "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"):
                                        print(f'Посты закончились, следующего поста нет.')
                                        break
                                    button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
                                    hover = browser.find_element(By.XPATH, button_xpath)
                                    ActionChains(browser).move_to_element(hover).perform()
                                    browser.find_element(By.XPATH, button_xpath).click()
                                    continue
                            print(f"Собираем данные поста {num}.")
                            like_button = browser.find_element(By.XPATH, xpath)
                            like_count = like_button.text
                            time_elements = browser.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                            time_ = time_elements.replace('T', '  time: ')
                            if ',' in like_count:
                                like_count = ''.join(like_count.split(','))
                            with open(f'{file_name}/{file_name}_Дата_публикации_и_лайки.txt', 'a') as file:
                                file.write(f"Post {num} data public: {time_};    number likes: {like_count}\n")
                                button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
                                hover = browser.find_element(By.XPATH, button_xpath)
                                ActionChains(browser).move_to_element(hover).perform()
                                browser.find_element(By.XPATH, button_xpath).click()
                                continue
                        else:
                            print(f"Собираем данные поста {num}.")
                            if not self.xpath_exists(xpath) and self.xpath_exists('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/div/time'):
                                print(f'В {num} посте данных о количестве лайков нет! идем дальше.')
                                time_elements = browser.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                                time_ = time_elements.replace('T', '  time: ')
                                with open(f'{file_name}/{file_name}_Дата_публикации_и_лайки.txt', 'a') as file:
                                    file.write(f"Post {num} data public: {time_}; No likes\n")
                                # наводим курсор и немного замираем на кнопке перехода на след пост и кликаем ее
                                if not self.xpath_exists(
                                        "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"):
                                    print(f'Посты закончились, следующего поста нет.')
                                    break
                                button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
                                hover = browser.find_element(By.XPATH, button_xpath)
                                ActionChains(browser).move_to_element(hover).perform()
                                browser.find_element(By.XPATH, button_xpath).click()
                                continue
                            if not self.xpath_exists(xpath) and not self.xpath_exists('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/div/time'):
                                print(f"Пост {num} не загрузился, даем больше времени.")
                                time.sleep(random.randrange(3, 6))
                                if not self.xpath_exists(xpath):
                                    print(f"Пост {num} так и не смог загрузиться.")
                                    if not self.xpath_exists(
                                            "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"):
                                        print(f'Посты закончились, следующего поста нет.')
                                        break
                                    button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
                                    hover = browser.find_element(By.XPATH, button_xpath)
                                    ActionChains(browser).move_to_element(hover).perform()
                                    browser.find_element(By.XPATH, button_xpath).click()
                                    continue
                            like_button = browser.find_element(By.XPATH, xpath)
                            like_count = like_button.text
                            time_elements = browser.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                            time_ = time_elements.replace('T', '  time: ')
                            if ',' in like_count:
                                like_count = ''.join(like_count.split(','))
                            with open(f'{file_name}/{file_name}_Дата_публикации_и_лайки.txt', 'a') as file:
                                file.write(f"Post {num} data public: {time_};    number likes: {like_count}\n")
                            # наводим курсор и немного замираем на кнопке перехода на след пост и кликаем ее
                            if not self.xpath_exists("//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"):
                                print(f'Посты закончились, следующего поста нет.')
                                break
                            button_xpath = "//div[@class='_aear']/div[@class=' _aaqg _aaqh']/button[@class='_abl-']"
                            hover = browser.find_element(By.XPATH, button_xpath)
                            ActionChains(browser).move_to_element(hover).perform()
                            browser.find_element(By.XPATH, button_xpath).click()

                print(f"Закончили с аккаунтом {count_ac}: {file_name}.\n")
            except Exception as ex:
                print(ex)


my_bot = InstagramBot()
my_bot.login(username1, password1)
my_bot.get_followers_ava_posts(
    'https://www.instagram.com/......',
    'https://www.instagram.com/......',
    'https://www.instagram.com/......'
                               )
my_bot.close_browser()
time.sleep(random.randrange(3, 6))
my_bot = InstagramBot()
my_bot.login(username2, password2)
my_bot.get_followers_ava_posts(
    'https://www.instagram.com/......',
    'https://www.instagram.com/......',
    'https://www.instagram.com/......'
)
my_bot.close_browser()
time.sleep(random.randrange(3, 6))
my_bot = InstagramBot()
my_bot.login(username3, password3)
my_bot.get_followers_ava_posts(
    'https://www.instagram.com/......',
    'https://www.instagram.com/......',
    'https://www.instagram.com/......'
)
my_bot.close_browser()
time.sleep(random.randrange(3, 6))
my_bot = InstagramBot()
my_bot.login(username, password)
my_bot.get_followers_ava_posts(
    'https://www.instagram.com/......',
    'https://www.instagram.com/......',
    'https://www.instagram.com/......'
)
my_bot.close_browser()
