from googleapiclient.discovery import build
from datetime import datetime, timedelta
from django.conf import settings

# チャンネル情報用クラス作成
class ChannelInfo:
    def __init__(self, channel_id, channel):
        self.channel_id = channel_id
        self.channel_url = channel['snippet']['customUrl'],
        self.channel_name = channel['snippet']['title'],
        self.description = channel['snippet']['description'],
        self.channel_icon_url = channel['snippet']['thumbnails']['medium']['url'],
        self.inserted_at = datetime.now().isoformat()  # 登録時間をISOフォーマットで返す

# 動画情報用クラス作成
class VideoInfo:
    def __init__(self, video):
        self.video_id = video['id'],
        self.video_name = video['snippet']['title'],
        self.description = video['snippet']['description'],
        date_time = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S%z')
        self.inserted_at = date_time + timedelta(hours=9) # UTC時間から日本時間に変換

class YoutubeApiView:
    """
        A class to represent information about a YouTube channel.
        This class holds detailed information for a specific YouTube channel, 
        including the channel ID, URL, name, description, channel icon URL, 
        and the timestamp of when the information was retrieved.

        Attributes:
            channel_id (str): The unique identifier for the YouTube channel.
            channel_url (str): The custom URL of the YouTube channel.
            channel_name (str): The title of the YouTube channel.
            description (str): The description of the YouTube channel.
            channel_icon_url (str): The URL of the channel's icon.
            inserted_at (str): The timestamp of when the channel information was retrieved in ISO format.
    """
    def __init__(self):
        # YouTube APIの初期化
        api_key = settings.YOUTUBE_API_KEY  # 環境変数からAPIキーを取得
        self.youtube_service = build('youtube', 'v3', developerKey=api_key)


    # 指定したChannelIDで情報を検索(キーワードではなくID固定)
    def get_channel_by_id(self, channel_id):
        # # チャンネル情報を取得
        return ChannelInfo(channel_id, self._get_channels_list(channel_id, "snippet"))


    # チャンネルのアップロード済み動画プレイリストID取得
    def get_channel_playlisteID(self, channel_id):
        # チャンネル情報を取得
        channel_info = self._get_channels_list(channel_id, "contentDetails")
        return channel_info['contentDetails']['relatedPlaylists']['uploads']
    

    # チャンネル情報取得共通部分
    def _get_channels_list(self, channel_id, part):
        """
            Retrieve detailed information about a specific YouTube channel.
            This function fetches channel data from the YouTube API using the provided channel ID and specified parts of the channel resource.

            Args:
                channel_id (str): The ID of the YouTube channel to retrieve.
                part (str): A comma-separated list of channel resource parts to include 
                            in the API response (e.g., 'snippet,contentDetails').
            Returns:
                dict or None: A dictionary containing channel details if the channel exists; otherwise, returns None.

        """
        request = self.youtube_service.channels().list(
            part=part,
            id=channel_id
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]
        
        return None

    
    # Channelキーワード検索
    def get_channel_by_keyword(self, channel_keyword):
        """
            Retrieve channel information based on a specified keyword.
            This function searches for YouTube channels that match the given keyword and returns a list of channel details. 
            It retrieves the first five channels found.

            Args:
                channel_keyword (str): The keyword to search for in channel names or descriptions.
            Returns:
                list: A list of channel details, each represented as a dictionary returned by the `get_channel_by_id` method.
        """
        response_data = []

        # チャンネル情報を取得
        request = self.youtube_service.search().list(
            part="snippet",
            q=channel_keyword,
            type="channel",
            maxResults="5"
        )
        response = request.execute()

        # チャンネル詳細を取得する為に、チャンネルIDを個別検索に飛ばして取得したクラス配列を作成
        if 'items' in response and len(response['items']) > 0:
            for channel in response['items']:
                response_data.append(self.get_channel_by_id(channel['snippet'].get('channelId')))
                    
            return response_data
    

    # チャンネルのプレイリストから動画情報取得
    def get_channel_by_playlist(self, playlist_id):
        video_list = []
        request = self.youtube_service.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=5
        )
        response = request.execute()
        if 'items' in response and len(response['items']) > 0:
            for video in response['items']:
                request = self.youtube_service.videos().list(
                    part="snippet,contentDetails",
                    id=video['snippet']['resourceId']['videoId']
                )
                response = request.execute()
                if 'items' in response and len(response['items']) > 0:
                    video_list.append(VideoInfo(response['items'][0]))
                
            return video_list
        return None

    
