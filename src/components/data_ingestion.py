from src.exception.exception import customexception
from src.logger.logging import logging
import pandas as pd 
import numpy as np 
import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path
from datetime import date
import requests as rq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from time import sleep
import lxml
from lxml import html
from datetime import date






















def click_show_more(driver):
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="c8hZ6"]/div/div'))
        )

        # Scroll to the "Show More" button to make it clickable
        ActionChains(driver).move_to_element(show_more_button).perform()
        time.sleep(1)  # Add a small delay to ensure the button is clickable

        # Click the "Show More" button
        show_more_button.click()

        # You may need to wait for the new content to load before proceeding
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, 'loading_indicator_xpath')))
        
    except Exception as e:
        print(f"An error occurred while clicking 'Show More': {e}")

def get_airline(soup):
    #get airlines
    airlines=[]
    items=soup.find_all('div',class_='J0g6-operator-text') 
    for item in items :
        airl=item.text
        airl = airl.split(',')[0].strip()
        airlines.append(airl)
    
    return airlines

def get_duration(soup):
    #getduration
    durations=[]
    duration_div=soup.find_all('div',class_='xdW8 xdW8-mod-full-airport')
    for d in duration_div :
        duration=d.find('div',class_='vmXl vmXl-mod-variant-default').text
        durations.append(duration)
    return durations


def get_stops(soup):
    stops=[]
    stop_div=soup.find_all('div',class_='vmXl vmXl-mod-variant-default')
    for s in stop_div :
        selected_element = s.select_one('.JWEO-stops-text, .JWEO-mod-warning')
        if selected_element:
          stops.append(selected_element.text)

    return stops



def get_price(soup):   
    #getprice
    prices=[]
    price_div=soup.find_all('div',class_='f8F1-price-text-container')

    for p in price_div :
        price=p.find('div',class_='f8F1-price-text').text
        price= price.replace('\xa0', ' ')
        prices.append(price)
    return prices


def get_class(soup):
    #getclass
    classes=[]
    class_div=soup.find_all('div',class_='aC3z-option')
    for c in class_div :
        classe=c.find('div',class_='aC3z-name').text
        classes.append(classe)
    return classes


#get_depature_time
def get_dep_time(soup):
    deps=[]
    dep_div=soup.find_all('div',class_='vmXl vmXl-mod-variant-large')
    for d in dep_div:
        departure=d.find_all('span')
        deps.append(departure[0].text)
    return deps
#get_arrival_time
def get_arr_time(soup):
    arrs=[]
    arr_div=soup.find_all('div',class_='vmXl vmXl-mod-variant-large')
    for a in arr_div:
        arrival=a.find_all('span')
        arrs.append(arrival[2].text)
    return arrs



#you specify the sources destinations that the airline company has for simplification reasons we will consider one route. you could add more to the list. 
#
sources=['LAX']
destinations=['PAR']
classes=['economy','business']
departure_date=['2024-12-20']  ### for example we want to track the flight that has this departure date and gather historical data 



@dataclass

class DataIngestionConfig:
    raw_data_path:str=os.path.join("artifacts","raw.csv")
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")
    

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        

    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        logging.info("scrapping data started")
        try:
            df=pd.DataFrame(columns=["Airline", "Source", "Destination","Duration","stops","class","departure time","arrival time", "Price","Date"])
            for k in range(len(departure_date)): #replace testdate with dates_1 that is a list of our wanted dates
                for j in range(len(classes)):    
                    for i in range(len(sources)): 
                        for l in range(len(destinations)):
                            if sources[i]==destinations[l]:
                                continue
                            driver = webdriver.Edge()
                            kayak=f"https://www.kayak.ae/flights/{sources[i]}-{destinations[l]}/{departure_date[k]}/{classes[j]}?sort=bestflight_a"
                            print(departure_date[k])
                            print(sources[i])
                            print(destinations[l])
                            print(classes[j])
                            driver.get(kayak)
                            # Click "Show More" button
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'ULvh-button.show-more-button')))
                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                            airlines = get_airline(soup)
                            print(len(airlines))
                            stops = get_stops(soup)
                            print(len(stops))
                            dep_time=get_dep_time(soup)
                            print(len(dep_time))
                            arr_time =get_arr_time(soup)
                            print(len(arr_time))
                            prices = get_price(soup)
                            print(len(prices))
                            duration = get_duration(soup)
                            print(len(duration))
                            df = pd.concat([df,pd.DataFrame({
                                            'Airline': airlines,
                                            'Duration': duration,
                                            'stops' : stops,
                                            'class' : classes[j],
                                            'Source':sources[i],
                                            'Destination': destinations[l],
                                            'departure time' : dep_time ,
                                            'arrival time' : arr_time,
                                            'Price' : prices,
                                            'Date' : departure_date[k]})])


                            df = df.replace('\n','', regex=True)

                            print(f"Succesfully saved {sources[i]} => {destinations[l]} route  ")
                            driver.quit()
            current_date = date.today()
            df['search_date'] = current_date
            print(df)
            file_exists = os.path.isfile('mydata/forcasting_data.csv')

            df.to_csv('mydata/forcasting_data.csv', index=False, mode='a', header=not file_exists)

            driver.quit()


            logging.info("scrapping data finished")
            
            data= pd.read_csv('mydata/forcasting_data.csv')
            logging.info("reading a df")
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info(" i have saved the raw dataset in artifact folder")
            
            logging.info("here i have performed train test split")
            split_index = int(len(df) * 0.8)  # Use 80% of the data for training

            # Split the DataFrame into train and test sets
            train_data = data.iloc[:split_index]
            test_data = data.iloc[split_index:]
            logging.info("train test split completed")
            
            train_data.to_csv(self.ingestion_config.train_data_path,index=False)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False)
            
            logging.info("data ingestion part completed")
            
            return (
                 
                
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )



        except Exception as e:
            logging.info()
            raise customexception(e,sys)


#if __name__=="__main__":
 #   obj=DataIngestion()

  #  obj.initiate_data_ingestion()


