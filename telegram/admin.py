from django.contrib import admin
from telegram.models import *


class TelegramAvatarAdmin(admin.ModelAdmin):
    list_display = ('telegram_bot_id', 'name', 'chat_prompt', 'story_prompt', 'max_input_tokens',
                    'max_response_tokens', 'max_conv_tokens', 'welcome_message', 'zero_credits_message', 'free_credits')
    search_fields = ('telegram_bot_id', 'name')
    list_filter = ()


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', 'name')
    search_fields = ('telegram_user_id', 'name')
    list_filter = ()


class TelegramMembershipAdmin(admin.ModelAdmin):
    list_display = ('telegram_user', 'telegram_avatar', 'credits_available', 'total_openai_tokens_consumed',
                    'stories_per_day', 'total_credits_purchased')
    search_fields = ('telegram_user', 'telegram_avatar')
    list_filter = ('telegram_avatar', )


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramAvatar, TelegramAvatarAdmin)
admin.site.register(TelegramMembership, TelegramMembershipAdmin)
