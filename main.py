from selenium import webdriver
from dotenv import load_dotenv
import time
from webdriver_manager.chrome import ChromeDriverManager
from pynput.keyboard import Key, Controller
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as EC
import csv

def get_content(path='content'):
    content_path=os.getcwd()+'\\'+path
    content_list=os.listdir(content_path)
    return content_list
def show_group_links(groups):
    print("-------Total subscribed Groups Links are:",len(groups),"-----------")
    print("------printing groups links------------")
    for index,value in enumerate(groups):
        print("--------",index," ",value," ","--------")
    return 0
def file_type(file_name):
    file_type=file_name.split('.')[1]
    return file_type
    
def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    
def read_credentials_from_csv(filename):
    credentials = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header if exists
        for row in reader:
            if len(row) == 2:  # Assuming each row has username and password
                credentials.append((row[0], row[1]))
    return credentials


# Function to check for alert and dismiss it
def check_and_dismiss_alert(driver):
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        if alert:
            print("Alert detected! Dismissing...")
            alert.dismiss()
    except:
        print("No alert detected.")
        
def Leave_popup(driver):
    try:
        driver.switchTo().alert().accept();
    except:
        pass
    

load_dotenv('.env')
print("---Loaded .env variables---")
url=os.getenv('url')
SCROLL_PAUSE_TIME = 3
credentials_list=read_credentials_from_csv('credentials.csv')
print('----  credentials loaded from credentials.csv-----')
credentials_list_lenght=len(credentials_list)
content_list=get_content()
content_list_lenght=len(content_list)

print("---Initializing the webdriver---")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-popup-blocking')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
print("---webdriver intialized---")

for i in range(credentials_list_lenght):
    username=credentials_list[i][0]
    password=credentials_list[i][1]
    driver.get(url)
    print("---Login to FB Account-:",str(username),"---")
    time.sleep(5)

    driver.find_element(By.XPATH,"//input[@id='email']").send_keys(username)
    driver.find_element(By.XPATH,"//input[@id='pass']").send_keys(password)
    data=driver.find_element(By.XPATH,"//button[@name='login']").click()
    if driver.current_url != "https://www.facebook.com/":
        print("Login unsuccessful. Please check your email and password.")
        driver.quit()
    else:
        time.sleep(5)
        print("<________",str(username), "login successful ________>")
        driver.get("https://www.facebook.com/groups/joins/?nav_source=tab")
        check_and_dismiss_alert(driver)
        # Scroll down to load all groups
        time.sleep(6)
        print("<________Facebook Group page Scrolling________>")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("<-------Fetching the links of face groups---------->")
        groups = driver.find_elements(By.XPATH,"//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3']")

        count=0
        content_list_counter=0
        list=[]
        for group in groups:
            list.append(group.get_attribute("href"))
        show_group_links(list)
        for group in list:
            if(content_list_counter<content_list_lenght):
                count=count+1
                print("<---------Open the group page---------->",group)
                driver.get(group)
                check_and_dismiss_alert(driver)
                time.sleep(2)
                last_height = driver.execute_script("return document.body.scrollHeight")
                count=1
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    if count>=2:
                        break
                    count+=1
                    last_height = new_height
                time.sleep(3)
                try:
                    res = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,"//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 xk50ysn xzsf02u']"))
                )   
                    # res=driver.find_element(By.XPATH,"//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 xk50ysn xzsf02u']")
                    res=res.text
                except:
                    res=''
                if(str(res)==str('Your membership is pending')):
                    continue
                else:
                    try:
                        content_path=os.getcwd()+'\\content\\'+str(content_list[content_list_counter])
                        filetype=file_type(content_list[content_list_counter])
                        driver.get(group)
                        time.sleep(2)
                        check_and_dismiss_alert(driver)
                        # Leave_popup(driver)
                        
                        create_post_button = driver.find_element(By.XPATH,"//span[contains(text(), 'Write something...')]")
                        create_post_button.click()
                        time.sleep(5)
                        try:
                            post_area=driver.find_element(By.CLASS_NAME,'_5rp7')
                            post_area.click()
                        except Exception as e:
                            time.sleep(15)
                            post_area=driver.find_element(By.CLASS_NAME,'_5rp7')
                            post_area.click()
                            
                        time.sleep(2)
                        
                        if filetype=='txt':
                            # Wait for the post box to load
                            post_text_area=driver.switch_to.active_element
                            post_text = read_file_to_string(content_path)
                            # post_text="adffffff dfff"
                            post_text_area.send_keys(post_text)
                            check_and_dismiss_alert(driver)
                            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            # time.sleep(SCROLL_PAUSE_TIME)
                            # new_height = driver.execute_script("return document.body.scrollHeight")
                            for _ in range(10):
                                pyautogui.press('tab')
                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)
                            time.sleep(15)
                            print("-----------File name:",content_list[content_list_counter]," upload to the group ",group," -----------")
                            content_list_counter=content_list_counter+1
                            print("<----------Group post Completed-------->") 
                        elif filetype in ['mp4','mov','avi']:
                            time.sleep(1)
                            upload_icon=driver.find_element(By.XPATH,"//div[@class='xr9ek0c xfs2ol5 xjpr12u x12mruv9']")
                            upload_icon.click()
                            time.sleep(4)
                            upload_popup=driver.find_element(By.XPATH,"//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x6s0dn4 x1gslohp x12nagc xzboxd6 x14l7nz5']")
                            upload_popup.click()
                            time.sleep(5)
                            keyboard=Controller()
                            keyboard.type(content_path)
                            keyboard.press(Key.enter)
                            time.sleep(20)
                            for _ in range(10):
                                pyautogui.press('tab')
                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)
                            time.sleep(15)
                            print("-----------File name:",content_list[content_list_counter]," upload to the group ",group," -----------")

                            content_list_counter=content_list_counter+1
                            
                        elif filetype in ['png','jpeg','gif']:
                            time.sleep(1)
                            upload_icon=driver.find_element(By.XPATH,"//div[@class='xr9ek0c xfs2ol5 xjpr12u x12mruv9']")
                            upload_icon.click()
                            time.sleep(4)
                            upload_popup=driver.find_element(By.XPATH,"//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x6s0dn4 x1gslohp x12nagc xzboxd6 x14l7nz5']")
                            upload_popup.click()
                            time.sleep(3)
                            keyboard=Controller()
                            keyboard.type(content_path)
                            keyboard.press(Key.enter)
                            time.sleep(5)
                            for _ in range(10):
                                pyautogui.press('tab')
                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)
                            time.sleep(15)
                            print("-----------File name:",content_list[content_list_counter]," upload to the group ",group," -----------")

                            content_list_counter=content_list_counter+1
                        else:
                            print("------------Some things went wrong on the Group:  ",group,"------------")
        
                        
                    except Exception as e:
                        print("^^^^^^^^^^^^^^^^^^^^^")
                        print("<><><><>ERROR<><><>")
                        driver.get("https://www.facebook.com/groups/joins/?nav_source=tab")
                        keyboard=Controller()
                        keyboard.press(Key.enter)
                        time.sleep(15)
                        continue
            else:
                time.sleep(20)
                driver.quit()
                print("<-----------",username,":","All data is uploaded sucessfully-------->")
                break