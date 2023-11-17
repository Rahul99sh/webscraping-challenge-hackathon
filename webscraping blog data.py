from selenium import webdriver
import time
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

"""
-----STRUCTURE OF CONTENT IN WEBSITE-----

driver-> blog-items(div) -> list of (blog-item[div])
blog-item -> img(div),content(div)
img -> a(tag) -> data-bg(attribute) -----> IMG_LINK--------(1)
content -> h6(tag) -> a(tag) ------ BLOG TITLE(text)---------(2)
content -> blog-detail(div) -> bd-item[0](div) -> span(tag) -----> BLOG DATE(text)-------(3)
content -> zilla-likes(tag) -> span(tag) -----> Likes Count-------(4)

"""

def scrape_blog_data():
    driver = webdriver.Chrome()
    driver.get('https://rategain.com/blog/')#target website
    page_no = 1
    blog_no = 1
    data_list = []
    while True:
        print("At page : ",page_no)
        
        time.sleep(5)
        blog_items = driver.find_elements(By.CLASS_NAME, "blog-item")  # Locate all blog items
        
        for blog_item in blog_items:
            time.sleep(3)
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", blog_item)#scrolling to blog item
            except Exception as e:
                print("Cannot Scroll:")
                
            image_link = ""#image is considered as optional field
            try:
                image_div = blog_item.find_element(By.CLASS_NAME, "img")
                image_link = image_div.find_element(By.XPATH, './/a').get_attribute('data-bg')
            except Exception as e:
                print("Cannot find image: ", blog_no)
                
            content_div = blog_item.find_element(By.CLASS_NAME, "content")
            title_tag = content_div.find_element(By.TAG_NAME, "h6").find_element(By.TAG_NAME, "a")
            title = title_tag.get_attribute("text")
            
            date_tag = content_div.find_element(By.CLASS_NAME, "blog-detail").find_elements(By.CLASS_NAME, "bd-item")[0].find_element(By.TAG_NAME, "span")
            date = date_tag.get_attribute("innerHTML")
            
            likes_tag = content_div.find_element(By.CLASS_NAME, "zilla-likes").find_element(By.TAG_NAME, "span")
            likes = likes_tag.get_attribute("innerHTML")
            likes_count = re.search(r'\d+', likes).group()#getting only count
            #data item for excel sheet
            blog_data = {
                'S.No': len(data_list) + 1,
                'Blog Title': title,
                'Publication date': date,
                'Blog Image URL': image_link,
                'likes Count': likes_count
            }
            data_list.append(blog_data)
            blog_no+=1
        
        pagination = driver.find_element(By.CLASS_NAME, "pagination")
        time.sleep(3)
        try:
            next_button = pagination.find_element(By.CLASS_NAME, "next")#navigating to next page
            next_button.click()
            page_no+=1
        except Exception as e:
            print("---End---")
            break
    
    # Create a DataFrame and export to an Excel file
    df = pd.DataFrame(data_list)
    df.to_excel('Scraped data.xlsx', index=False)
    driver.quit()
scrape_blog_data()