from selenium import webdriver
from tkinter import filedialog
import time

file = filedialog.askopenfile(mode='r')

#Hiding Process
options = webdriver.ChromeOptions()
options.add_argument('headless')


driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://www.virustotal.com/gui/')

time.sleep(2)

def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

shadow_section = expand_shadow_element(driver.find_element_by_tag_name("home-view"))
upload_shadow =  expand_shadow_element(shadow_section.find_element_by_tag_name("vt-ui-main-upload-form"))
upload_shadow.find_element_by_id('fileSelector').send_keys(file.name)

time.sleep(1)

try:
    upload_shadow.find_element_by_id('confirmUpload').click()
except Exception as e:
    print(e)

time.sleep(30)

main_shell = expand_shadow_element(driver.find_element_by_tag_name("vt-ui-shell"))
file_shell = expand_shadow_element(driver.find_element_by_tag_name("file-view"))
report_shell = expand_shadow_element(file_shell.find_element_by_tag_name("vt-ui-main-generic-report"))
detection_list_shell = expand_shadow_element(file_shell.find_element_by_tag_name("vt-ui-detections-list"))
card_shell = expand_shadow_element(file_shell.find_element_by_tag_name("vt-ui-file-card"))
generic_card_shell = expand_shadow_element(card_shell.find_element_by_tag_name("vt-ui-generic-card"))

detection = card_shell.find_element_by_class_name('detections').find_element_by_tag_name('p').text

engines = detection_list_shell.find_elements_by_class_name('engine-name')
about = detection_list_shell.find_elements_by_class_name('individual-detection')

print(f"{detection}\n")

for engine, info in zip(engines, about):
    print(f"{engine.text} - {info.text}")