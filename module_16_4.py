from typing import Annotated, List
from fastapi import FastAPI, Path, HTTPException, Body
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get('/users')
async def get_user() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def userName(user: User, username: str, age: int) -> str:
    num_user = len(users)
    if num_user == 0:
        user.id = 1
    else:
        user.id = users[num_user - 1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    return f'User {username} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def updateUser(user_id: int, username: str, age: int, user: str = Body()) -> str:
    try:
        change_user = users[user_id - 1]
        change_user.username = username
        change_user.age = age
        return f'The user with ID = {user_id} is changed. Username: {username}, age: {age}'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
async def deleteUser(user_id: int) -> str:
    try:
        users.pop(user_id - 1)
        return f'User with ID = {user_id} was deleted.'
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')