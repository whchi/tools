# YouTube Channel Video Growth Analyzer

這是一個 YouTube 頻道影片成長趨勢分析工具，可以分析指定頻道的所有影片並計算其觀看量成長趨勢。

## 功能特色

1. **頻道影片導出**: 將指定頻道的所有影片數據導出為 CSV 檔案
2. **成長趨勢計算**: 計算每部影片的日、週、月觀看量成長趨勢
3. **智能過濾**: 自動跳過上線未滿 24 小時的影片，避免不準確的趨勢計算
4. **詳細統計**: 提供影片觀看數、按讚數、留言數等詳細統計信息

## 安裝與設置

### 1. 安裝依賴

```bash
uv sync --locked
```

### 2. 獲取 YouTube API 密鑰

1. 前往 [Google Cloud Console](https://console.developers.google.com/)
2. 創建新項目或選擇現有項目
3. 啟用 YouTube Data API v3
4. 創建 API 密鑰
5. 將 API 密鑰複製到 `config.py` 文件中

### 3. 配置 API 密鑰

編輯 `config.py` 文件，將 `YOUR_YOUTUBE_API_KEY_HERE` 替換為您的實際 API 密鑰：

```python
YOUTUBE_API_KEY = "您的_API_密鑰"
```

## 使用方法

### 命令行使用

```bash
uv run --env-file .env -m main
```

程式會要求您輸入頻道識別符，可以是：
- 頻道名稱（例如：PewDiePie）
- 頻道 ID（例如：UC-lHJZR3Gqxm24_Vd_AJ5Yw）
- 用戶名

### 程式化使用

```python
from main import YouTubeAnalyzer
from config import YOUTUBE_API_KEY

# 初始化分析器
analyzer = YouTubeAnalyzer(YOUTUBE_API_KEY)

# 分析頻道
success = analyzer.analyze_channel("頻道名稱")

if success:
    # 打印摘要
    analyzer.print_summary()

    # 導出到 CSV
    filename = analyzer.export_to_csv()
    print(f"數據已保存到: {filename}")
```

## 輸出說明

程式會自動生成兩種格式的報告，並保存在 `data/` 文件夾中：

### 1. CSV 檔案 (詳細數據)

### 2. Excel 檔案 (多工作表分析)

Excel 文件包含以下工作表：
- **Video Data**: 完整的影片數據
- **Summary**: 頻道統計摘要
- **Top Videos**: 觀看數最高的前20個影片

### 數據欄位說明

- `video_id`: 影片 ID
- `title`: 影片標題
- `published_at`: 發布時間
- `view_count`: 觀看次數
- `like_count`: 按讚數
- `comment_count`: 留言數
- `duration`: 影片時長
- `days_since_publish`: 發布後經過天數
- `eligible_for_analysis`: 是否適合進行成長分析
- `daily_growth`: 每日平均觀看成長
- `weekly_growth`: 每週平均觀看成長
- `monthly_growth`: 每月平均觀看成長
- `average_daily_views`: 平均每日觀看數
- `description`: 影片描述（截取前500字）
- `thumbnail_url`: 縮圖 URL
- `category_id`: 影片分類 ID

### 成長趨勢計算說明

由於 YouTube Analytics API 需要頻道擁有者授權，本工具使用簡化的成長計算方法：

- **平均每日觀看數** = 總觀看數 / 發布後天數
- **每日成長** = 平均每日觀看數
- **每週成長** = 平均每日觀看數 × 7
- **每月成長** = 平均每日觀看數 × 30

## 限制與注意事項

1. **API 配額限制**: YouTube Data API 有每日請求限制
2. **數據精確度**: 成長趨勢計算是基於當前總觀看數的平均值，非真實的增長率
3. **24小時規則**: 發布未滿24小時的影片不會進行成長分析
4. **權限限制**: 部分數據（如詳細的分析數據）需要頻道擁有者權限

## 錯誤處理

程式包含完整的錯誤處理機制：

- API 請求失敗處理
- 頻道不存在處理
- 網路連接錯誤處理
- 數據格式錯誤處理

## 範例輸出

```
YouTube 頻道影片成長趨勢分析器
========================================
請輸入頻道名稱、用戶名或頻道ID: PewDiePie

開始分析頻道: PewDiePie
頻道ID: UC-lHJZR3Gqxm24_Vd_AJ5Yw
頻道名稱: PewDiePie
正在獲取頻道所有影片...
已獲取 50 個影片...
已獲取 100 個影片...
...
總共獲取了 4500 個影片
正在獲取影片統計數據...
正在計算成長趨勢...

==================================================
分析摘要
==================================================
頻道名稱: PewDiePie
頻道訂閱數: 111000000
頻道總觀看數: 29000000000
總影片數: 4500
可分析影片數 (超過24小時): 4485
近期影片數 (少於24小時): 15
總觀看數: 29,000,000,000
總讚數: 450,000,000
平均每日觀看成長: 125000.50
==================================================

✅ 分析完成！
📁 CSV 文件已保存: PewDiePie_20250128_143052.csv
```

## 開發者信息

此工具使用 YouTube Data API v3 開發，遵循 Google API 使用條款和限制。

## 授權

本項目採用 MIT 授權協議。
