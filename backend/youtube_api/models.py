from django.db import models

class YoutubeProfile(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)  # ユーザーとの関連
    channel_id = models.CharField(max_length=255, unique=True)  # YouTubeのチャンネルID
    channel_url = models.URLField()  # YouTubeチャンネルのURL
    channel_name = models.CharField(max_length=255)  # チャンネル名
    description = models.TextField()  # チャンネルの説明
    playlistid = models.CharField(null=True) # チャンネルのアップロード済み動画リストID
    channel_icon_url = models.URLField()  # チャンネルアイコンのURL
    inserted_at = models.DateTimeField(auto_now_add=True)  # 登録日時

    def __str__(self):
        return self.channel_name
