from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Database import models
from Database.database import engine
from Router import user_routes, job_routes, map_routes, auth_routes

app = FastAPI()

models.Base.metadata.create_all(engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(job_routes.router)
app.include_router(map_routes.router)



