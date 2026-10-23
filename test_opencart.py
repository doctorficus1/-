import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



def test_home_page_title(driver, base_url):
    """Тест 1: Проверка заголовка страницы"""
    driver.get(base_url)
    assert "Your Store" in driver.title


def test_logo_is_visible(driver, base_url):
    """Тест 2: Проверка отображения логотипа"""
    driver.get(base_url)
    logo = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#logo img, a.navbar-brand img, header img"))
    )
    assert logo.is_displayed()


def test_search_input_present(driver, base_url):
    """Тест 3: Проверка наличия строки поиска"""
    driver.get(base_url)
    search = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "search"))
    )
    assert search.is_displayed()



def test_search_positive(driver, base_url):
    """Тест 4: Поиск существующего товара (MacBook)"""
    driver.get(base_url)
    search = driver.find_element(By.NAME, "search")
    search.clear()
    search.send_keys("MacBook")
    search.send_keys(Keys.RETURN)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-layout, .product-thumb"))
    )
    assert "MacBook" in driver.page_source


def test_search_empty(driver, base_url):
    """Тест 5: Отправка пустого поискового запроса"""
    driver.get(base_url)
    search = driver.find_element(By.NAME, "search")
    search.clear()
    search.send_keys(Keys.RETURN)
    assert "search" in driver.current_url or driver.current_url.endswith("/")



def test_navigation_menu_links(driver, base_url):
    """Тест 6: Проверка кликабельности меню"""
    driver.get(base_url)
    links = driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar-nav a")
    assert len(links) >= 2
    for link in links[:3]:
        assert link.is_enabled()


def test_footer_present(driver, base_url):
    """Тест 7: Проверка наличия футера"""
    driver.get(base_url)
    footer = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "footer"))
    )
    assert footer.is_displayed()



def test_admin_login_page(driver, base_url):
    """Тест 8: Проверка перехода на страницу авторизации админки"""
    driver.get(base_url + "/administration")
    assert "administration" in driver.current_url.lower() or "login" in driver.page_source.lower()


def test_admin_login_invalid(driver, base_url):
    """Тест 9: Попытка входа в админку с неверным паролем"""
    driver.get(base_url + "/administration")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("user")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .btn-primary").click()

    error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger, .text-danger, [role='alert']"))
    )
    assert error.is_displayed()


def test_admin_login_valid(driver, base_url):
    """Тест 10: Успешный вход в админку с правильными данными"""
    driver.get(base_url + "/administration")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("user")
    driver.find_element(By.NAME, "password").send_keys("bitnami")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .btn-primary").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("route=common/dashboard")
    )
    assert "dashboard" in driver.current_url.lower()