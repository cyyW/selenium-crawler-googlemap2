# selenium-crawler-googlemap2
selenium-crawler-googlemap2 是一個繼 selenium-crawler-googlemap 的 selenium 爬蟲工具

新增了設定抓取店家數量及總資料筆數並推算達到總資料筆數平均每個店家所需抓取的資料數

5/5:新增店家地區判別及過濾

## 環境
* python `3.9.15`
* 虛擬環境使用 `conda`
* chrome driver:https://chromedriver.chromium.org/downloads
  - 請確認自身 google chrome 版本，並由此下載相應之版本

## 提示
* 如若電腦記憶體無法負荷一次抓取所有資料，請自行將資料抓取拆分成多輪進行，但可能導致兩輪店家有重複請自行檢查
* 推算達到所需資料數平均每個景點所需資料數 mu ，由於過程中會將空白留言之資料進行刪除，因此建議將 mu 數值稍作增加
* 請自行檢查 driver.find_element By.XPATH 中的 FULL XPATH 於 google map 中是否有更動並請自行替換
* 如需刪減留言可參考319行之代碼並加以調整

