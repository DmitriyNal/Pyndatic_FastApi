from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
import uvicorn
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# users = {'1': 'Имя: Example, возраст: 18'}
users = []


class User(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=30)
    age: int = Field(ge=0, le=100)


@app.get('/users', summary='Список пользователей', tags=['Пользователи'])
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}', summary='Добавить пользователя', tags=['Пользователи'])
async def create_user(username: str, age: int):
    if users:
        new_user = users[-1].id + 1
    else:
        new_user = 1
    new_user = User(id=new_user, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', summary='Изменить пользователя', tags=['Пользователи'])
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}', summary='Удалить пользователя', tags=['Пользователи'])
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8001)
