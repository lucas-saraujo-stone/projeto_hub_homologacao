import time
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9111")
#Change chrome driver path accordingly
chrome_driver = "C:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options)
print(driver.title)
print(driver.session_id)

xpath_setup = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[1]/ul[2]/li/a/span")
xpath_setup.click()

status_versao = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/div[2]/select")
status_versao.click()

validacao_integracao = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/div[2]/select/option[2]")
validacao_integracao.click()

time.sleep(3)
botao_buscar = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/button[1]")
botao_buscar.click()
