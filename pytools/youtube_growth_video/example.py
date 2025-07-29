#!/usr/bin/env python3
"""
YouTube 頻道分析範例腳本

這個腳本展示如何使用 YouTubeAnalyzer 類來分析頻道
"""

from main import YouTubeAnalyzer
from config import YOUTUBE_API_KEY

def example_analysis():
    """範例分析函數"""
    try:
        # 初始化分析器
        analyzer = YouTubeAnalyzer(YOUTUBE_API_KEY)

        # 範例頻道 (您可以修改為任何頻道)
        channel_identifier = "Veritasium"  # 可以改為任何頻道名稱或 ID

        print(f"開始分析頻道: {channel_identifier}")

        # 執行分析
        success = analyzer.analyze_channel(channel_identifier)

        if success:
            # 打印分析摘要
            analyzer.print_summary()

            # 導出文件
            csv_filename = analyzer.export_to_csv()
            xlsx_filename = analyzer.export_to_xlsx()

            print("\n分析完成！")
            print(f"CSV 數據已保存至: {csv_filename}")
            print(f"Excel 數據已保存至: {xlsx_filename}")

            # 獲取一些統計信息
            videos_data = analyzer.videos_data

            # 找出觀看數最高的前5個影片
            top_videos = sorted(videos_data,
                              key=lambda x: x.get('view_count', 0),
                              reverse=True)[:5]

            print("\n觀看數最高的前5個影片:")
            print("-" * 50)
            for i, video in enumerate(top_videos, 1):
                title = video.get('title', 'Unknown')[:50]
                views = video.get('view_count', 0)
                print(f"{i}. {title}... - {views:,} 觀看")

            # 找出成長最快的前5個影片 (適合分析的影片)
            eligible_videos = [v for v in videos_data if v.get('eligible_for_analysis', False)]
            if eligible_videos:
                top_growth_videos = sorted(eligible_videos,
                                         key=lambda x: x.get('average_daily_views', 0),
                                         reverse=True)[:5]

                print("\n每日成長最快的前5個影片:")
                print("-" * 50)
                for i, video in enumerate(top_growth_videos, 1):
                    title = video.get('title', 'Unknown')[:50]
                    daily_growth = video.get('average_daily_views', 0)
                    print(f"{i}. {title}... - {daily_growth:.0f} 每日觀看")
        else:
            print("分析失敗，請檢查頻道名稱是否正確")

    except ValueError as e:
        print(f"配置錯誤: {e}")
        print("請確保在 config.py 中正確設置了 YouTube API 密鑰")
    except Exception as e:
        print(f"分析過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    example_analysis()
