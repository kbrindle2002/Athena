from fastapi import APIRouter

router = APIRouter(prefix="/module/fake_news_detector", tags=["modules"])

@router.get("/")
def root():
    return {"module": "fake_news_detector", "status": "ok"}
