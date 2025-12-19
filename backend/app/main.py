from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from .models import Base, Title, Chapter
from .schemas import TitleCreate, TitleResponse, ChapterCreate, ChapterResponse
from .database import engine, get_db

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Novel Reader API",
    description="API for reading novels and managing chapters",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Expanded for dev/prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/titles/", response_model=TitleResponse, status_code=status.HTTP_201_CREATED)
def create_novel(title: TitleCreate, db: Session = Depends(get_db)):
    """Create a new novel."""
    new_title = Title(**title.model_dump())
    db.add(new_title)
    db.commit()
    db.refresh(new_title)
    return new_title

# 1. Убери слэш после titles
@app.get("/titles", response_model=List[TitleResponse])
def get_all_novels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Title).options(joinedload(Title.chapters)).offset(skip).limit(limit).all()

# 2. Здесь тоже проверь, чтобы не было лишних знаков
@app.get("/titles/{title_id}", response_model=TitleResponse)
def get_novel_by_id(title_id: int, db: Session = Depends(get_db)):
    # Добавь этот принт, чтобы увидеть в консоли, доходит ли запрос
    print(f"--- ЗАПРОС НА ID: {title_id} ---")
    
    novel = db.query(Title).options(joinedload(Title.chapters)).filter(Title.id == title_id).first()
    if not novel:
        raise HTTPException(status_code=404, detail="Not Found")
    return novel

@app.post("/titles/{title_id}/chapters/", response_model=ChapterResponse)
def create_chapter_for_novel(title_id: int, chapter: ChapterCreate, db: Session = Depends(get_db)):
    """Add a chapter to a novel."""
    novel = db.query(Title).filter(Title.id == title_id).first()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    
    new_chapter = Chapter(**chapter.model_dump(), title_id=title_id)
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter

@app.get("/chapters/{chapter_id}", response_model=ChapterResponse)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    """Get a specific chapter."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.get("/")
def root():
    return {"status": "online", "message": "API is running"}