import sys, os, random, string, time, urllib.parse
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager

username = sys.argv[1]
password = sys.argv[2]
pc_search = 2
mobile_search = 2
with open('words.txt', 'r') as f:
    words = f.read().split()

def getUrl(driver, url, sleep=3, retry=3):
    for _ in range(retry):
        try:
            driver.get(url)
            print(f"[Title]: {driver.title.lower()}")
            time.sleep(sleep)
            break
        except Exception as e:
            print(f"[GET ERROR {url}] {e}")

_driver_path = EdgeChromiumDriverManager().install()
print(f"EdgeChromiumDriverManager installed Successfully at {_driver_path}")

_options = Options()
_options.add_argument("--headless")
_options.add_argument("--disable-gpu")
_options.add_argument("--no-sandbox")

driver = webdriver.Edge(_options, Service(_driver_path))
driver.set_page_load_timeout(10)

getUrl(driver, 'https://rewards.bing.com/')

if "sign in" in driver.title.lower():
    email_field = driver.find_element(By.NAME, "loginfmt")
    email_field.send_keys(username)
    email_field.send_keys(Keys.RETURN)
    time.sleep(3)
    print(f"[Title]: {driver.title.lower()}")
    
    password_field = driver.find_element(By.NAME, "passwd")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    print(f"[Title]: {driver.title.lower()}")
    
    if "stay signed in" in driver.title.lower():
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)
        print(f"[Title]: {driver.title.lower()}")
        
getUrl(driver, 'https://rewards.bing.com/')
_user = driver.find_element(By.ID, 'mectrl_currentAccount_primary').get_attribute('textContent').strip()
_total = int(driver.find_element(By.ID, 'balanceToolTipDiv').get_attribute('textContent').split()[-1])
_today = int(driver.find_element(By.ID, 'dailypointToolTipDiv').get_attribute('textContent').split()[-1])
print(F"[{_user}] Total: {_total} Today: {_today}")

_tab1 = driver.current_window_handle
_a_href = [a.get_attribute('href') for a in driver.find_elements(By.XPATH, "//p[@ng-bind-html='$ctrl.pointProgressText']") if a.get_attribute('href')]
for _href in _a_href:
    getUrl(driver, _href)

# for tab in driver.window_handles:
#     if tab != _tab1:
#         driver.switch_to.window(tab)
#         driver.close()
driver.switch_to.window(_tab1)

for _ in range(pc_search):
    getUrl(driver, f"https://www.bing.com/search?q={random.choice(words)}&form=QBLH&sp=-1&ghc=1&lq=0&pq=hel&sc=10-3&qs=n&sk=&cvid=CA3534C5DE96458BB6A7C71DDAD1EC80&ghsh=0&ghacc=0&ghpl=")

dev_tools = driver.execute_cdp_cmd
dev_tools('Emulation.setDeviceMetricsOverride', {
    'mobile': True,
    'width': 375,
    'height': 667,
    'deviceScaleFactor': 2,
    'fitWindow': True
})
dev_tools('Network.setUserAgentOverride', {
    'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    'deviceScaleFactor': 2,
})

for _ in range(mobile_search):
    getUrl(driver, f"https://www.bing.com/search?q={random.choice(words)}&form=QBLH&sp=-1&ghc=1&lq=0&pq=hel&sc=10-3&qs=n&sk=&cvid=CA3534C5DE96458BB6A7C71DDAD1EC80&ghsh=0&ghacc=0&ghpl=")

getUrl(driver, 'https://rewards.bing.com/')

user = driver.find_element(By.ID, 'mectrl_currentAccount_primary').get_attribute('textContent').strip()
total = int(driver.find_element(By.ID, 'balanceToolTipDiv').get_attribute('textContent').split()[-1])
today = int(driver.find_element(By.ID, 'dailypointToolTipDiv').get_attribute('textContent').split()[-1])
print(F"[{user}] Total: {total} Today: {today}")

getUrl(driver, 'https://rewards.bing.com/pointsbreakdown')
_status = driver.find_element(By.XPATH, "//div[@id='earningreport-level-heading']/p").get_attribute('textContent').strip()

body = f"[{user}]\nTotal: {total-_total} [{_total}->{total}]\nToday: {today-_today} [{_today}->{today}\nStatus: {_status}]"
qbody = urllib.parse.quote(body)
getUrl(driver, f"https://script.google.com/macros/s/AKfycbxQJ8fPbmXHu2qKO8gCE_5ezf-0CH0s7jXDGbRarJVsuTNlNzMoIVfr_wiXy73DC-Ob/exec?email=bhowmickdip8@gmail.com&sub=Microsoft-Reward-Points&body={qbody}")
print(driver.find_element(By.TAG_NAME, 'body').text)
print(body)

driver.quit()
