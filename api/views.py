from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Game, GameCharacter, InviteCode, Participant, Vote
from django.core import serializers
from django.db import IntegrityError

# Create your views here.
def list_games(request):
    full_game_list = serializers.serialize("json", Game.objects.order_by("last_update_time").all(), fields=["game_name", "last_update_time"])
    return JsonResponse({
        "success": True,
        "games": full_game_list
    })

def list_characters(request, game_id):
    try:
        target_game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Game does not exist"
        })
    
    return JsonResponse({
        "success": True,
        "game_name": target_game.game_name,
        "characters": serializers.serialize("json", target_game.gamecharacter_set.all(), fields=["name", "sex"])
    })


@csrf_exempt
def record_votes(request, game_id):
    # Check whether the http method is POST
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Incorrect http method"
        }) 
    # Now it must be a POST message

    # Check whether the game id exists
    try:
        target_game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Game does not exist"
        })
    # Now the game must exist

    # Try to decode the json
    try:
        post_data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Corrupted json content"
        })
    # Decode success
    # post_data = {
    #     "invite_code": "XXXXXX",
    #     "nickname": "Some Name",
    #     "votes": [
    #         {
    #             "character_id": 2,
    #             "score": 9
    #         },
    #         {
    #             "character_id": 3,
    #             "score": 10
    #         }    
    #     ]
    # }

    # Validate the invite code
    try:
        invite_code_object = InviteCode.objects.get(code=post_data["invite_code"])
    except InviteCode.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Invalid invite code"
        })
    # The code exists
    
    # If the code is used, then we see if it is the voter trying to change the record;
    # if it is not used, we assume it is a new user trying to register
    if invite_code_object.used:
        try:
            participant = Participant.objects.get(name=post_data["nickname"])
        except Participant.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "The nickname does not match"
            })
    else:
        try:
            participant = Participant.objects.create(name=post_data["nickname"], register_code=invite_code_object)
        except IntegrityError:
            return JsonResponse({
                "success": False,
                "message": "The nickname has already been taken!"
            })
        invite_code_object.used = True
        invite_code_object.save()
    
    for vote in post_data["votes"]:
        try:
            target_character = GameCharacter.objects.get(pk=vote["character_id"])
        except GameCharacter.DoesNotExist:
            continue

        try:
            record = Vote.objects.get(voting_user=participant, voting_character=target_character)
        except Vote.DoesNotExist:
            record = Vote.objects.create(voting_user=participant, voting_character=target_character, score=vote["score"])
        else:
            record.score = vote["score"]
        finally:
            record.save()

    return JsonResponse({
        "success": True
    })
    # return HttpResponse(request.POST)

def vote_results(request, game_id):
    return JsonResponse({"success": True})