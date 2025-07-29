#!/usr/bin/env python3
"""
YouTube Channel Video Growth Analyzer

This script analyzes YouTube channel videos and calculates their growth trends.

Features:
1. Export all videos from a specified channel to CSV
2. Calculate daily/weekly/monthly view growth trends
3. Skip videos uploaded less than 24 hours ago

Requirements:
- YouTube Data API v3 key
- Google API Python client libraries
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from dateutil import parser as date_parser

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import (
    YOUTUBE_API_KEY,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    MAX_RESULTS_PER_REQUEST,
    DEFAULT_DAYS_THRESHOLD
)

class YouTubeAnalyzer:
    """YouTube channel video analyzer for growth trends"""

    def __init__(self, api_key: str):
        """Initialize YouTube API client"""
        if api_key == "YOUR_YOUTUBE_API_KEY_HERE":
            raise ValueError("Please set your YouTube API key in config.py")

        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=api_key
        )
        self.channel_data = {}
        self.videos_data = []

    def get_channel_id_by_username(self, username: str) -> Optional[str]:
        """Get channel ID from username or handle"""
        try:
            print(f"嘗試透過用戶名查找頻道: {username}")

            # Try to get channel by username
            request = self.youtube.channels().list(
                part="id,snippet",
                forUsername=username
            )
            response = request.execute()

            print(f"用戶名查詢響應: {response}")

            # Check if response has items and is not empty
            if response.get('items') and len(response['items']) > 0:
                channel_id = response['items'][0]['id']
                self.channel_data = response['items'][0]
                print(f"透過用戶名找到頻道ID: {channel_id}")
                return channel_id

            print("用戶名查詢失敗，嘗試搜索...")

            # If username doesn't work, try searching
            search_request = self.youtube.search().list(
                part="snippet",
                q=username,
                type="channel",
                maxResults=1
            )
            search_response = search_request.execute()

            print(f"搜索響應: {search_response}")

            # Check if search response has items and is not empty
            if search_response.get('items') and len(search_response['items']) > 0:
                channel_id = search_response['items'][0]['snippet']['channelId']
                print(f"透過搜索找到頻道ID: {channel_id}")

                # Get full channel info
                channel_request = self.youtube.channels().list(
                    part="id,snippet,statistics",
                    id=channel_id
                )
                channel_response = channel_request.execute()
                if channel_response.get('items') and len(channel_response['items']) > 0:
                    self.channel_data = channel_response['items'][0]
                return channel_id

            print("搜索也未找到任何結果")
            return None
        except HttpError as e:
            print(f"HTTP錯誤獲取頻道ID: {e}")
            print(f"錯誤詳情: {e.content if hasattr(e, 'content') else 'No content'}")
            return None
        except Exception as e:
            print(f"意外錯誤獲取頻道ID: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_channel_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        """Get the uploads playlist ID for a channel"""
        try:
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()

            if response.get('items') and len(response['items']) > 0:
                uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                return uploads_playlist_id
            return None
        except HttpError as e:
            print(f"Error getting uploads playlist: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error getting uploads playlist: {e}")
            return None

    def get_all_videos_from_playlist(self, playlist_id: str) -> List[Dict]:
        """Get all videos from a playlist (uploads)"""
        videos = []
        next_page_token = None

        print("正在獲取頻道所有影片...")

        while True:
            try:
                request = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=MAX_RESULTS_PER_REQUEST,
                    pageToken=next_page_token
                )
                response = request.execute()

                # Check if response has items
                if not response.get('items'):
                    print("Warning: No items in playlist response")
                    break

                for item in response['items']:
                    video_data = {
                        'video_id': item['snippet']['resourceId']['videoId'],
                        'title': item['snippet']['title'],
                        'published_at': item['snippet']['publishedAt'],
                        'description': item['snippet']['description'][:500],  # Truncate description
                        'thumbnail_url': item['snippet']['thumbnails'].get('medium', {}).get('url', '')
                    }
                    videos.append(video_data)

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

                print(f"已獲取 {len(videos)} 個影片...")

            except HttpError as e:
                print(f"Error getting videos: {e}")
                break

        print(f"總共獲取了 {len(videos)} 個影片")
        return videos

    def get_video_statistics(self, video_ids: List[str]) -> Dict[str, Dict]:
        """Get detailed statistics for multiple videos"""
        video_stats = {}

        # YouTube API allows up to 50 video IDs per request
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            try:
                request = self.youtube.videos().list(
                    part="statistics,snippet,contentDetails",
                    id=','.join(batch_ids)
                )
                response = request.execute()

                # Check if response has items
                if not response.get('items'):
                    print(f"Warning: No items in video statistics response for batch: {batch_ids}")
                    continue

                for item in response['items']:
                    video_id = item['id']
                    stats = item.get('statistics', {})
                    snippet = item.get('snippet', {})
                    content_details = item.get('contentDetails', {})

                    video_stats[video_id] = {
                        'view_count': int(stats.get('viewCount', 0)),
                        'like_count': int(stats.get('likeCount', 0)),
                        'comment_count': int(stats.get('commentCount', 0)),
                        'duration': content_details.get('duration', ''),
                        'published_at': snippet.get('publishedAt', ''),
                        'category_id': snippet.get('categoryId', ''),
                        'tags': snippet.get('tags', [])
                    }
            except HttpError as e:
                print(f"Error getting video statistics: {e}")

        return video_stats

    def is_video_eligible_for_growth_analysis(self, published_at: str, threshold_days: int = DEFAULT_DAYS_THRESHOLD) -> bool:
        """Check if video is old enough for growth analysis"""
        try:
            publish_date = date_parser.parse(published_at)
            current_time = datetime.now(publish_date.tzinfo)
            time_diff = current_time - publish_date
            return time_diff.days >= threshold_days
        except Exception as e:
            print(f"Error parsing date {published_at}: {e}")
            return False

    def calculate_growth_trends(self, video_data: Dict, days_back: int = 30) -> Dict:
        """Calculate growth trends for a video (simplified version)"""
        # Note: This is a simplified implementation
        # In reality, you'd need historical data from YouTube Analytics API
        # which requires OAuth authentication and channel ownership

        current_views = video_data.get('view_count', 0)
        published_at = video_data.get('published_at', '')

        if not self.is_video_eligible_for_growth_analysis(published_at):
            return {
                'daily_growth': 'N/A - Too Recent',
                'weekly_growth': 'N/A - Too Recent',
                'monthly_growth': 'N/A - Too Recent',
                'eligible_for_analysis': False
            }

        try:
            publish_date = date_parser.parse(published_at)
            current_time = datetime.now(publish_date.tzinfo)
            days_since_publish = (current_time - publish_date).days

            if days_since_publish == 0:
                return {
                    'daily_growth': 'N/A - Same Day',
                    'weekly_growth': 'N/A - Same Day',
                    'monthly_growth': 'N/A - Same Day',
                    'eligible_for_analysis': False
                }

            # Simplified growth calculation (average views per day)
            avg_daily_views = current_views / days_since_publish

            growth_data = {
                'daily_growth': round(avg_daily_views, 2),
                'weekly_growth': round(avg_daily_views * 7, 2),
                'monthly_growth': round(avg_daily_views * 30, 2),
                'eligible_for_analysis': True,
                'days_since_publish': days_since_publish,
                'average_daily_views': avg_daily_views
            }

            return growth_data

        except Exception as e:
            print(f"Error calculating growth trends: {e}")
            return {
                'daily_growth': 'Error',
                'weekly_growth': 'Error',
                'monthly_growth': 'Error',
                'eligible_for_analysis': False
            }

    def analyze_channel(self, channel_identifier: str) -> bool:
        """Main method to analyze a channel"""
        print(f"開始分析頻道: {channel_identifier}")
        if channel_identifier.startswith('@'):
            channel_identifier = channel_identifier[1:]

        # Get channel ID
        if channel_identifier.startswith('UC') and len(channel_identifier) == 24:
            channel_id = channel_identifier
            # Get channel info
            try:
                request = self.youtube.channels().list(
                    part="snippet,statistics",
                    id=channel_id
                )
                response = request.execute()
                if response.get('items') and len(response['items']) > 0:
                    self.channel_data = response['items'][0]
                else:
                    print(f"Warning: No channel data found for ID: {channel_id}")
            except HttpError as e:
                print(f"Error getting channel info: {e}")
                return False
        else:
            channel_id = self.get_channel_id_by_username(channel_identifier)
            if not channel_id:
                print(f"找不到頻道: {channel_identifier}")
                return False

        print(f"頻道ID: {channel_id}")
        if self.channel_data:
            print(f"頻道名稱: {self.channel_data['snippet']['title']}")

        # Get uploads playlist ID
        uploads_playlist_id = self.get_channel_uploads_playlist_id(channel_id)
        if not uploads_playlist_id:
            print("無法獲取上傳播放列表ID")
            return False

        # Get all videos
        videos = self.get_all_videos_from_playlist(uploads_playlist_id)
        if not videos:
            print("沒有找到任何影片")
            return False

        # Get video statistics
        print("正在獲取影片統計數據...")
        video_ids = [video['video_id'] for video in videos]
        video_stats = self.get_video_statistics(video_ids)

        # Combine data and calculate growth trends
        print("正在計算成長趨勢...")
        for video in videos:
            video_id = video['video_id']
            if video_id in video_stats:
                video.update(video_stats[video_id])
                # Calculate growth trends
                growth_data = self.calculate_growth_trends(video_stats[video_id])
                video.update(growth_data)

        self.videos_data = videos
        return True

    def export_to_csv(self, filename: str = None) -> str:
        """Export video data to CSV file"""
        if not self.videos_data:
            raise ValueError("No video data to export. Run analyze_channel first.")

        # Generate filename if not provided
        if not filename:
            channel_name = self.channel_data.get('snippet', {}).get('title', 'Unknown_Channel')
            # Clean channel name for filename
            safe_channel_name = "".join(c for c in channel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/{safe_channel_name}_{timestamp}.csv"

        # Ensure data directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Define CSV columns
        columns = [
            'video_id', 'title', 'published_at', 'view_count', 'like_count',
            'comment_count', 'duration', 'days_since_publish', 'eligible_for_analysis',
            'daily_growth', 'weekly_growth', 'monthly_growth', 'average_daily_views',
            'description', 'thumbnail_url', 'category_id'
        ]

        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()

            for video in self.videos_data:
                # Prepare row data
                row = {col: video.get(col, '') for col in columns}
                # Convert lists to strings for CSV
                if isinstance(row.get('tags'), list):
                    row['tags'] = ', '.join(row['tags'])
                writer.writerow(row)

        print(f"數據已導出到: {filename}")
        return filename

    def export_to_xlsx(self, filename: str = None) -> str:
        """Export video data to Excel file"""
        if not self.videos_data:
            raise ValueError("No video data to export. Run analyze_channel first.")

        # Generate filename if not provided
        if not filename:
            channel_name = self.channel_data.get('snippet', {}).get('title', 'Unknown_Channel')
            # Clean channel name for filename
            safe_channel_name = "".join(c for c in channel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/{safe_channel_name}_{timestamp}.xlsx"

        # Ensure data directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Define columns
        columns = [
            'video_id', 'title', 'published_at', 'view_count', 'like_count',
            'comment_count', 'duration', 'days_since_publish', 'eligible_for_analysis',
            'daily_growth', 'weekly_growth', 'monthly_growth', 'average_daily_views',
            'description', 'thumbnail_url', 'category_id'
        ]

        # Prepare data for pandas DataFrame
        data_for_df = []
        for video in self.videos_data:
            row = {}
            for col in columns:
                value = video.get(col, '')
                # Convert lists to strings for Excel
                if isinstance(value, list):
                    value = ', '.join(str(item) for item in value)
                row[col] = value
            data_for_df.append(row)

        # Create DataFrame
        df = pd.DataFrame(data_for_df)

        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Video Data', index=False)

            # Summary sheet
            summary_data = self._create_summary_data()
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Top videos sheet (by views)
            eligible_videos = [v for v in self.videos_data if v.get('eligible_for_analysis', False)]
            if eligible_videos:
                top_videos = sorted(eligible_videos,
                                  key=lambda x: x.get('view_count', 0),
                                  reverse=True)[:20]

                top_videos_data = []
                for i, video in enumerate(top_videos, 1):
                    top_videos_data.append({
                        'Rank': i,
                        'Title': video.get('title', '')[:50],
                        'Views': video.get('view_count', 0),
                        'Daily Growth': video.get('average_daily_views', 0),
                        'Published': video.get('published_at', ''),
                        'Days Since Publish': video.get('days_since_publish', 0)
                    })

                top_df = pd.DataFrame(top_videos_data)
                top_df.to_excel(writer, sheet_name='Top Videos', index=False)

        print(f"Excel 數據已導出到: {filename}")
        return filename

    def _create_summary_data(self) -> List[Dict]:
        """Create summary data for Excel export"""
        if not self.videos_data:
            return []

        total_videos = len(self.videos_data)
        eligible_videos = sum(1 for video in self.videos_data if video.get('eligible_for_analysis', False))
        recent_videos = total_videos - eligible_videos
        total_views = sum(video.get('view_count', 0) for video in self.videos_data)
        total_likes = sum(video.get('like_count', 0) for video in self.videos_data)

        summary_data = [
            {'Metric': 'Channel Name', 'Value': self.channel_data.get('snippet', {}).get('title', 'N/A')},
            {'Metric': 'Total Videos', 'Value': total_videos},
            {'Metric': 'Eligible for Analysis (>24h)', 'Value': eligible_videos},
            {'Metric': 'Recent Videos (<24h)', 'Value': recent_videos},
            {'Metric': 'Total Views', 'Value': total_views},
            {'Metric': 'Total Likes', 'Value': total_likes},
        ]

        if self.channel_data and 'statistics' in self.channel_data:
            stats = self.channel_data['statistics']
            summary_data.extend([
                {'Metric': 'Channel Subscribers', 'Value': stats.get('subscriberCount', 'N/A')},
                {'Metric': 'Channel Total Views', 'Value': stats.get('viewCount', 'N/A')},
            ])

        if eligible_videos > 0:
            eligible_videos_data = [v for v in self.videos_data if v.get('eligible_for_analysis', False)]
            avg_daily_growth = sum(v.get('average_daily_views', 0) for v in eligible_videos_data) / eligible_videos
            summary_data.append({'Metric': 'Average Daily Growth', 'Value': round(avg_daily_growth, 2)})

        return summary_data

    def print_summary(self):
        """Print analysis summary"""
        if not self.videos_data:
            print("沒有可用的分析數據")
            return

        total_videos = len(self.videos_data)
        eligible_videos = sum(1 for video in self.videos_data if video.get('eligible_for_analysis', False))
        recent_videos = total_videos - eligible_videos

        total_views = sum(video.get('view_count', 0) for video in self.videos_data)
        total_likes = sum(video.get('like_count', 0) for video in self.videos_data)

        print("\n" + "="*50)
        print("分析摘要")
        print("="*50)

        if self.channel_data:
            print(f"頻道名稱: {self.channel_data['snippet']['title']}")
            if 'statistics' in self.channel_data:
                stats = self.channel_data['statistics']
                print(f"頻道訂閱數: {stats.get('subscriberCount', 'N/A')}")
                print(f"頻道總觀看數: {stats.get('viewCount', 'N/A')}")

        print(f"總影片數: {total_videos}")
        print(f"可分析影片數 (超過24小時): {eligible_videos}")
        print(f"近期影片數 (少於24小時): {recent_videos}")
        print(f"總觀看數: {total_views:,}")
        print(f"總讚數: {total_likes:,}")

        if eligible_videos > 0:
            eligible_videos_data = [v for v in self.videos_data if v.get('eligible_for_analysis', False)]
            avg_daily_growth = sum(v.get('average_daily_views', 0) for v in eligible_videos_data) / eligible_videos
            print(f"平均每日觀看成長: {avg_daily_growth:.2f}")

        print("="*50)


def main():
    """Main function"""
    print("YouTube 頻道影片成長趨勢分析器")
    print("=" * 40)

    # Check if API key is configured
    if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY_HERE":
        print("錯誤: 請在 config.py 中設置您的 YouTube API 密鑰")
        print("請前往 https://console.developers.google.com/ 獲取 API 密鑰")
        return

    # Get channel identifier from user
    channel_identifier = input("請輸入頻道名稱、用戶名或頻道ID: ").strip()
    if not channel_identifier:
        print("錯誤: 請提供有效的頻道識別符")
        return

    try:
        # Initialize analyzer
        analyzer = YouTubeAnalyzer(YOUTUBE_API_KEY)

        # Analyze channel
        success = analyzer.analyze_channel(channel_identifier)
        if not success:
            print("分析失敗")
            return

        # Print summary
        analyzer.print_summary()

        # Export to both CSV and XLSX
        csv_filename = analyzer.export_to_csv()
        xlsx_filename = analyzer.export_to_xlsx()

        print("\n✅ 分析完成！")
        print(f"📁 CSV 文件已保存: {csv_filename}")
        print(f"📊 Excel 文件已保存: {xlsx_filename}")

    except ValueError as e:
        print(f"配置錯誤: {e}")
    except Exception as e:
        print(f"分析過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
