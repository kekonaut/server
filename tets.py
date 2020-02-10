import aiohttp
from aiohttp import web
import json
import random

chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

users = {}
counter = {}
routes = web.RouteTableDef()


def check_auth(request):
    token = request.cookies.get('Secret-token')
    try:
        user = tokens[token]
        print(user)
        return user
    except KeyError:
        raise web.HTTPUnauthorized


async def finduser(request):
    user = request.match_info['name']
    if user in users:
        return web.Response(text='Hey,{}, '.format(request.match_info['name']) + 'Lets count welsh corgi!')


tokens = {}


@routes.post('/login')
async def logged(request):
    user = request.query['name']
    password = request.query['password']
    if str(users[user]) == str(password):
        cookie = ''
        for i in range(29):
            cookie += random.choice(chars)
        tokens[cookie] = user
        response = web.json_response({'answer': 'Hey,{}, '.format(user) + 'Lets count welsh corgi!'})
        response.set_cookie('Secret-token', cookie)
        print(cookie)
        return response

        #       async with aiohttp.ClientSession() as session:
        #          my_data = {'name': user,
        #                      'password': password}
        #          data = await session.post('http://0.0.0.0:8080/count', data=my_data)
        #           print(await data.text())
   #     return web.Response(text='Hey,{}, '.format(user) + 'Lets count welsh corgi!')
    else:
        return web.Response(text='Permission denied')


@routes.post('/registration')
async def do_login(request):
    user = request.query['name']
    if user not in users:
        users[user] = request.query['password']
        counter[user] = 0
        response_obj = 'Success, you are registered'
    else:
        response_obj = 'This nickname is already in use'
    return web.Response(text=response_obj)


async def get_counter(request):
    user= check_auth(request)
    try:
        count = str(counter[user])
        return web.Response(text=count)
    except Exception as e:
        return web.Response(text=str(e))


async def post_counter(request):
    user=check_auth(request)
    try:
        counter[user] += 1
        return web.Response(text='ok')
    except Exception as e:
        return web.Response(text=str(e))


async def delete_counter(request):
    user=check_auth(request)
    try:
        counter[user] -= 1
        return web.Response(text='ok')
    except Exception as e:
        return web.Response(text=str(e))


async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj))


app = web.Application()
app.add_routes(routes)
app.router.add_get('/{name}', finduser, name='user', allow_head=False)
app.add_routes([web.post('/count/', post_counter),
                web.get('/count/', get_counter),
                web.delete('/count/', delete_counter)])
web.run_app(app)
