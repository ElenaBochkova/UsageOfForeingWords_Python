""" находит слово в гугл переводчике и проигрывает его звук"""
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time

def play(word_name):
    if word_name == "":
        word_name = "empty space"
    opts = Options()
    opts.headless = True
    browser = Firefox(options=opts)
    word_path = 'https://translate.google.com/#auto/ru/' + word_name
    browser.get(word_path)
    browser.find_element_by_xpath("//div[3]/div[2]/div").click()
    time.sleep(1)
    browser.quit();

if __name__ == '__main__':
    import sys
    params = sys.argv[1:]
    if len(params)==0:
        word_name = "empty space"
    else:
        word_name = params[0]
    play(word_name)
    
