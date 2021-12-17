from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time 
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser
import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




class agent:
   
    # init method or constructor 
    def __init__(self, driver, name="", barcode="", unlinkbarcode=""):
        self.driver = driver
        self.name = name
        self.barcode =  barcode
        self.unlinkbarcode = unlinkbarcode
        self.email_content = ""
    
    def add_jpg(self,photo):
        loc = pyautogui.center(pyautogui.locateOnScreen(photo,grayscale=True,  confidence=.9))
        pyautogui.click(loc)
    
    def close_driver(self):
        driver.close()

    
    def login(self):
    
        driver.get("http://sonamu.int.kn/inventory/login.jsp")

        username = driver.find_element_by_id("j_username")

        password = driver.find_element_by_id("j_password")

        button_login = driver.find_element_by_id("button_login")

        username.send_keys("")
        password.send_keys("")

        time.sleep(1)

        button_login.click()

    def show_detail(self):
        try:
            driver.find_element_by_link_text("Show Detail").click()
    
        except:
            time.sleep(0.5)
            driver.find_element_by_xpath("//li[@class='dropdown']/a[@id='selectLocationPopup']").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//div[@id='s2id_accessStationList']/a/div/b").click()
            time.sleep(0.5)
            try:
                driver.find_element_by_xpath("//div/ul/li/div[@class='select2-result-label']").click()
            except:
                print("fkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            time.sleep(0.5)
            driver.find_element_by_link_text("Show Detail").click()

    def selectPool(self,Pool):
        driver.find_element_by_xpath("//a[@class='select2-choice select2-default']/div/b").click()
        driver.find_element_by_xpath("//div[text()='{}']".format(Pool)).click()
        time.sleep(0.5)
        driver.find_element_by_xpath("//a[@onclick='return false;']/span[text()='Select a user by enter their user name or full name (You must be select a station and hardware pool before)']").click()
        
        driver.find_element_by_xpath("//div[@class='select2-drop select2-with-searchbox select2-drop-active']/div/input[@class='select2-input select2-focused']").send_keys(self.name)
        time.sleep(0.5)
        driver.find_element_by_xpath("//li[@class='select2-results-dept-0 select2-result select2-result-selectable select2-highlighted']").click()
        driver.find_element_by_xpath("//input[@id='transfer']").click()
        self.email_content += "{} has been tranfer to {}".format(self.barcode,self.name)
        self.email_content += "\n"
    

    def unlink(self,barcode):

        self.unlinkbarcode =  barcode

        self.login()
        
        driver.get("http://sonamu.int.kn/inventory/iu/hardwareSearch_searchResult.action?hardware.hardwareTypeDts.hardwareDeviceDts.id=&hardware.hardwareTypeDts.brandName=&hardware.knAssetNo=&expiryDateFrom=&purchaseDateFrom=&hardware.status=&hardware.hardwareTypeDts.modelNumber=&hardware.barcode={}&expiryDateTo=&purchaseDateTo=&hardware.hardwarePoolDts.id=&hardware.serialNumber=&hardware.remarks=".format(self.unlinkbarcode))

        self.show_detail()
        time.sleep(0.5)
        driver.find_element_by_xpath("//input[@value='UnLink']").click() 
        time.sleep(1)
        pyautogui.click(x=100, y=500)
        time.sleep(1)

        driver.find_element_by_xpath("//input[@value='Recieved']").click() 

        self.email_content += "{} has been unlinked".format(self.unlinkbarcode)
        self.email_content += "\n"

        

    def tranfer(self,name,barcode,HKG_or_AP,Pool):

        self.name = name
        self.barcode = barcode

        self.login()

        driver.get("http://sonamu.int.kn/inventory/iu/hardwareSearch_searchResult.action?hardware.hardwareTypeDts.hardwareDeviceDts.id=&hardware.hardwareTypeDts.brandName=&hardware.knAssetNo=&expiryDateFrom=&purchaseDateFrom=&hardware.status=&hardware.hardwareTypeDts.modelNumber=&hardware.barcode={}&expiryDateTo=&purchaseDateTo=&hardware.hardwarePoolDts.id=&hardware.serialNumber=&hardware.remarks=".format(self.barcode))

        self.show_detail()
        driver.find_element_by_xpath("//input[@value='Transfer']").click()
        time.sleep(1)
        if HKG_or_AP=="HKG":
            self.selectPool(Pool)
            
        else:
            driver.find_element_by_xpath("//div[@id='s2id_allowTransferStationList']/a/div/b").click()
            driver.find_element_by_xpath("//ul/li[2]/div").click()
            self.selectPool(Pool)
            
            



    def show_user_detail(self,name):

        self.name = name

        self.login()

        driver.get("http://sonamu.int.kn/inventory/iu/userSearch_searchResult.action?knuser.userType.id=&knuser.department=&knuser.userName={}&excludeResignUser=true&knuser.kncode=&knuser.staffNo=&knuser.email=".format(self.name))

        self.show_detail()

        
        userdata = driver.find_elements_by_xpath("//table[@id='hardwareSoftwareDisplayTable']/tbody")
        for s in userdata:
            print(s.text)
        

    def check_current_user(self,barcode):
        self.barcode =  barcode
        self.login()

        driver.get("http://sonamu.int.kn/inventory/iu/hardwareSearch_searchResult.action?hardware.hardwareTypeDts.hardwareDeviceDts.id=&hardware.hardwareTypeDts.brandName=&hardware.knAssetNo=&expiryDateFrom=&purchaseDateFrom=&hardware.status=&hardware.hardwareTypeDts.modelNumber=&hardware.barcode={}&expiryDateTo=&purchaseDateTo=&hardware.hardwarePoolDts.id=&hardware.serialNumber=&hardware.remarks=".format(self.barcode))

        self.show_detail()

        #driver.save_screenshot("screenshot.png")

        try:
            userdata = driver.find_elements_by_xpath("//table[@class='table table-striped']")
            for s in userdata:
                print(s.text)  
            print(" End")
                    
        except:
            print("no current user")
        #driver.close()
        #driver.quit()

    def send_email(self):
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = "Tom inventory record"  #郵件標題
        content["from"] = "shingshing125@gmail.com"  #寄件者
        content["to"] = "tom.chan@kuehne-nagel.com" #收件者
        content.attach(MIMEText(self.email_content))  #郵件內容
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("shingshing125@gmail.com", "")  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)

        


    
        
chrome_options = Options()
chrome_options.add_argument("--window-size=1000,1000")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)



bot = agent(driver)

bot.unlink("hkg22100326")
bot.tranfer("tom.chan","hkg22100326","HKG","NC Spare Pool")

#bot.unlink("HKGU2100218")
#bot.tranfer("ryan.chung","HKGU2100218","AP","AP Spare Pool")

#bot.unlink("HKG22100421")
#bot.tranfer("joey.yam","HKG22100421","HKG","FA Spare Pool")
	
#bot.check_current_user("hkg22100326")
#bot.show_user_detail("tom.chan")
#bot.show_user_detail("ryan.chung")
#print(bot.email_content)
bot.send_email()


bot.close_driver()





