from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from pathlib import Path
from time import sleep

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


def abrir_janela_whatsapp():
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, timeout=60)
    barra_lateral = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]')))
    driver.implicitly_wait(2)

def abrir_janel_de_conversa(nome_contato):
    barra_pesquisa = driver.find_element(By.XPATH, '//div[@title="Caixa de texto de pesquisa"]')
    barra_pesquisa.send_keys(Keys.CONTROL + 'a')
    barra_pesquisa.send_keys(Keys.DELETE)

    barra_pesquisa = driver.find_element(By.XPATH, '//div[@title="Caixa de texto de pesquisa"]')
    barra_pesquisa.send_keys(nome_contato)

    wait = WebDriverWait(driver, timeout=2)
    span_buscando = f'//span[@title="{nome_contato}"]'
    conversa_lateral = wait.until(EC.presence_of_element_located((By.XPATH, span_buscando)))
    conversa_lateral.click()

def sai_das_conversas():
    barra_pesquisa = driver.find_element(By.XPATH, '//div[@title="Caixa de texto de pesquisa"]')
    barra_pesquisa.send_keys(Keys.CONTROL + 'a')
    barra_pesquisa.send_keys(Keys.DELETE)
    barra_pesquisa.send_keys(Keys.ESCAPE)

def envia_mensagem(mensagem):
    barra_de_mensagem = driver.find_element(By.XPATH, '//div[@title="Digite uma mensagem"]')
    barra_de_mensagem.send_keys(mensagem)
    barra_de_mensagem.send_keys(Keys.RETURN)

def envia_documentos(caminho_do_documento):
    botao_anexos = driver.find_element(By.XPATH, '//div[@title="Attach" or @title="Anexar"]')
    botao_anexos.click()

    botao_documentos = driver.find_element(By.XPATH, '//input[@accept="*" and @type="file"]')
    botao_documentos.send_keys(caminho_do_documento)

    bota_enviar = driver.find_element(By.XPATH, '//div[@aria-label="Enviar"]')
    bota_enviar.click()

def envia_imagem(caminho_imagem):
    botao_anexos = driver.find_element(By.XPATH, '//div[@title="Attach" or @title="Anexar"]')
    botao_anexos.click()

    botao_fotos = driver.find_element(By.XPATH, '//span[text()="Fotos e vídeos"]/../input')
    botao_fotos.send_keys(caminho_imagem)

    botao_enviar = driver.find_element(By.XPATH, '//div[@aria-label="Enviar"]')
    botao_enviar.click()

if __name__ == '__main__':

    contatos = ['Cliente 1', 'Cliente 2', 'Cliente 3']
    caminho_catalogo = str(Path(__file__).parent.parent / 'catalogo.pdf')
    mensagem = """
    Olá {}!

    Foi um prazer conhecê-lo.

    Envio um catálogo dos nossos produtos, para que você possa explorá-lo.

    Um abraço!
    """

    abrir_janela_whatsapp()

    for contato in contatos:
        abrir_janel_de_conversa(contato)
        sleep(1)
        envia_mensagem(mensagem.format(contato))
        sleep(1)
        envia_documentos(caminho_catalogo)
        sleep(1)
        sai_das_conversas()
        sleep(1)
    
    sleep(200)




