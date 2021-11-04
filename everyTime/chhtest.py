from selenium import webdriver
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')

chrome_options.add_argument('--no-sandbox')

chrome_options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome("/usr/bin/chromedriver")



driver.get('http://naver.com')
