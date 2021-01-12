from time import sleep
from selenium import webdriver
import csv
import random

login = 'nickname'
password = 'password'
account = 'morgen_shtern/'

browser = webdriver.Firefox()

nicknames = []
array = [] #массив для перевода значения количества подписчков из str в int
messages = [] # contents message strings

def slp():
    a = random.randint(1, 8)
    for n in range(a + 1):
        print('sleeping ' + str(n) + '/' + str(a))
        sleep(n)

def cook():
    #cookie = {'name' : 'foo', 'value' : 'bar'}
    #browser.add_cookie(cookie)
    #browser.get_cookies()
    browser.delete_all_cookies()

def log_in():

    browser.implicitly_wait(5)

    browser.get('https://www.instagram.com/')

    cook()
    slp()

    username_input = browser.find_element_by_css_selector("input[name='username']")
    password_input = browser.find_element_by_css_selector("input[name='password']")

    username_input.send_keys(login)
    password_input.send_keys(password)

    login_button = browser.find_element_by_xpath("//button[@type='submit']")
    login_button.click()

    slp()

    not_now_button = browser.find_element_by_xpath("//button[@type='button']")
    not_now_button.click()
    slp()

    try:
        not_now_button2 = browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]") #disabling notifications
        slp()
    except:
        try:
            not_now_button2 = browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
            slp()
        except: # and another attempt for different accounts
            not_now_button2 = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
    slp()
    not_now_button2.click()

def scroll():
    SCROLL_PAUSE_TIME = 0.5
    count = 0
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('scrolling.. ')
    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)

def adjust(str):
    slp()
    for i in str:
        if i == ',':
            pass
        else:
            array.append(i)
    print(array)
    num = ''.join(array)
    num = int(num)
    print(num)
    return num

def get(i):
    print(type(i))

    last_sub = int(input('input the latter sub: '))
    n = 0
    while n < last_sub:
        n += 1
        try:
            el = browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/ul/div/li[{}]/div/div[1]/div[2]/div[1]/span/a'.format(n)) # parsing followers
        except:
            try:
                el = browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/ul/div/li[{}]/div/div[2]/div[1]/div/div/span/a'.format(n))
            except:
                el = browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/ul/div/li[{}]/div/div[2]/div/div/div/span/a'.format(n))

        print('parsing element ' + str(n))
        name = el.get_attribute('title')
        #print(name)
        nicknames.append(name)
        with open('nicknames.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name])
            f.close()
        scroll()
    print('parsing finished')

def parse():

    browser.get('https://www.instagram.com/' + account)
    print('Press Ctrl + Shift + M to Enter cell mode in browser and press enter here to continue')
    input()
    slp()

    sub_max = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/ul/li[2]/a/span').get_attribute('title') #setting the last subscriber
    #browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click() # opens /followers/
    browser.find_element_by_xpath('/html/body/div[1]/section/main/div/ul/li[2]/a/span').click()
    print(sub_max)
    get(sub_max)
    slp()

def get_message_content(n):

    with open('msg' + str(n) + '.txt', 'r', encoding='utf-8') as f:
        message_content  = f.read()
        print('message_content {} = '.format(n) + message_content)
        messages.append(message_content)

def message(nickname, message_content, n_of_textfile):

    create_dialog = browser.find_element_by_xpath('//*[@id="react-root"]/section/div/div[1]/div/div[3]/div/div[2]/a/svg/path')
    create_dialog.click()
    slp()
    receiver = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
    receiver.click()
    receiver.send_keys(nickname)
    slp()
    browser.find_element_by_xpath('//*[@id="f208bd861f4ec38"]/div').click()
    slp()
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div/button/div').click()
    slp()
    get_message_content(n_of_textfile)
    browser.find_element_by_css_selector(
    '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea').send_keys(message_content)

def whaddyawant():

    print('wanna parse? ')
    answer = input('y for yes or n for no: ')
    if answer == 'y':
        parse()
    else:
        pass


log_in()
whaddyawant()
