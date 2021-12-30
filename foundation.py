import requests
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import artists_sn
import pandas as pd
import openpyxl
import os
import shutil
import pyautogui
from threading import *

print("-This app will open Google Chrome, it will be closed by itself, don't touch it.-")
target = int(input('Enter the amount of artists for invites-scanning: '))

end_xpath = f'//*[@id="__next"]/div[4]/div[2]/div/div[2]/div[1]/div[{target + 25}]/a/div[2]/div[1]/div'

pass_ = []


def keys_end(html):
    repeat_in = True
    while repeat_in is True:
        html.send_keys(Keys.END)
        if len(pass_) > 0:
            repeat_in = False


def wait_page(wait):
    try:
        wait.until(ec.visibility_of_element_located((By.XPATH, end_xpath)))
        pass_.append('end')
    except:
        print('Error 404')


def links(target):
    list_url = 'https://foundation.app/profiles?sortBy=users_sort_date_joined_desc'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(list_url)

    load_time = 50
    wait = WebDriverWait(driver, load_time)
    actions = ActionChains(driver)

    try:
        wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[4]/div[1]/div[2]/div/div[2]')))
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[4]/div[1]/div[2]/div/div[2]/select').click()
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[4]/div[1]/div[2]/div/div[2]/select/option[2]').click()
        driver.find_element(By.XPATH, '//*[@id="header"]/div/div').click()
    except Exception as ex:
        print(ex)
        input('Check your internet connection. This program will be closed.')

    html = driver.find_element(By.TAG_NAME, 'html')
    t_wait = Thread(target=wait_page, args=(wait,))
    t_keys = Thread(target=keys_end, args=(html,))

    t_keys.start()
    t_wait.start()
    actions.key_down(Keys.END)
    actions.perform()
    x = 1  # Counting

    nicknames = []
    errors = []

    for n in range(26, target + 26):
        try:
            xPath = f'//*[@id="__next"]/div[4]/div[2]/div/div[2]/div[1]/div[{n}]/a/div[2]/div[1]/div'
            element = driver.find_element(By.XPATH, xPath)
            print(str(x) + '/' + str(target) + ' has been added...')
            x += 1
            nicknames.append(element.text)
        except Exception as e:
            try:
                xPath = f'//*[@id="__next"]/div[4]/div[2]/div/div[2]/div[1]/div[{n}]/a'
                element = driver.find_element(By.XPATH, xPath)
                print('***', x, str(e).splitlines()[0], '***')
                print(str(x) + '/' + str(target) + ' has been added as name: ', element.text.splitlines()[0])
                x += 1
                nicknames.append(element.text.splitlines()[0])
            except:
                if len(errors) == 4:
                    print("--Seems like page didn't load completely,"
                          "or you just closed Google Chrome.\nPlease try to restart the app in a couple minutes--")
                    input()
                else:
                    errors.append('0')
                    print('Failed to add', str(x) + '. Moving forward.')

                continue

    t_wait.join()
    t_keys.join()
    driver.close()

    links_list = []
    artist_link = 'https://foundation.app/'
    for nickname in nicknames:
        links_list.append(artist_link + nickname)
    return links_list


if __name__ == '__main__':

    # Defining the list of authors from newest to oldest
    try:
        authors = links(target)
    except Exception as exc:
        print(str(exc))
        input('Now you need to restart me.')
    # Defining if these authors have some sold works (theoretically have any invites).
    # Creating a lists of authors with any sold works.
    instagram_list, twitter_list, foundation = artists_sn.sn_get(authors)

    # Saving these lists to ./Links
    foundations = pd.DataFrame(foundation)
    inst_table = pd.DataFrame(instagram_list)
    twitter_table = pd.DataFrame(twitter_list)

    z_mistake = 1
    while z_mistake == 1:
        try:
            os.mkdir('./Links')
        except:
            try:
                os.rmdir('./Links')
            except:
                shutil.rmtree('./Links')
        else:
            z_mistake = 0

    inst_table.to_excel('./Links/inst.xlsx')
    twitter_table.to_excel('./Links/twitters.xlsx')
    foundations.to_excel('./Links/artists.xlsx')

    print('\n')
    input('Lists are successfully created, check them in "Links" folder.')
