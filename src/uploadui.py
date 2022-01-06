import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select

def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )

def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud") 

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

def get_tier_from_name(name):
    if "Tier 1" in name:
        return 1
    elif "Tier 2" in name:
        return 2
    elif "Tier 3" in name:
        return 3
    elif "Tier 4" in name:
        return 4
    elif "Tier 5" in name:
        return 5
    elif "Tier 6" in name:
        return 6

def calculate_price_based_on_tier(tier):
    if tier == 1:
        return 1.024
    if tier == 2:
        return 0.512
    if tier == 3:
        return 0.256
    if tier == 4:
        return 0.128
    if tier == 5:
        return 0.048
    if tier == 6:
        return 0.016

def get_tier_attr_from_tier(tier):
    if tier == 1:
        return "Tier 1"
    if tier == 2:
        return "Tier 2"
    if tier == 3:
        return "Tier 3"
    if tier == 4:
        return "Tier 4"
    if tier == 5:
        return "Tier 5"
    if tier == 6:
        return "Tier 6"

# _____MAIN_CODE_____
def upload_ui(driver, metadata):
    ###START###

    ###wait for methods
    wait = WebDriverWait(driver, 60)

    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )
        
    def wait_css_selectorTest(code):
        wait.until(
            ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
        )    

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))


    for data in metadata:
        print("Start creating NFT ", data["name"])
        COLLECTION_URL = os.getenv('COLLECTION_URL')
        IMAGE_FOLDER = os.getenv('IMAGE_FOLDER')
        THUMBNAIL_FOLDER = os.getenv('THUMBNAIL_FOLDER')
        driver.get(COLLECTION_URL)
        # time.sleep(3)

        tier = get_tier_from_name(data["name"])
        tokenNum = data['name'].split("#")[-1].strip()
        price = calculate_price_based_on_tier(tier)
        tier_attr = get_tier_attr_from_tier(tier)

        # wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        # additem = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        # additem.click()
        driver.get(COLLECTION_URL + "assets/create")
        time.sleep(1)

        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        mediaSrc = data['image'] if data['animation_url'] is None else data['animation_url']
        extension = '.' + mediaSrc.split('.')[-1].strip()
        imagePath = IMAGE_FOLDER + str(tier) + '/' + tokenNum + extension  # change folder here
        imageUpload.send_keys(imagePath)
        if data['animation_url'] is not None:
            wait_css_selector('input[type="file"][name="preview"]')
            preview_image = driver.find_element_by_css_selector('input[type="file"][name="preview"]')
            preview_image_path = THUMBNAIL_FOLDER + 'tier-' + str(tier) + 'thumbnail-' + tokenNum + '.jpg'
            preview_image.send_keys(preview_image_path)

        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys(data["name"])  # +1000 for other folders #change name before "#"
        time.sleep(0.5)

        # ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
        # ext_link.send_keys(loop_external_link)
        # time.sleep(0.5)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(data["description"])
        time.sleep(0.5)

        prop_btn = driver.find_element_by_css_selector('button[aria-label="Add properties"]').click();
        wait_css_selector('div[role="dialog"]>header>h4')
        prop_inputs = driver.find_elements_by_css_selector('.AssetPropertiesForm--column input.browser-default.Input--input')
        prop_type = prop_inputs[0]
        prop_type.send_keys("Tier")
        prop_name = prop_inputs[1]
        prop_name.send_keys(tier_attr)
        driver.find_element_by_css_selector('div[role="dialog"]>footer>button').click()

        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        driver.execute_script("arguments[0].click();", create)
        time.sleep(3)

        wait_for_signature = driver.find_elements_by_css_selector('div[role="dialog"]>header>h4')
        if len(wait_for_signature) > 0 and wait_for_signature[0].text == 'Waiting for your wallet signature...':
            driver.switch_to.window(driver.window_handles[1])
            driver.refresh()
            wait_css_selector('button.btn-secondary[data-testid="request-signature__sign"]')
            driver.find_element_by_css_selector('button.btn-secondary[data-testid="request-signature__sign"]').click()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        wait_css_selector("i[aria-label='Close']")
        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
        cross.click()
        time.sleep(1)

        main_page = driver.current_window_handle
        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell.click()

        wait_css_selector("input[placeholder='Amount']")
        amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
        amount.send_keys(str(price))

        wait_css_selector("button[type='submit']")
        listing = driver.find_element_by_css_selector("button[type='submit']")
        listing.click()
        time.sleep(5)

        # wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        # sign = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        # sign.click()
        # time.sleep(2)
        
        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle
        # change the control to signin page
        driver.switch_to.window(login_page)
        driver.refresh()
        wait_css_selector("button[data-testid='request-signature__sign']")
        sign = driver.find_element_by_css_selector("button[data-testid='request-signature__sign']")
        sign.click()
        time.sleep(1)
        
        # change control to main page
        driver.switch_to.window(main_page)
        time.sleep(1)

        print('NFT creation completed!')