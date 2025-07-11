from selenium.common import StaleElementReferenceException
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from random import randint

def initSelenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    #start driver selenium
    driver = webdriver.Chrome(options=options)
    return driver;


def openFileandWrite(content, filename):
    with open(filename, "a") as file:
        file.write("\n" + content)

def registerationRequest(firstName, lastName, email, password):
    data = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password 
    }
    driver = initSelenium()
    siteUrl = "https://www.unhinged.ai/"
    
    try:
        driver.get(siteUrl)
        
        # Wait for the initial button to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()

        # Wait for the "Sign Up" button to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Sign Up"))).click()

        # Wait for the form elements to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstName")))
        
        # Fill out the form elements
        driver.find_element(By.ID, "firstName").send_keys(firstName)
        driver.find_element(By.ID, "lastName").send_keys(lastName)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "confirmPassword").send_keys(password)

        # Click the sign-up button
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Sign Up')]")))
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign Up')]").submit()

        # Wait for the page to load (adjust as needed)
        # note this is used to submit form, can give exception when using click 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Log data
        print("Data completed:", data)
        openFileandWrite(str(data), "users.txt")

        sleep(2)
    except StaleElementReferenceException:
        print("Stale element error.")
    except Exception as e:
        print("Error", e)
    finally:
        # Close the WebDriver after execution
        driver.quit()  

def main():
    #run main functions here
    account_input = int(input("How many accounts would you like to be made? "))
    print(account_input)
    for i in range(1, account_input+1):
        print("Count", i)
        fake = Faker()
        fakerSeed = randint(0,10000)
        print("Faker Seed", fakerSeed)
        Faker.seed(fakerSeed)
        registerationRequest(fake.first_name(), fake.last_name(), fake.email(), fake.password())

if __name__ == "__main__":
    print("Loading main.py")
    main()
