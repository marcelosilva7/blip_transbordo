from fastapi import FastAPI, Request, Response, status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

import os

class AuthTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Retrieve the expected token here, directly within the middleware
        expected_token = os.getenv("TOKEN_ACCESS")
        authorization: str = request.headers.get("Authorization")
        if authorization:
            scheme, _, token = authorization.partition(' ')
            if scheme.lower() == 'bearer' and token == expected_token:
                return await call_next(request)
            else:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid or missing authentication token"}
                )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization header is required"}
        )

lista = [

    {"cpf": "12345678911", "nome": "rodolfo", "nomemae": "maria", "nascimento": "10/10/2001"},
    {"cpf": "98765432199", "nome": "joao", "nomemae": "joaquina", "nascimento": "09/09/2002"}

]

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Você está no começo"}

@app.get("/cpf/{cpf}")
def listar_cpf(cpf: str):
    cpf_achado = None  # Inicializa cpf_achado antes do loop
    for item in lista:
        if item["cpf"] == cpf:
            cpf_achado = item
            break

    if cpf_achado is None:  # Verifica se cpf_achado ainda é None
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='CPF não encontrado')

    return cpf_achado