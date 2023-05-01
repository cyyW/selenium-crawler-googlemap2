from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.common.action_chains import ActionChains
import logging
import numpy as np
import pandas as pd
import openpyxl
import xlsxwriter
import math

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})

driver=webdriver.Chrome(chrome_options=options)

driver.get('https://www.google.com.tw/maps/@25.0407284,121.5484174,15z?hl=zh-TW&authuser=0')
driver.maximize_window()
time.sleep(2)


#搜尋關鍵字
searchbox = driver.find_element(By.ID, 'searchboxinput')
searchbox.send_keys('新北 景點')
actions = ActionChains(driver)
actions.move_to_element(driver.find_element(By.ID, 'searchbox-searchbutton')).click().perform()
time.sleep(3)


#滾動總景點頁面，設置並確認總店家數 aq
z = 0
aq = 1000 #所需總店家數(須設定)
po_list = [7]
while True :
    pane0 = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane0)
    time.sleep(3)
    po = driver.find_elements(By.CLASS_NAME,"hfpxzc") #抓取景點用以計數，會從第一次滾動開始抓
    print(len(po)) 
    po_list.append(len(po)) #保存每輪總景點數
    if len(po)>= aq: #本輪景點數>=所需總店家數
        print("已抓到所需店家數")
        break 
    elif len(po) == po_list[-2] : #本輪店家數=上輪店家數
        aq = len(po)
        print("已拉至最底")
        break
print("總店家數為:",aq)



#取得所有景點的總留言數並存入dict_quantity及實際有效景點 u
aas = driver.find_elements(By.CLASS_NAME,"UY7F9")
bbs = driver.find_elements(By.CLASS_NAME, "qBF1Pd.fontHeadlineSmall ")
dict_quantity = [] 
dict_name_check = []
u = 0
time.sleep(3)
for i in range(min(aq, len(aas))):
    aa = aas[i]
    bb = bbs[i]
    u = u+1
    # print(aa.get_attribute('textContent').replace('(','').replace(')',''))
    dict_quantity.append(int(aa.get_attribute('textContent').replace('(','').replace(')','').replace(',', '')))
    # print(bb.get_attribute('textContent'))
    dict_name_check.append(bb.get_attribute('textContent'))  
print(dict_quantity)
print(dict_name_check)
print("需抓景點數:",aq)
print("實抓景點數:",u)

"qBF1Pd fontHeadlineSmall "

#推算達到所需資料數平均每個景點所需資料數 mu，提供給留言下拉
needquantity = 10000 #所需資料數(須設定)
mu = math.ceil(needquantity/aq)
total = 0
x = 0
while total<needquantity:
    filtered_list = list(filter(lambda x: x<mu, dict_quantity)) #小於mu的所有數
    result = sum(filtered_list) #小於mu數之和
    count = len(filtered_list) #小於mu的數量
    x = u-count #大於的數量
    total = (x)*mu+result
    mup = math.ceil((needquantity-total)/x)
    print("目前平均數",mu)
    mu = mu+mup

print("初估留言總數:", total)
print("平均每個點之留言數量:", mu)
# print("平均每個點會抓:", math.ceil(mu / 10) * 10)
# print("留言區下拉數:", math.ceil(mu / 10)-1)


alldata_dict = pd.DataFrame({'名稱':[],
                             '留言':[]})
index_list = [] #處存各點留言抓取數量，計算無空白留言數量


#因電腦無法一次抓完可採多輪抓取
#設置迴圈數及決定網頁xpth的 x 來更動
mu +=10 #因有空白留言多抓一輪
g = 0
x = 3+(60*2) #第一輪用1號for迴圈，第二輪用2號，(?*2) ?看for迴圈第一個數字
yy = 0

#點擊店家數量
#一次全抓
for y in range(aq):
#多輪抓取
# for y in range (0,60):
# for y in range(60,aq):
    dict_name = []
    dict_message = []
    try:
        #依序點擊店家、點擊更多評論、找到留言區介面
        print("第",y+1,"輪開始")
        time.sleep(3)
        actions.move_to_element(driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[' + str(x) + ']/div/a')).click().perform()
        print("點擊店家ok")
        time.sleep(7.5)
        #actions.move_to_element(driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[51]/div/button')).click().perform()
        x += 2
        try:
            actions.move_to_element(driver.find_element(By.CLASS_NAME,"HHrUdb.fontTitleSmall.rqjGif")).click().perform()
            print("點擊更多評論ok")
        except:
            try:
                time.sleep(7.5)
                actions.move_to_element(driver.find_element(By.CLASS_NAME,"HHrUdb.fontTitleSmall.rqjGif")).click().perform()
                print("二次點擊更多評論ok")    
            except:
                print("點擊更多評論出現錯誤")
                g += 1
                continue
        
        time.sleep(9)

        # scroll_div = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
        

        # 留言頁面下拉
        po1_list = [10]
        while True :
            pane1 = driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane1)
            time.sleep(3)
            po1 = driver.find_elements(By.CLASS_NAME,"rsqaWe") #抓取日期用以計數，會從第一次滾動開始抓
            print(len(po1)) 
            po1_list.append(len(po1)) #保存每輪總景點數
            if len(po1) == po1_list[-2] : #確認是拉到最底還是卡住多等兩秒
                time.sleep(3)
                po1 = driver.find_elements(By.CLASS_NAME,"rsqaWe")
                po1_list.pop()
                po1_list.append(len(po1))
                print("二次確認是否已到底")
            if len(po1)>= mu: #本輪景點數>=所需總店家數
                print("已抓到所需留言數")
                break 
            elif len(po1) == po1_list[-2] : #本輪店家數=上輪店家數
                print("已拉至最底")
                break
    

        #抓取所需 enements
        months = driver.find_elements(By.CLASS_NAME,"rsqaWe")
        messages = driver.find_elements(By.CLASS_NAME,"wiI7pd")
        fulltext= driver.find_elements(By.CLASS_NAME,"w8nwRe.kyuRq")
        
        #點開全部評論
        for ft in fulltext:
            ft.click()
            time.sleep(0.5)
        time.sleep(3)

        #抓取留言(透過時間迴圈篩出空白留言)
        s = 1
        w = 1
        for month in months:
            dict_name.append(driver.find_element(By.CLASS_NAME,'iD2gKb.W1neJ').get_attribute('textContent'))  
            print(driver.find_element(By.CLASS_NAME,'iD2gKb.W1neJ').get_attribute('textContent'))
            try:
                dict_message.append(driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[9]/div[' + str(s) + ']/div/div/div[4]/div[2]/div/span[1]').get_attribute('textContent').replace('\n', '').replace('�', '').replace('口', '').replace('👍', ''))
                print(str(w) + ' ' + '成功')
                # print(driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[9]/div[' + str(s) + ']/div/div/div[4]/div[2]/div/span[1]').get_attribute('textContent'),"\n")
                s += 3
                w += 1                                    
            except:
                # logging.exception("An exception was thrown!")
                dict_message.append("")
                print(str(w) + ' ' + '失敗')
                s += 3
                w += 1
                # break
         
                
        #這裡先將每個店家的名稱、留言先進行 dataframe 合併，
        #而後刪除空白留言資料後併入 alldata_dict，並將有問題的店家排除
        try:
            dict_name1 = pd.DataFrame({'名稱':dict_name})
            print(dict_name1)
            
            dict_message1 = pd.DataFrame({'留言':dict_message}).replace('',np.nan)
            print(dict_message1)

            print("\n", "合併 DataFrame:")
            data_dict1 = pd.concat([dict_name1, dict_message1],axis=1)
            print(data_dict1)
            
            print("\n", "去除空白留言 DataFrame:")
            data_dict2 = data_dict1.dropna(axis='index', how='any', subset=['留言']).reset_index(drop=True)
            index_list.append(len(data_dict2.index)) #取得每個點實際抓到多少留言
            print(data_dict2)


            print("\n", "總資料 DataFrame:")
            alldata_dict = pd.concat([alldata_dict,data_dict2],axis=0,ignore_index = True )
            print(alldata_dict)
            yy = yy+1
            
            
            print("目前總資料筆數:",len(alldata_dict))
            print("目前總景點數:",yy)
        except:
            print("本輪店家資料合併出現錯誤")
            # print("name:",range(len(dict_name1)))
            # print("message;",range(len(dict_message1)))  
    except:
        #如果正常跑完不會出現
        print("出包了q")
        # break



print("\n", "最終總資料 DataFrame:")
alldata_dict1 = pd.DataFrame(alldata_dict)
print(alldata_dict1)

print("相關結果如下:")
print("共",y+1,"家店")

index_count_all = len(alldata_dict1.index)
print("總留言數量:", index_count_all)

count1 = len([num for num in index_list if num >= math.ceil(mu / 10) * 10])
print("抓至所需平均留言數量:", count1)

print("無法點擊更多流言景點數:", g)

# 存檔(檔名)
alldata_dict1.to_excel('newtaipei_landmark_2.xlsx',engine='xlsxwriter',index = True, header = True)
driver.close()




#刪減多於留言數至設定留言
# total_count = 10000 # 設定總景點數
# while len(alldata_dict1) > total_count:
#     value_counts = alldata_dict1['名稱'].value_counts() # 使用 value_counts() 方法計算每個景點的數量
#     sorted_values = value_counts.sort_values(ascending=False) # 按照數量由大到小對景點進行排序
#     print(sorted_values.index[0])
#     indexes_to_remove = alldata_dict1[alldata_dict1['名稱'] == sorted_values.index[0]].tail(1).index # 使用索引留言最多的景點的最後一則留言
#     print(indexes_to_remove)
#     alldata_dict1 = alldata_dict1.drop(indexes_to_remove) #將其刪除
#     if len(alldata_dict1) == total_count: #直至達到規定總資料數
#         break
# alldata_dict1 = alldata_dict1.reset_index(drop=True) 

# print("\n", "刪減留言後的最終datafram:")
# print(alldata_dict1)



# 舊留言頁面下拉，留言數量為(i+1)*10
# for i in range (math.ceil(mu / 10)-1) :
#     pane1 = driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
#     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane1)
#     time.sleep(3)