# from django.db import models


# class Channel(models.Model):
#     channel_id = models.CharField(max_length=100, unique=True)
#     channel_name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         "users.User", on_delete=models.CASCADE, related_name="channels"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
