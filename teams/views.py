from rest_framework.views import APIView, Request, Response, status
from .models import Team
from django.forms.models import model_to_dict
from utils import data_processing
from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        try:
            team_data = data_processing(request.data)
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as err:
            return Response({"error": str(err)}, status.HTTP_400_BAD_REQUEST) 
        
        team = Team.objects.create(**team_data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)
    
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        team_list = []
        for team in teams:
            team_dict = model_to_dict(team)
            team_list.append(team_dict)

            return Response(team_list, status.HTTP_200_OK)
        

class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )
        converted_team = model_to_dict(team)
        return Response(converted_team)    

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            found_team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )

        for key, value in request.data.items():
            setattr(found_team, key, value)
        found_team.save()

        converted_team = model_to_dict(found_team)
        return Response(converted_team)    

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            found_team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"},
                status.HTTP_404_NOT_FOUND,
            )
        found_team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

