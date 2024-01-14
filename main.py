import time

from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import pandas as pd


photo_links = []
mobile_links = []
mobile_names = []
mobile_prices = []


link = "https://www.amazon.eg"
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
driver.get("https://www.amazon.eg/")
driver.find_element(By.LINK_TEXT, 'موبايلات').click()
driver.find_element(By.CSS_SELECTOR, '#apb-desktop-browse-search-see-all > span').click()

while True:
    try:
        # time.sleep(25)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        mobiles = soup.find_all("div", {'class': 'a-section a-spacing-base'})
        for mobile in mobiles:
            photo_link = mobile.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            mobile_link = \
            mobile.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})[
                'href']
            mobile_name = mobile.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text

            try:
                mobile_price = mobile.find('div', {'class': 'a-row a-size-base a-color-secondary'}).text
            except:
                mobile_price = mobile.find('span', {'class': 'a-price-whole'}).text + " Eg "

            # Append data to lists
            photo_links.append(link + photo_link)
            mobile_links.append(link + mobile_link)
            mobile_names.append(mobile_name)
            mobile_prices.append(mobile_price)


        check = input(" Do you want to get data from the next page Y or N ")
        if check.capitalize() == 'Y':

            driver.find_element(By.CSS_SELECTOR,
                        '#search > div.s-desktop-width-max.s-desktop-content.s-wide-grid-style-t1.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(30) > div > div > span > a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator').click()
        else:
            data = {'photo_link': photo_links,
                    'mobile_link': mobile_links,
                    'mobile_name': mobile_names,
                    'mobile_price': mobile_prices}

            df = pd.DataFrame(data)

            # Writing DataFrame to an Excel file
            with pd.ExcelWriter('mobiles.xlsx', engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='mobiles', index=False)
                exit()
    except Exception as e:
        data = {'photo_link': photo_links,
                'mobile_link': mobile_links,
                'mobile_name': mobile_names,
                'mobile_price': mobile_prices}

        df = pd.DataFrame(data)

        # Writing DataFrame to an Excel file
        with pd.ExcelWriter('mobiles.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='mobiles', index=False)


        driver.close()
