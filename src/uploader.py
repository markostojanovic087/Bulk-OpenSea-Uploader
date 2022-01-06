from selenium import webdriver
from time import sleep
import os
import uploadui

class Uploader:
    def __init__(self):
        # Get the base directories
        bin_base = os.path.join(os.getcwd(), "bin")
        chromedriver_path = os.path.join(bin_base, "chromedriver")
        ext_path = os.path.join(bin_base, "metamask.crx")
        self.__METAMASK_URL = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html"
        self.__METAMASK_ID = "nkbihfbeogaeaoehlefnkodbefgpgknn"
        self.__collection_url = ""

        # Initialize the driver
        opt = webdriver.ChromeOptions()
        opt.add_extension(extension=ext_path)
        opt.add_argument('--log-level=3')
        self.__driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=opt)

        # Close the metamask popup and navigate back to the correct window
        sleep(2)
        self.__driver.switch_to.window(self.__driver.window_handles[0])
        self.__driver.close()
        self.__driver.switch_to.window(self.__driver.window_handles[0])


    def connect_metamask(self, seed_phrase: str, password: str):
        '''
        Connect to Metamask
        '''

        # Navigate to metamask screen
        self.__driver.get(f"{self.__METAMASK_URL}#initialize/welcome")
        sleep(1)

        # Skip through wallet setup screen
        self.__driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/button').click()
        self.__driver.find_element_by_css_selector('button.first-time-flow__button:first-of-type').click()
        self.__driver.find_element_by_css_selector('button.btn-primary[data-testid="page-container-footer-next"]').click()
        sleep(0.5)

        # Enter wallet seed phrase and password
        self.__driver.find_element_by_css_selector('input.MuiInputBase-input:first-of-type').send_keys(seed_phrase)
        self.__driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        self.__driver.find_element_by_xpath('//*[@id="confirm-password"]').send_keys(password)
        self.__driver.find_element_by_css_selector('.first-time-flow__form>.first-time-flow__checkbox-container>.first-time-flow__checkbox').click()
        self.__driver.find_element_by_css_selector('.btn-primary').click()
        sleep(2)

    def set_network(self, rpc_url: str, chain_id: int, preconfigured_network: int = None):
        '''
        Sets the specified network to Metamask and selects it. Also adds it if it is not a default network.
        '''

        # Go to the networks tab
        self.__driver.get("data:")
        self.__driver.get(f"{self.__METAMASK_URL}#settings/networks")
        sleep(1.5)

        # Choose one of the preconfigured networks if specified
        if preconfigured_network == None:
            self.__driver.find_element_by_css_selector('.color-indicator--color-rinkeby').click()
            self.__driver.find_element_by_xpath('//*[@id="network-name"]').send_keys("Network")
            self.__driver.find_element_by_xpath('//*[@id="rpc-url"]').send_keys(rpc_url)
            self.__driver.find_element_by_xpath('//*[@id="chainId"]').send_keys(chain_id)
            self.__driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[7]/button[2]').click()
            preconfigured_network = 7

        # Select the network
        self.__driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div').click()
        self.__driver.find_element_by_xpath(f'//*[@id="app-content"]/div/div[3]/div/li[{preconfigured_network}]').click()
        sleep(2)

    def open_metamask(self):
        '''
        Open Metamask in new window
        '''

        # Open the extension in a new tab and switch back
        self.__driver.execute_script("window.open('');")
        self.__driver.switch_to.window(self.__driver.window_handles[1])
        self.__driver.get(f"chrome-extension://{self.__METAMASK_ID}/popup.html")
        self.__driver.switch_to.window(self.__driver.window_handles[0])

    def __metamask_execute(self, fn):
        '''
        Execute an operation within Metamask and then switch back
        '''

        self.__driver.switch_to.window(self.__driver.window_handles[1])
        self.__driver.refresh()
        sleep(2)
        fn()
        sleep(2)
        self.__driver.switch_to.window(self.__driver.window_handles[0])

    def connect_opensea(self, test: bool):
        '''
        Connect OpenSea with Metamask
        '''

        self.__driver.get("https://testnets.opensea.io/login" if test else "https://opensea.io/login")
        sleep(2)
        self.__driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div/div[2]/ul/li[1]/button').click()
        sleep(1)
        def connect():
            self.__driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]').click()
            self.__driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
            sleep(2)
        self.__metamask_execute(connect)

    def sign_transaction(self):
        def sign():
            self.__driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]').click()
            sleep(1)
        self.__metamask_execute(sign)

    def set_collection_url(self, collection_url: str):
        '''
        Sets the OpenSea collection URL to upload to
        '''

        self.__collection_url = collection_url

    def upload_old(self, asset_path: str, name: str):
        '''
        Upload a single NFT to OpenSea.
        '''

        # Add an item to the collection
        self.__driver.get(f"{self.__collection_url}/assets/create")
        sleep(1)

        # Input the data
        self.__driver.find_element_by_xpath('//*[@id="media"]').send_keys(asset_path)
        self.__driver.find_element_by_xpath('//*[@id="name"]').send_keys(name)

    def upload(self, metadata):
        uploadui.upload_ui(self.__driver, metadata)

    def close(self):
        for window_handle in self.__driver.window_handles:
            self.__driver.switch_to.window(window_handle)
            self.__driver.close()