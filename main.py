from uvicorn import run

from tasks import *
from web import tech, api
from root import app

if __name__ == '__main__':
    app.include_router(tech)
    app.include_router(api)
    run(app, host="0.0.0.0", port=8000)
