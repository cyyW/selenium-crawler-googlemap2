# selenium-crawler-googlemap2
selenium-crawler-googlemap2 是一個繼 [selenium-crawler-googlemap](https://github.com/cyyW/selenium-crawler-googlemap) 的 google map selenium 爬蟲工具；我們用其抓取了六都(台北、新北、新竹、台中、台南、高雄)的景點留言，每都10000筆以上總計六萬筆以上並將其存入 [地標評論.xlsx](https://github.com/cyyW/selenium-crawler-googlemap2/blob/main/%E5%9C%B0%E6%A8%99%E8%A9%95%E8%AB%96.xlsx)之中。

* 新增 : 可設定抓取店家數量及總資料筆數，推算達到總資料筆數平均每個店家所需抓取的資料數。
* 5/5 : 新增店家地區判別及過濾，因為之後發現 google map 搜尋特定地區時常出錯。

## 環境
* python `3.9.15`
* 虛擬環境使用 `conda`
* chrome driver : https://chromedriver.chromium.org/downloads
  - 請確認自身 google chrome 版本，並由此下載相應之版本

## 提示
* 如若電腦記憶體無法負荷一次抓取所有資料，請自行將資料抓取拆分成多輪進行，但可能導致兩輪店家有重複請自行檢查
* 推算達到所需資料數平均每個景點所需資料數 mu ，由於過程中會將空白留言之資料進行刪除，因此建議將 mu 數值稍作增加
* 請自行檢查 driver.find_element By.XPATH 中的 FULL XPATH 於 google map 中是否有更動並請自行替換
* 如需刪減留言可參考319行之代碼並加以調整

