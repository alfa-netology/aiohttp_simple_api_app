from http import HTTPStatus

from pydantic import ValidationError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from werkzeug.security import generate_password_hash

from application import web
from application.models import UserModel, AdvertisingModel
from application.serializers import UserSerializer, AdvertisingSerializer


class StatusView(web.View):
    @staticmethod
    async def get():
        return web.json_response({'STATUS': 'OK'}, status=HTTPStatus.OK)


class UserListView(web.View):
    @staticmethod
    async def get():
        message = {}
        users_list = await UserModel.select('id', 'username', 'email').gino.all()
        for user in users_list:
            message[user.id] = {'username': user.username, 'email': user.email}
        return web.json_response(message, status=HTTPStatus.OK)


class UserView(web.View):
    async def post(self):
        try:
            user_data = await self.request.json()
            user_data = UserSerializer(**user_data)
            user_data.password = generate_password_hash(user_data.password)
            new_user = await UserModel.create(**user_data.dict())
            message = {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}
            return web.json_response(message, status=HTTPStatus.CREATED)
        except ValidationError as e:
            return web.json_response(e.json(), status=HTTPStatus.BAD_REQUEST)
        except UniqueViolationError as e:
            message = {'error_message': e.detail}
            return web.json_response(message, status=HTTPStatus.BAD_REQUEST)

    async def get(self):
        try:
            user_id = self.request.match_info['user_id']
            user = await UserModel.get(int(user_id))
            message = {'id': user.id, 'username': user.username, 'email': user.email}
            return web.json_response(message, status=HTTPStatus.OK)
        except AttributeError:
            message = {'error_message': 'user not found'}
            return web.json_response(message, status=HTTPStatus.NOT_FOUND)


class AdvertisingListView(web.View):
    @staticmethod
    async def get():
        message = {}
        advertising_list = await AdvertisingModel.select('id', 'title', 'text', 'created_at').gino.all()
        for advertising in advertising_list:
            message[advertising.id] = {
                'title': advertising.title,
                'text': advertising.text,
                'created_at': str(advertising.created_at)
            }
        return web.json_response(message, status=HTTPStatus.OK)

class AdvertisingView(web.View):
    async def post(self):
        try:
            advertising_data = await self.request.json()
            advertising_data = AdvertisingSerializer(**advertising_data)
            new_advertising = await AdvertisingModel.create(**advertising_data.dict())
            new_advertising.created_at = str(new_advertising.created_at)
            return web.json_response(new_advertising.to_dict(), status=HTTPStatus.CREATED)
        except ValidationError as e:
            return web.json_response(e.json(), status=HTTPStatus.BAD_REQUEST)
        except ForeignKeyViolationError as e:
            message = {'error_message': e.detail}
            return web.json_response(message, status=HTTPStatus.BAD_REQUEST)

    async def get(self):
        try:
            advertising_id = self.request.match_info['id']
            advertising = await AdvertisingModel.get(int(advertising_id))
            advertising.created_at = str(advertising.created_at)
            return web.json_response(advertising.to_dict())
        except AttributeError:
            message = {'error_message': 'advertising not found'}
            return web.json_response(message, status=HTTPStatus.NOT_FOUND)

    async def patch(self):
        try:
            data = await self.request.json()
            data = AdvertisingSerializer(**data)
        except ValidationError as e:
            return web.json_response(e.json(), status=HTTPStatus.BAD_REQUEST)

        id_ = self.request.match_info['id']
        response = await AdvertisingModel.update.values(**data.dict()).where(AdvertisingModel.id == int(id_)).gino.status()

        if response[0] == 'UPDATE 1':
            return web.json_response(data.dict(), status=HTTPStatus.OK)
        else:
            message = {'error_message': 'advertising not found'}
            return web.json_response(message, status=HTTPStatus.NOT_FOUND)

    async def delete(self):
        id_ = self.request.match_info['id']
        response = await AdvertisingModel.delete.where(AdvertisingModel.id == int(id_)).gino.status()

        if response[0] == 'DELETE 1':
            message = {'message': 'advertising successfully deleted'}
            return web.json_response(message, status=HTTPStatus.OK)
        else:
            message = {'error_message': 'advertising not found'}
            return web.json_response(message, status=HTTPStatus.NOT_FOUND)

