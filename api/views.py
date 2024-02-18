from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Game, GameCharacter, InviteCode, Participant, Vote
from django.db import IntegrityError

# Create your views here.
def list_games(request):
    # full_game_list = serializers.serialize("json", Game.objects.order_by("last_update_time").all(), fields=["game_name", "last_update_time"])
    full_game_list = Game.objects.order_by("-last_update_time").values("id", "game_name", "last_update_time")
    return JsonResponse({
        "success": True,
        "games": list(full_game_list)
    })

def list_characters(request, game_id):
    try:
        target_game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Game does not exist"
        })

    character_list = target_game.gamecharacter_set.values("id", "name", "sex")
    
    return JsonResponse({
        "success": True,
        "game_name": target_game.game_name,
        "characters": list(character_list)
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
                "message": "The invite code has already been used"
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

        # try:
        #     record = Vote.objects.get(voting_user=participant, voting_character=target_character)
        # except Vote.DoesNotExist:
        #     record = Vote.objects.create(voting_user=participant, voting_character=target_character, score=vote["score"])
        # else:
        #     record.score = vote["score"]
        # finally:
        #     record.save()
        _, created = Vote.objects.update_or_create(voting_user=participant, voting_character=target_character, defaults= {"score": vote["score"]})

    return JsonResponse({
        "success": True,
        "creat_new": created
    })
    # return HttpResponse(request.POST)

def vote_results(request, game_id):
    try:
        query_game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Game does not exist"
        })
    
    vote_result_by_user = list()
    voted_participants_pk = Vote.objects.filter(voting_character__game=query_game).values_list("voting_user", flat=True).distinct()
    for participant_pk in voted_participants_pk:
        score_list = dict()
        single_participant_votes = Vote.objects.filter(voting_character__game=query_game, voting_user=participant_pk).all()
        for single_vote in single_participant_votes:
            score_list[single_vote.voting_character.name] = single_vote.score

        vote_result_by_user.append({
            "participant_name": Participant.objects.get(pk=participant_pk).name,
            "scores": score_list
        })
        print(vote_result_by_user)

    return JsonResponse({
        "success": True,
        "vote_result": vote_result_by_user
    })