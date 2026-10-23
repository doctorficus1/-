import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

BASE_URL = "http://192.168.0.251:8081"
# Указываем путь к драйверу Edge, который мы положили в папку с проектом
DRIVER_PATH = r"E:\opencart-project\msedgedriver.exe"


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless") # Если захочешь скрыть окна браузера

    # Запускаем Edge
    service = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    driver.implicitly_wait(3)

    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return BASE_URL