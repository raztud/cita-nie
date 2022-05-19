import os
import random
import time
from datetime import datetime
from shutil import which


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

from constants import START_PAGE, CERTIFICADOS_ASIGNACION_NIE, PASSPORT
from cita_information import PASSPORT_NUMBER, PERSON_NAME


def log(txt):
    now = datetime.now()
    date_time = now.strftime("%H:%M:%S")
    print(f"{date_time} {txt}")


def select_province(province_name: str):
    check_too_many_requests()
    select = Select(driver.find_element(by=By.ID, value="form"))
    select.select_by_visible_text(province_name)

    time.sleep(random.randint(2, 5))
    btn_accept = driver.find_element(by=By.ID, value="btnAceptar")
    btn_accept.click()


def select_certificate(certificate_type: str):
    check_too_many_requests()
    select_id = "tramiteGrupo[0]"
    select = Select(driver.find_element(by=By.ID, value=select_id))
    select.select_by_value(certificate_type)

    driver.execute_script("javascript:envia()")
    time.sleep(random.randint(2, 5))

    driver.execute_script("javascript:document.forms[0].submit()")


def fill_passport(passport_no, name):
    # select radio button rdbTipoDocPas
    radio_btn = driver.find_element(by=By.ID, value="rdbTipoDocPas")
    radio_btn.click()

    # fill passport number in txtIdCitado
    driver.find_element(by=By.ID, value="txtIdCitado").send_keys(passport_no)

    # fill name in txtDesCitado
    driver.find_element(by=By.ID, value="txtDesCitado").send_keys(name)
    time.sleep(random.randint(2, 5))
    driver.execute_script("javascript:envia()")
    time.sleep(random.randint(2, 5))
    driver.execute_script("javascript:enviar('solicitud')")


def fill_documents(doc_type: str, doc_no: str, name: str):
    if doc_type == PASSPORT:
        fill_passport(doc_no, name)
    else:
        raise NotImplementedError()


def refresh_page(refresh_count, start_count):
    check_too_many_requests()

    time.sleep(random.randint(5, 10))

    txt = "En este momento no hay citas disponibles."
    txt_provincias = "PROVINCIAS DISPONIBLES"
    page_source = driver.page_source

    if txt in page_source:
        log("No appointments available")
        refresh_count += 1
        log(f"Refreshing... {refresh_count}")

        driver.refresh()

        refresh_page(refresh_count, start_count)
    elif txt_provincias in page_source:
        start_count += 1
        start_process(start_count)
    else:
        speak("Found! Take action")
        time.sleep(120)


def speak(word):
    if which("espeak") is not None:
        os.system("espeak '" + word + "'")
    elif which("say") is not None:
        os.system("say '" + word + "'")
    elif which("wsay") is not None:
        os.system('wsay "' + word + '"')
    else:
        log(word)


def check_too_many_requests():
    while True:
        if "Too Many Requests" in driver.page_source:
            wait_time = random.randint(5, 10)
            log(f"Too Many Requests. Wait {wait_time} minutes...")
            time.sleep(60 * wait_time)
        else:
            break


def start_process(start_count):
    start_count += 1
    log(f"[Re]start {start_count}")
    check_too_many_requests()

    select_province(province)
    select_certificate(CERTIFICADOS_ASIGNACION_NIE)

    fill_documents(PASSPORT, PASSPORT_NUMBER, PERSON_NAME)

    refresh_page(refresh_count=0, start_count=start_count)


if __name__ == "__main__":
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    province = "Barcelona"
    driver.get(START_PAGE)

    try:
        start_process(start_count=0)
    except:
        speak("Process failed")
        
