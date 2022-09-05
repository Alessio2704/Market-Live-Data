from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import multiprocessing

field_names = ["ticker","time","price"]
with open("data.csv","w") as csv_file:
    csv_writer = csv.DictWriter(csv_file,fieldnames=field_names)
    csv_writer.writeheader()


def getQuote(ticker,exchange=None):
    service = Service("/Users/alessiomarcuzzi/Downloads/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("headless") 
    driver = webdriver.Chrome(service=service,options=options)
    url = f"https://it.tradingview.com/symbols/{ticker}/?exchange={exchange}"
    driver.implicitly_wait(10)
    driver.get(url)
    price_initial = float(driver.find_element(By.XPATH,'//*[@id="anchor-page-1"]/div/div[3]/div[1]/div/div/div/div[1]/div[1]').text)
    while True:
        price = float(driver.find_element(By.XPATH,'//*[@id="anchor-page-1"]/div/div[3]/div[1]/div/div/div/div[1]/div[1]').text)
        if price != price_initial:
            time_now = datetime.now().strftime("%H:%M:%S")
            with open("data.csv","a") as csv_file:
                csv_writer = csv.DictWriter(csv_file,fieldnames=field_names)
                csv_writer.writerow({"ticker":ticker,"time":time_now,"price":price})
            price_initial = price
        else:
            pass

def animate(i,ticker):
    data = pd.read_csv("data.csv")
    x = data["time"]
    y = data["price"]
    plt.cla()
    plt.plot(x,y)
    plt.title(ticker.upper())
    plt.gca().axes.xaxis.set_visible(False)

def mainFunc(ticker):
    ani = FuncAnimation(plt.gcf(),animate,interval=1000,fargs=[ticker])
    plt.show()

if __name__ == '__main__':
    ticker = input("Ticker: ")
    exchange = input("Exchange(optional): ")
    p1 = multiprocessing.Process(target=getQuote,args=[ticker,exchange])
    p2 = multiprocessing.Process(target=mainFunc,args=[ticker])
    p1.start()
    p2.start()     
    p1.join()
    p2.join()
