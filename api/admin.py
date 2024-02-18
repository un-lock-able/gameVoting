from django.contrib import admin
from .models import Game, GameCharacter, Participant, InviteCode, Vote


class GameCharacterInline(admin.TabularInline):
    model = GameCharacter
    extra = 0


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["game_name"]}),
        # (
        #     "Dates",
        #     {
        #         "fields": [
        #             "create_time", "last_update_time"
        #         ]
        #     }
        # )
    ]
    inlines = [GameCharacterInline]
    readonly_fields = ["create_time", "last_update_time"]
    list_display = ["game_name", "last_update_time", "create_time"]

class InviteCodeAdmin(admin.ModelAdmin):
    readonly_fields = ["code", "used"]
    list_display = ["code", "used"]

class VoteAdmin(admin.ModelAdmin):
    list_display = ["voting_user", "voting_character", "score", "create_time", "last_update_time"]


# Register your models here.
admin.site.register(Game, GameAdmin)
# admin.site.register(GameCharacter)
admin.site.register(Participant)
admin.site.register(InviteCode, InviteCodeAdmin)
admin.site.register(Vote, VoteAdmin)
