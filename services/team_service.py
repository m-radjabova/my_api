from typing import List
from fastapi import HTTPException
from schema.user import RequestUser, RequestTeam
from services.user_service import UserService

user_service = UserService()

class TeamService:
    def __init__(self):
        self.teams = [
            {
                "id": 1,
                "name": "Backend Team",
                "members": [{
                    "id": 3,
                    "username": "Hasan Rasulov",
                    "email": "hasan@gmail.com",
                }],
            },
            {
                "id": 2,
                "name": "Frontend Team",
                "members": [{
                    "id": 2,
                    "username": "Daler Ismatov",
                    "email": "ismatov@gmail.com",
                    },
                {   "id": 1,
                    "username": "Muslima Radjabova",
                    "email": "muslima@gmail.com",
                }],
            },
        ]

    def get_teams(self):
        return self.teams

    def create_team(self, team_data: RequestTeam):
        team_dict = team_data.model_dump()
        team_dict["id"] = len(self.teams) + 1
        team_dict["members"] = []
        
        self.teams.append(team_dict)
        return team_dict

    def get_team(self, team_id: int):
        for team in self.teams:
            if team["id"] == team_id:
                return team
        raise HTTPException(status_code=404, detail="Team not found")

    def delete_team(self, team_id: int):
        for i, team in enumerate(self.teams):
            if team["id"] == team_id:
                del self.teams[i]
                return {"message": "Team deleted successfully"}
        raise HTTPException(status_code=404, detail="Team not found")
    
    def update_team_name(self, team_id: int, new_name: str):
        for i, team in enumerate(self.teams):
            if team["id"] == team_id:
                self.teams[i]["name"] = new_name
                return self.teams[i]
        raise HTTPException(status_code=404, detail="Team not found")


    def add_member_to_team(self, team_id: int, user_id: int):
        team = self.get_team(team_id)
        user = user_service.get_user(user_id)

        if any(member["id"] == user_id for member in team["members"]):
            raise HTTPException(status_code=400, detail="User already in this team")

        team["members"].append(user)
        return team

    def add_members_to_team(self, team_id: int, user_ids: List[int]):
        team = self.get_team(team_id)
        for user_id in user_ids:
            user = user_service.get_user(user_id)
            if not any(member["id"] == user_id for member in team["members"]):
                team["members"].append(user)
        return team

    def get_user(self, user_id: int):
        return user_service.get_user(user_id)
