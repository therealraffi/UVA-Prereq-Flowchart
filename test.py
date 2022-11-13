import requests
from bs4 import BeautifulSoup

page = requests.get("https://sisuva.admin.virginia.edu/psp/ihprd/UVSS/SA/s/WEBLIB_HCX_GN.H_DASHBOARD.FieldFormula.IScript_Main")
print(text)
soup = BeautifulSoup(page.content, "html.parser")
