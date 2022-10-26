import os
from time import sleep
from sys import exit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk

driverpath = os.path.abspath(os.sep) + 'chromedriver.exe'

browser = webdriver.Chrome(executable_path=driverpath)

# killswitch
def closeProgram():
    browser.quit()
    exit()

# opens a new Chrome window for each item
def search():
    items = inputText.get(1.0,"end-1c").split('\n')
    i = 0

    marketplaceSelection = marketplace.get()

    while i < (len(items)):
        if items[i] != "":
            match marketplaceSelection:

                case "Google":
                    browser.get('https://shopping.google.com')
                    sleep(1)
                    searchbar = browser.find_element(By.XPATH, '/html/body/c-wiz[1]/div/div/c-wiz/form/div[2]/div[1]/input')
                
                case "Amazon":
                    browser.get('https://www.amazon.com')
                    sleep(1)
                    searchbar = browser.find_element(By.XPATH, '/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input')
                
                case "Ebay":
                    browser.get('https://ebay.com')
                    sleep(1)
                    searchbar = browser.find_element(By.XPATH, '/html/body/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')
            
            searchbar.click()
            searchbar.send_keys(items[i])
            searchbar.send_keys(Keys.ENTER)

            # Saves window opener;
            # unsure if relevant past current iteration of while loop
            currentWindow = browser.current_window_handle

            # TODO: figure out iterating thru next item once new tab is open
            """
            browser.execute_script("window.open('https://shopping.google.com', 'new_window')")
            browser.switch_to_window(browser.window_handles[0])
            """

            

            #print(browser.current_url)

            sleep(1)
            i+= 1

# GUI
frame = tk.Tk()
frame.title("Price Finder")
frame.configure(bg='#6a6a6a')
frame.resizable(False,False)

inputLabel = tk.Label(frame,text="Products:")
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

searchButton = tk.Button(frame,text="Search", command=search)
searchButton.configure(bg='#898989', fg='#f0f0f0')
searchButton.pack(pady=6)

frame.protocol("WM_DELETE_WINDOW", closeProgram)
frame.mainloop()