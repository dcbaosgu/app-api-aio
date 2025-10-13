from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):

    if app.openapi_schema: return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["info"]["contact"] = {
        "name": "Dev quèn",
        "url": "https://dcbao.com/",
        "email": "dcbao.dev@gmail.com",
    }
    
    openapi_schema["info"]["termsOfService"] = "https://github.com/Canon-D2/app-api-aio"

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter: **'Bearer <JWT>'**, where JWT is the access token",
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    
    return app.openapi_schema
