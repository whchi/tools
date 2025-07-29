#!/usr/bin/env python3
"""
CSV to XLSX Converter

將現有的 CSV 文件轉換為 XLSX 格式並移動到 data 文件夾
"""

import os
import pandas as pd

def convert_csv_to_xlsx():
    """轉換當前目錄下的 CSV 文件為 XLSX"""

    # 確保 data 目錄存在
    os.makedirs('data', exist_ok=True)

    # 查找所有 CSV 文件
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

    if not csv_files:
        print("沒有找到 CSV 文件")
        return

    for csv_file in csv_files:
        try:
            print(f"正在轉換: {csv_file}")

            # 讀取 CSV
            df = pd.read_csv(csv_file, encoding='utf-8')

            # 生成 XLSX 文件名
            base_name = os.path.splitext(csv_file)[0]
            xlsx_file = f"data/{base_name}.xlsx"

            # 轉換為 XLSX
            with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
                # 主數據表
                df.to_excel(writer, sheet_name='Video Data', index=False)

                # 創建摘要表
                if not df.empty:
                    summary_data = []

                    # 基本統計
                    total_videos = len(df)
                    eligible_videos = len(df[df.get('eligible_for_analysis', pd.Series([False] * len(df)))])
                    total_views = df['view_count'].sum() if 'view_count' in df.columns else 0
                    total_likes = df['like_count'].sum() if 'like_count' in df.columns else 0

                    summary_data = [
                        {'Metric': 'Total Videos', 'Value': total_videos},
                        {'Metric': 'Eligible for Analysis', 'Value': eligible_videos},
                        {'Metric': 'Total Views', 'Value': total_views},
                        {'Metric': 'Total Likes', 'Value': total_likes},
                    ]

                    # 平均成長率
                    if 'average_daily_views' in df.columns:
                        eligible_df = df[df.get('eligible_for_analysis', pd.Series([False] * len(df)))]
                        if not eligible_df.empty:
                            avg_growth = eligible_df['average_daily_views'].mean()
                            summary_data.append({'Metric': 'Average Daily Growth', 'Value': round(avg_growth, 2)})

                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)

                    # 前20名影片（按觀看數）
                    if 'view_count' in df.columns and 'title' in df.columns:
                        top_videos = df.nlargest(20, 'view_count')[['title', 'view_count', 'published_at']]
                        top_videos['rank'] = range(1, len(top_videos) + 1)
                        top_videos = top_videos[['rank', 'title', 'view_count', 'published_at']]
                        top_videos.columns = ['Rank', 'Title', 'Views', 'Published']
                        top_videos.to_excel(writer, sheet_name='Top Videos', index=False)

            print(f"✅ 轉換完成: {xlsx_file}")

            # 移動 CSV 到 data 文件夾
            new_csv_path = f"data/{csv_file}"
            os.rename(csv_file, new_csv_path)
            print(f"📁 CSV 已移動到: {new_csv_path}")

        except Exception as e:
            print(f"❌ 轉換 {csv_file} 時發生錯誤: {e}")

if __name__ == "__main__":
    convert_csv_to_xlsx()
