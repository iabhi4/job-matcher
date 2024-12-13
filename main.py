from fastapi import FastAPI
from routes.user import userRouter
from routes.rules import rulesRouter
from routes.dashboard import dashboardRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(userRouter)
app.include_router(rulesRouter)
app.include_router(dashboardRouter)

@app.get("/")
async def root():
    return {"message": "Job Matcher Backend is running!"}