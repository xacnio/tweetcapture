from selenium import webdriver
from selenium.webdriver.chrome.options import Options


async def get_driver(lang, custom_options=None, driver_path=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=430,1000");

    if isinstance(custom_options, list) and len(custom_options) > 0:
        for option in custom_options:
            chrome_options.add_argument(option)
    if lang:
        chrome_options.add_argument('--lang=' + lang)

    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(
        executable_path=driver_path, options=chrome_options)

    return driver
