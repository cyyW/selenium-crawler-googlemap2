# selenium-crawler-googlemap2
google_crawler.py 是一個繼 selenium-crawler-googlemap 的 selenium 爬蟲工具

並新增了設定抓取店家數量及總資料筆數的功能

## 環境
* python `3.9.15`
* 虛擬環境使用 `conda`
* chrome driver:https://chromedriver.chromium.org/downloads
  - 請確認自身 google chrome 版本，並由此下載相應之版本

## 提示
* 如若電腦記憶體無法負荷一次抓取所有資料，請自行將資料抓取拆分成多輪進行
* 請自行檢查 driver.find_element By.XPATH 中的 FULL XPATH 於 google map 中是否有更動並請自行替換
* 如需將留言刪減規定數量，可啟用代碼261行之程式並將其放置在241行之下
