from os import name
from typing import ItemsView
import requests
from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def click():
    font_list_Name=[]
    font_list_Text=[]
    
    options = Options()
    options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=options)
    browser.implicitly_wait(20)
    browser.get("https://www.rakuten-sec.co.jp/web/fund/find/search/result.html")
    
    for pageIndex in range(1,10):
        item_select = browser.find_element_by_xpath("//a[@id='pcm-fsearch-tab-operation-policy']")
        browser.execute_script("arguments[0].click();", item_select)    
        soup = BeautifulSoup(browser.page_source,"html.parser")
        
        htmlItemTableTr=soup.find("table",{"class":"pcm-fsearch-table pcm-fsearch-result-table pcm-fsearch-result-table--operation-policy"}).tbody.find_all('tr')    
        # htmlItemContents=soup.find_all("td",{"data-field":"operatingpolicy"})
        
        # print(f"==========第{str(pageIndex)}頁==========")
        
        # for name in htmlItemContents:
            # if '\n' in name.string:
            #     name=name.string.strip()
            # else:
            #     name=name.string
            # if ":"+name not in font_list_Text :
            #     font_list_Text.append(":"+name)
            
        for row in htmlItemTableTr:
            htmlItemNameID=row.find("a")["href"]
            htmlItemNameTd=row.find("a",{"href":htmlItemNameID})
            htmlItemContents=row.find("td",{"data-field":"operatingpolicy"})
            if '\n' in htmlItemContents.string:
                htmlItemContents=htmlItemContents.string.strip()
            else:
                htmlItemContents=htmlItemContents.string
            if htmlItemContents not in font_list_Text :
                font_list_Text.append(":"+htmlItemContents)
            htmlItemName=htmlItemNameTd.string
            if htmlItemName not in   font_list_Name :
                font_list_Name.append(htmlItemName)
        # print(font_list_Text)    
            
        # for item in htmlItemName:
        #     if item.string not in font_list_Name    :
        #         font_list_Name.append(item.string)
        # print(font_list_Name)

        # for i in range(len(font_list_Name)):
        #     if font_list_Name[i]+font_list_Text[i] not in font_list_New:
        #         font_list_New.append(font_list_Name[i]+font_list_Text[i])
                
        # for i in range(len(font_list_Name)):
        #     d=dict([(font_list_Name[i],font_list_Text[i])])
        # print(d)   
        # print(font_list_New)  
        page_next = browser.find_element_by_xpath("//a[@class='pcm-fsearch-result-pagination__link pcm-fsearch-page-link pcm-fsearch-page-link--next']")
        page_next.click()
        browser.implicitly_wait(10)
    
    return font_list_Name,font_list_Text
        

    


