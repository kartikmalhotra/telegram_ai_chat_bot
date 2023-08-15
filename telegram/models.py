from django.db import models
from django.db.models import JSONField
from django.core.validators import MaxValueValidator


class TelegramAvatar(models.Model):
    telegram_bot_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, default='Bot Name')
    chat_prompt = models.TextField(default='You are a helpful assistant.')
    story_prompt = models.TextField(default='You are a story teller.')
    max_input_tokens = models.IntegerField(default=250, validators=[MaxValueValidator(500)])
    max_response_tokens = models.IntegerField(default=250)
    max_conv_tokens = models.IntegerField(default=2000, validators=[MaxValueValidator(4096)])
    telegram_token = models.CharField(max_length=255, unique=True)
    welcome_message = models.CharField(max_length=1024, default='Default welcome message')
    zero_credits_message = models.CharField(max_length=1024, default='Default zero credits message')
    free_credits = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class TelegramUser(models.Model):
    telegram_user_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TelegramMembership(models.Model):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True)
    telegram_avatar = models.ForeignKey(TelegramAvatar, on_delete=models.CASCADE)
    credits_available = models.IntegerField(default=0)
    total_credits_purchased = models.IntegerField(default=0)
    total_openai_tokens_consumed = models.IntegerField(default=0)
    conv_history = JSONField(default=list)
    stories_per_day = models.IntegerField(default=3)

    def __str__(self):
        return self.telegram_user.name + ' / ' + self.telegram_avatar.name
