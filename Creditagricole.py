import webbrowser
import sys
import os
import json
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

identifiant = "11987944100" # INSERER VOTRE IDENTIFIANT
password = [1, 2, 3, 4, 5, 6] # INSERER VOTRE PASSWORD
path = "Users/Documents/python/" # LIEN DE VOTRE PROJET PYTHON
driver = webdriver.Chrome()
driver.get('https://www.credit-agricole.fr/ca-norddefrance/professionnel/acceder-a-mes-comptes.html?resource=%2Fca-norddefrance%2Fprofessionnel%2Foperations%2Fsynthese.html')
login_account = driver.find_element_by_id("Login-account")
login_account.send_keys(identifiant)
login_button = driver.find_element_by_xpath("//button[@class='btn btn-primary col-xs-12 Login-button']")
login_button.click()
time.sleep(2)
# TAPPE SUR LE CLAVIER VIRTUEL 6 FOIS POUR FAIRE CROIRE QUE L'ON INSCRIT LE PASSWORD
for i in range(6):
    button = driver.find_element_by_xpath('//*[@id="clavier_num"]/div[1]/div/div/a[1]')
    button.click()

# Récupérer le code
keypad_divs = driver.find_elements_by_css_selector("div.Login-keypad")
chiffres = []
for div in keypad_divs:
    chiffre_divs = div.find_elements_by_css_selector("div[data-pos]")
    for chiffre_div in sorted(chiffre_divs, key=lambda x: int(x.get_attribute("data-pos"))):
        chiffres.append(chiffre_div.text)
code = "".join(chiffres)
print(code)

# Créer un dictionnaire qui mappe chaque chiffre du code à un chiffre de votre choix
correspondance = {}
for i in range(len(code)):
    correspondance[str(i)] = str(int(code[i]))

print(correspondance)

a_trouver = password
correspondance_inverse = dict((v, k) for k, v in correspondance.items())
correspondance_liste = [correspondance_inverse[str(chiffre)] for chiffre in a_trouver]
print(correspondance_liste)

js_script = f'document.getElementById("j_password").value = JSON.parse(\'{json.dumps(correspondance_liste)}\').join(",");'
driver.execute_script(js_script)
element = driver.find_element_by_xpath('//*[@id="validation"]')
element.click()
time.sleep(2)
element2 = driver.find_element_by_xpath('//*[@id="popin_tc_privacy_button_2"]')
element2.click()
