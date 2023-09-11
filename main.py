from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep

# Driver settings
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.instagram.com/")
driver.maximize_window()

# username = input("Enter username: ")
username = "your_username"
username_insta = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
# password = input("Enter password: ")
password = "your_password"
password_insta = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

username_insta.clear()
password_insta.clear()
username_insta.send_keys(username)
password_insta.send_keys(password)

login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
not_now_save = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not Now')]"))).click()
not_now_notification = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

profile_link1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Profile')]"))).click()
sleep(5)
get_following_count = driver.find_elements(By.XPATH, f"//a[@href='/{username}/following/']//span//span")
total_following = int()
try:
    for following_count in get_following_count:
        total_following = int(following_count.text)
except:
    pass

print(total_following)
following_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), ' following')]"))).click()
sleep(5)
i = 1
while i < total_following - 1:
    try:
        element = driver.find_element(By.XPATH, f"//div[@class='_aano']//div[{i}]")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        i = i + 1
    except:
        sleep(1)


sleep(10)
following_profile_images = driver.find_elements(By.TAG_NAME, "img")
following_profile_images = [image.get_attribute('alt') for image in following_profile_images]

following_name = []
for image in following_profile_images:
    if image.find("\'s profile picture") != -1:
        image = image.replace("\'s profile picture", "")
        following_name.append(image)

following_name.remove(username)
following_name.remove('Highlights')
followings = []
for i in range(total_following):
    followings.append(following_name[i])

print(followings)
print(len(followings))

with open("following.txt", "w") as f:
    for followings_username in followings:
        f.write(followings_username + "\n")

f.close()


close_button = driver.find_element(By.XPATH, "//button[@type='button' and @class='_abl-']").click()
get_follower_count = driver.find_elements(By.XPATH, f"//a[@href='/{username}/followers/']//span//span")
try:
    for follower_count in get_follower_count:
        total_followers = int(follower_count.text)
except:
    pass

print(total_followers)

follower_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), ' follower')]"))).click()

sleep(5)
i = 1
while i < total_followers - 1:
    try:
        element = driver.find_element(By.XPATH, f"//div[@class='_aano']//div[{i}]")
        element.location_once_scrolled_into_view
        i = i + 1
    except:
        sleep(1)

sleep(10)
follower_profile_images = WebDriverWait(driver, 10).until(lambda x:x.find_elements(By.TAG_NAME, "img"))
follower_profile_images = [image.get_attribute('alt') for image in follower_profile_images]

followers_name = []
for image in follower_profile_images:
    if image.find("\'s profile picture") != -1:
        image = image.replace("\'s profile picture", "")
        followers_name.append(image)

followers_name.remove(username)
followers_name.remove('Highlights')

followers = []
for i in range(total_followers):
    try:
        followers.append(followers_name[i])
    except:
        pass

print(followers)
print(len(followers))

with open("followers.txt", "w") as f:
    for followers_username in followers:
        f.write(followers_username + "\n")

f.close()
driver.close()