from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from controller import token, user, transaction, coin, coinmarketcap

app = FastAPI(debug=True)

app.include_router(token.router, tags=["Autenticação"])
app.include_router(user.router, tags=["Usuários"])
app.include_router(transaction.router, tags=["Transações"])
app.include_router(coin.router, tags=["Carteira"])
app.include_router(coinmarketcap.router, tags=["Ativos"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
