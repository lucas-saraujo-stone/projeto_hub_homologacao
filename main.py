import time
import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import download
import apk_informacoes
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from versionamento import Versionamento

#Padronizar a pasta de downloads e entender porque o debuggerAddress não funciona corretamente em conjunto

def main():
    chrome_options = Options()
    '''chrome_options.debugger_address = "127.0.0.1:9111"
    chrome_prefs = {
        "download.default_directory": "C:\Downloads",  # Altere para a pasta desejada
        "download.prompt_for_download": False,  # Desativa o pop-up de confirmação
        "download.directory_upgrade": True,    # Permite atualização de diretório
        "safebrowsing.enabled": True,           # Evita bloqueios do Chrome para downloads
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)'''
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9111")
    #Change chrome driver path accordingly
    #Executar no CMD: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9111 --user-data-dir="C:\selenum\ChromeProfile"
    chrome_driver = "C:\chromedriver\chromedriver.exe"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://partnerhub.stone.com.br/#/integration")
    time.sleep(3)

    xpath_setup = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[1]/ul[2]/li/a/span")
    xpath_setup.click()

    status_versao = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/div[2]/select")
    status_versao.click()

    validacao_integracao = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/div[2]/select/option[2]")
    validacao_integracao.click()

    time.sleep(3)
    botao_buscar = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/button[1]")
    botao_buscar.click()
    time.sleep(3)

    tabela = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table")
    linhas = tabela.find_elements(By.TAG_NAME,"tr")

    #lista_versionamentos = []
    apk_baixado = None

    for linha in linhas[1:]:
        texto_linha = linha.text
        lista_colunas = texto_linha.split('\n')
        location = linha.location
        size = linha.size
        produto = lista_colunas[0]
        tipo = lista_colunas[1]
        if produto == "SDK Android" and tipo == "Versionamento":
            nome_aplicacao = lista_colunas[2]
            parceiro = lista_colunas[4]
            status = lista_colunas[9]
            eixo_x = location['x'] + size['width'] / 2  # Centro do elemento no eixo X
            eixo_y = location['y'] + size['height'] / 2  # Centro do elemento no eixo Y
            actions = ActionChains(driver)
            actions.move_by_offset(eixo_x, eixo_y).click().perform()

            versionamento = Versionamento(nome_aplicacao, parceiro, status)

            botao_app_download = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table/tbody[1]/tr[2]/td/app-application-approval-detailed-information/div/div[2]/div/div/div/div[2]/div[1]/div[4]/button/i")))
            #botao_app_download = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table/tbody[1]/tr[2]/td/app-application-approval-detailed-information/div/div[2]/div/div/div/div[2]/div[1]/div[4]/button/i")
            botao_app_download.click()

            # Após acionar o download via Selenium
            pasta_download = r"C:\Users\lucas.saraujo\Downloads"
            try:
                time.sleep(2)
                apk_baixado = download.espera_pelo_download(pasta_download)
                print(f"Arquivo baixado: {apk_baixado}")
                apk_informacoes.tamanho_apk(apk_baixado, versionamento)
                apk_informacoes.dados_apk(apk_baixado, versionamento)

                #TESTE RECUSA
                '''botao_recusar_homologacao = driver.find_element(By.XPATH,
                    "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table/tbody[1]/tr[2]/td/app-application-approval-detailed-information/div/div[2]/div/div/div/div[3]/div/div/div/button[1]/span")
                botao_recusar_homologacao.click()
                area_justificativa_recusa = driver.find_element(By.NAME, "justification")
                area_justificativa_recusa.send_keys("Teste de recusa!")'''

                #TESTE ACEITA
                botao_aprovar_homologacao = driver.find_element(By.XPATH,
                    "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table/tbody[1]/tr[2]/td/app-application-approval-detailed-information/div/div[2]/div/div/div/div[3]/div/div/div/button[3]/span")
                botao_aprovar_homologacao.click()
                botao_confirmar_homologacao = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                     "/html/body/ngb-modal-window/div/div/confirm-modal/div/div[2]/button[2]")))
                actions.move_to_element(botao_confirmar_homologacao).click().perform()

                break
            except TimeoutError as e:
                print(str(e))
            finally:
                os.remove(apk_baixado)


    print("Fim")


if __name__ == "__main__":
    main()

#https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test
#https://googlechromelabs.github.io/chrome-for-testing/#stable
#https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
#https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/

