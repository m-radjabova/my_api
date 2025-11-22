from http import HTTPStatus
from typing import List
from typing_extensions import Annotated
from fastapi import APIRouter, Query

from schema.user import RequestTeam
from services.team_service import TeamService


router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)

team_service = TeamService()

@router.get("/",  status_code=HTTPStatus.OK)
async def get_teams():
    return team_service.get_teams()

@router.post("/", status_code=HTTPStatus.CREATED)
async def create_team(team: RequestTeam):
    return team_service.create_team(team)

@router.get("/{team_id}", status_code=HTTPStatus.OK)
async def get_team(team_id: int):
    return team_service.get_team(team_id)

@router.delete("/{team_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_team(team_id: int):
    team_service.delete_team(team_id)
    return HTTPStatus.NO_CONTENT

@router.patch("/{team_id}", status_code=HTTPStatus.OK)
async def update_team(team_id: int, new_name: Annotated[str, Query(min_length=3)]):
    return team_service.update_team_name(team_id, new_name)

@router.post("/{team_id}/members")
async def add_members_to_team(team_id: int, user_ids: List[int]):
    return team_service.add_members_to_team(team_id, user_ids)