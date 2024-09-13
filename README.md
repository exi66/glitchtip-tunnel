# Glitchtip tunnel

This is an aiohttp-based application for tunnelling Glitchtip traffic like in [Sentry](https://docs.sentry.io/platforms/javascript/troubleshooting/#using-the-tunnel-option) to avoid blocking by adblockers

## Installation

### 1. Setup your webserver

#### Nginx example

```
...
	location /tunnel {
		add_header 'Access-Control-Allow-Origin' '*';
		proxy_pass http://127.0.0.1:8080;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
	}
...
```

### 2. Run docker

```
docker build -t tunnel .
docker run -p 8080:8080 -e SENTRY_HOST='your.host.glitchtip.com' tunnel
```
