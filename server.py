import os
import json
from json import JSONDecodeError
from aiohttp import ClientSession, web

SENTRY_HOST = os.getenv('SENTRY_HOST', 'localhost')

async def main(request):
    data = await request.text()
    real_ip = request.headers.get('X-Real-IP')
    forwarded_for = request.headers.get('X-Forwarded-For')
    proxy_headers = {'Content-type': 'text/plain;charset=UTF-8'}
    if not real_ip is None:
        proxy_headers['X-Real-IP'] = real_ip
    if not forwarded_for is None:
        proxy_headers['X-Forwarded-For'] = forwarded_for

    try:
        headers, *another = data.split('\n')
        json_headers = json.loads(headers)
        dsn = json_headers['dsn']
        glitchtip_key = json_headers['trace']['public_key']
        project_id = int(dsn.split('/')[-1])
    except (ValueError, JSONDecodeError):
        return web.Response(text="Invalid request", status=400)

    async with ClientSession() as session:
        async with session.post(
                f'https://{SENTRY_HOST}/api/{project_id}/envelope/?glitchtip_key={glitchtip_key}',
                data=data,
                headers=proxy_headers
        ) as response:
            response_data = await response.text()

        return web.Response(text=response_data)


app = web.Application()
app.add_routes([web.post('/{param:.*}', main)])
web.run_app(app)
