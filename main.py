import os
import csv
from sys import exit
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#TODO: pip install selectorlib, might use for web scraping search results
#import selectorlib


urlList = []
driverpath = os.path.abspath(os.sep) + 'chromedriver.exe'

browser = webdriver.Chrome(executable_path=driverpath)

# killswitch
def closeProgram():
    browser.quit()
    exit()

# opens a new Chrome window for each item
def searchItems():
    items = list(filter(None, inputText.get(1.0,"end-1c").split('\n')))
    i = 0

    marketplaceSelection = marketplace.get()

    while i < (len(items)):           
        if(i > 0):
            browser.execute_script("window.open('', 'new_window')")

        match marketplaceSelection:

            case "Google":
                marketplaceUrl = 'https://shopping.google.com'
                if (i==0):
                    browser.get(marketplaceUrl)
                else:
                    browser.switch_to.window(browser.window_handles[-1])
                    browser.get(marketplaceUrl)
                
                browser.implicitly_wait(0.5)
                searchbar = browser.find_element(By.XPATH, '/html/body/c-wiz[1]/div/div/c-wiz/form/div[2]/div[1]/input')
                typeItem(searchbar, items[i])
            
            case "Amazon":
                marketplaceUrl = 'https://www.amazon.com'
                if (i==0):
                    browser.get(marketplaceUrl)
                else:
                    browser.switch_to.window(browser.window_handles[-1])
                    browser.get(marketplaceUrl)
                
                browser.implicitly_wait(0.5)
                searchbar = browser.find_element(By.XPATH, '/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input')
                typeItem(searchbar, items[i])
            
            case "Ebay":
                marketplaceUrl = 'https://ebay.com'
                if (i==0):
                    browser.get(marketplaceUrl)
                else:
                    browser.switch_to.window(browser.window_handles[-1])
                    browser.get(marketplaceUrl)
                
                browser.implicitly_wait(0.5)
                searchbar = browser.find_element(By.XPATH, '/html/body/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')
                typeItem(searchbar, items[i])

        # Saves window opener
        # unsure if relevant past current iteration of while loop
        currentWindow = browser.current_window_handle

        #print(browser.current_url)
        urlList.append(browser.current_url)

        browser.implicitly_wait(0.5)
        i+= 1
    
    for i in items:
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])

def typeItem(searchElement, searchText):
    searchElement.click()
    searchElement.send_keys(searchText)
    searchElement.send_keys(Keys.ENTER)

def savePrices():
    print(urlList)

    # TODO: Figure out writing each url in urlList to csv output file
    
    with open('pricefinderresults.csv', mode='w') as results_file:
        writer = csv.writer(results_file, delimiter=',', quotechar='"')
        writer.writerow(urlList)
    

# GUI
frame = tk.Tk()
frame.title("Price Finder")
frame.configure(bg='#6a6a6a')
frame.resizable(False,False)

searchButton = tk.Button(frame,text="Search", command=searchItems)
searchButton.configure(bg='#898989', fg='#f0f0f0')
searchButton.pack(pady=6)

saveButton = tk.Button(frame,text="Save", command=savePrices)
saveButton.configure(bg='#898989', fg='#f0f0f0')
saveButton.pack(pady=6)

inputLabel = tk.Label(frame,text="Products:")
inputLabel.configure(bg='#6a6a6a', fg='#f0f0f0')
inputLabel.pack(pady=3)

inputText = tk.Text(frame, height=20, width=17)
inputText.configure(bg='#898989', fg='#f0f0f0')
inputText.pack(pady=3,padx=6)

marketplace = tk.StringVar(frame, "Google")
marketplaceLabel = tk.Label(frame, text="Marketplace:")
marketplaceLabel.configure(bg='#6a6a6a', fg='#f0f0f0')
marketplaceLabel.pack(pady=6)

googleRadiobutton = tk.Radiobutton(frame, text = "Google", variable = marketplace, value = "Google",
    indicator = 0, background = '#6a6a6a', foreground = '#000000').pack(pady=3)
amazonRadiobutton = tk.Radiobutton(frame, text = "Amazon", variable = marketplace, value = "Amazon",
    indicator = 0, background = '#6a6a6a', foreground = '#000000').pack(pady=3)
ebayRadiobutton = tk.Radiobutton(frame, text = "Ebay", variable = marketplace, value = "Ebay",
    indicator = 0, background = '#6a6a6a', foreground = '#000000').pack(pady=3)

frame.protocol("WM_DELETE_WINDOW", closeProgram)
frame.mainloop()