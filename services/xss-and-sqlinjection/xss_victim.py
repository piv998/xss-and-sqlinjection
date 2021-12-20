from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def css(selector):
    global driver
    return WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

def alert():
    global driver
    WebDriverWait(driver, 100).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
    alert = driver.switch_to.alert
    alert.accept()

def slowSendKeys(elem, keys):
    for key in keys:
        elem.send_keys(key)
        sleep(0.1)

def randWord(symbol_count, alphabet):
    res = [random.choice(alphabet) for _ in range(symbol_count)]
    return ''.join(res)

def randId():
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    a = randWord(4, alphabet)
    b = randWord(4, alphabet)
    c = randWord(4, alphabet)
    return f'{a}-{b}-{c}'


def randFlag():
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    a = randWord(31, alphabet)
    return f'{a}='

def main(generatedFlagsCount, intruderKey):
    global driver    
    driver.get("http://localhost")
    addFlagAnchor = css('a[href="add_flag.html"')
    addFlagAnchor.click()

    keyEl = css('#key')
    valueEl = css('#value')

    flags = []

    for i in range(generatedFlagsCount):
        keyEl.clear()
        valueEl.clear()
        id = randId()
        flag = randFlag()
        keyEl.send_keys(id)
        valueEl.send_keys(flag)
        valueEl.send_keys(Keys.RETURN)
        alert()
        print(f'{id} {flag}')
        flags.append({"id": id, "flag": flag})

    sleep(1)

    mainAnchor = css('a[href="index.html"]')
    mainAnchor.click()
    viewFlagAnchor = css('a[href="get_flag.html"]')
    viewFlagAnchor.click()
    keyEl = css('#key')
    keyEl.send_keys(intruderKey)
    keyEl.send_keys(Keys.RETURN)

    intruderButton = css('button[onclick]')
    intruderButton.click()

    sleep(1)

    for flag in flags:
        keyEl.clear()
        slowSendKeys(keyEl, flag['id'])
        keyEl.send_keys(Keys.RETURN)
        sleep(0.2)

    sleep(1)



driver = webdriver.Chrome()
try:
    main(generatedFlagsCount=30, intruderKey='a')
    sleep(1)
finally:
    # driver.close()
    driver.quit()

