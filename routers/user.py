from fastapi import  status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app import models,schemas,utils
from app.database import get_db


router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserRequest, db: Session = Depends(get_db)):
    """Create a new user"""
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int ,db: Session = Depends(get_db)):
    """Get a user by ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")