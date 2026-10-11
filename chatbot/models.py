from django.db import models
from django.conf import settings

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='chat_logs')
    session_id = models.CharField(max_length=100, db_index=True)
    user_query = models.TextField()
    bot_response = models.TextField()
    model_used = models.CharField(max_length=50, default='qwen3:4b')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CHAT_HISTORY'
        verbose_name = 'Chat History'
        verbose_name_plural = 'Chat Histories'
        ordering = ['created_at']

    def __str__(self):
        user_name = self.user.username if self.user else f"Guest ({self.session_id[:8]})"
        return f"Chat by {user_name} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
