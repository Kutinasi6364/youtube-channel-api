from django.shortcuts import render, redirect, get_object_or_404
from youtube_api.models import YoutubeProfile
from youtube_api.views import YoutubeApiView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ChannelInfoSerializer


# DBのChannelからすべての情報を取得してchannel_list.htmlに表示する
@login_required
def channel_home_view(request):
    contents = []
    sorted_videos = []
    channels = YoutubeProfile.objects.filter(user=request.user)
    youtube_api_view = YoutubeApiView()

    # チャンネルから投稿情報を取得
    if channels.exists():
        for channel in channels:
            for video in youtube_api_view.get_channel_by_playlist(channel.playlistid):
                contents.append(video)
    
        # 投稿順に並び替え(降順)
        sorted_videos = sorted(contents, key=lambda content: content.inserted_at, reverse=True)
    else:
        messages.error(request, "You don't have any channels.")

    return render(request, "channels/channel_home.html", {"channels": channels, "videos": sorted_videos})


@login_required
def channel_list_view(request):
    channels = YoutubeProfile.objects.filter(user=request.user)
    return render(request, "channels/channel_list.html", {"channels": channels})

@login_required
def channel_search_view(request):
    channel_keyword = request.GET.get("channel_keyword")

    if channel_keyword:
        youtube_api_view = YoutubeApiView()
        channel_info = youtube_api_view.get_channel_by_keyword(channel_keyword)

        if 'error' in channel_info:
            return render(request, "channels/channel_search.html", {"error": channel_info['error']})
        
        return render(request, "channels/channel_search.html", {"channel_info": channel_info})
    else:
        return render(request, "channels/channel_search.html")



# channel_id からチャンネル情報を検索して保存
def register_channel_subscription(request):
    print(f"Channel_id: {request.POST.get('channel_id')}")
    if request.method == 'POST':
        youtube_api_view = YoutubeApiView()
        playlistid = youtube_api_view.get_channel_playlisteID(request.POST.get('channel_id'))
        channel_info = youtube_api_view.get_channel_by_id(request.POST.get('channel_id')) # チャンネル情報取得
        message = register_youtube_channel(channel_info, playlistid, request.user) # チャンネル情報保存

        messages.success(request, message['message'])
    else:
        messages.error(request, 'An error occurred while processing your request. Please try again later.')

    return redirect('channels:channel_list')  # 'channels:list'はURLパターンの名前


# Channel情報を YoutubeProfile モデルに登録
def register_youtube_channel(channel_info, playlistid, user):
    youtube_profile = YoutubeProfile(
        user=user,
        channel_id=channel_info.channel_id,
        channel_url=channel_info.channel_url[0],
        channel_name=channel_info.channel_name[0],
        description=channel_info.description[0],
        playlistid=playlistid,
        channel_icon_url=channel_info.channel_icon_url[0],
        inserted_at=channel_info.inserted_at[0]  # 登録時間
    )
    youtube_profile.save()  # データベースに保存
    return {'message': 'Channel registered successfully.'}


# Channel情報を YoutubeProfile モデルから削除
def unregister_channel_subscription(request):
    try:
        youtube_profile = get_object_or_404(YoutubeProfile, user=request.user, channel_id=request.POST.get('channel_id')) # 削除対象データ取得
        youtube_profile.delete()
        messages.success(request, 'Channel unregistered successfully.')
    
    except YoutubeProfile.DoesNotExist:
        messages.error(request, 'The channel does not exist or you don\'t have permission to unregister it.')
    except Exception as e:
        messages.error(request, f'An error occurred while processing your request. Please try again later.{e}')

    return redirect('channels:channel_list')


# Rest framework API Endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 認証されたユーザーのみ
def channel_view_set(request):
    print("request.user: ", request)  
    channel = YoutubeProfile.objects.filter(user=request.user)
    serializer = ChannelInfoSerializer(channel, many=True)
    
    if channel.exists():
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)