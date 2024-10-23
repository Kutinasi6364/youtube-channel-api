## 5. API仕様書

### APIエンドポイント一覧
- **POST /api/channels/**: チャンネル登録
  - **リクエスト**: `{ "channel_url": "YouTubeチャンネルのURL" }`
  - **レスポンス**: `{ "id": 1, "channel_name": "Channel Name", "channel_id": "UCXXXX" }`
- **DELETE /api/channels/{id}/**: チャンネル削除
  - **リクエスト**: チャンネルID
  - **レスポンス**: `{ "message": "Deleted" }`
- **GET /api/channels/**: チャンネル一覧取得
  - **レスポンス**: チャンネル情報の配列

---