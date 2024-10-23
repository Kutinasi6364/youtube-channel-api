from rest_framework import serializers
from youtube_api.models import YoutubeProfile

class ChannelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeProfile
        fields = '__all__'
