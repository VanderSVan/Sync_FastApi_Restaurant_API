from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, ProgrammingError

from .routers import client, order, schedule, table
from .utils.exceptions import JSONException


def create_app():
    application = FastAPI()

    # Routers
    application.include_router(client.router)
    application.include_router(order.router)
    application.include_router(schedule.router)
    application.include_router(table.router)

    # Exception handlers
    @application.exception_handler(JSONException)
    async def error_handler_400(request: Request, exception: JSONException):
        return JSONResponse(status_code=exception.status_code,
                            content={"message": exception.message})

    @application.exception_handler(IntegrityError)
    async def handler_alchemy_integrity_error(request: Request, integrity_err):
        err_name = "sqlalchemy.exc.IntegrityError"
        traceback = integrity_err.args[0] or str(integrity_err)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": {'err_name': err_name,
                                                 'traceback': traceback}})

    @application.exception_handler(ProgrammingError)
    async def handler_alchemy_integrity_error(request: Request, programming_err):
        err_name = "sqlalchemy.exc.ProgrammingError"
        traceback = programming_err.args[0] or str(programming_err)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": {'err_name': err_name,
                                                 'traceback': traceback}})

    @application.exception_handler(AttributeError)
    async def handler_alchemy_integrity_error(request: Request, attribute_err):
        err_name = "AttributeError"
        traceback = attribute_err.args or str(attribute_err)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": {'err_name': err_name,
                                                 'traceback': traceback}})

    return application


app = create_app()