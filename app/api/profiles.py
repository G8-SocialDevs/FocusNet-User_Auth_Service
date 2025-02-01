from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.profiles import ProfileResponse, ProfileUpdate

router = APIRouter()

@router.get("/list_profiles", response_model=list[ProfileResponse])
def list_profiles(db: Session = Depends(get_db)):
    # Obtener todos los usuarios y devolver solo los campos necesarios para los perfiles
    users = db.query(User).all()
    profiles = [
        ProfileResponse(
            UserID=user.UserID,
            FirstName=user.FirstName,
            LastName=user.LastName,
            UserName=user.UserName,
            UserImage=user.UserImage,
            Bio=user.Bio,
            PhoneNumber=user.PhoneNumber
        )
        for user in users
    ]
    return profiles

@router.get("/obtain_profile/{user_id}", response_model=ProfileResponse)
def obtain_profile(user_id: int, db: Session = Depends(get_db)):
    # Buscar al usuario por su UserID
    user = db.query(User).filter(User.UserID == user_id).first()

    # Si el usuario no existe, levantar una excepción HTTP
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no existente")

    # Devolver los datos del usuario en el formato solicitado
    return {
        "UserID": user.UserID,
        "FirstName": user.FirstName,
        "LastName": user.LastName,
        "UserName": user.UserName,
        "UserImage": user.UserImage,
        "Bio": user.Bio,
        "PhoneNumber": user.PhoneNumber
    }

@router.put("/update_profile/{user_id}", response_model=ProfileResponse)
def update_profile(user_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    # Buscar al usuario por su UserID
    user = db.query(User).filter(User.UserID == user_id).first()

    # Si el usuario no existe, levantar una excepción HTTP
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no existente")
    
    # Actualizar solo los campos que no sean None
    if profile.FirstName is not None:
        user.FirstName = profile.FirstName
    if profile.LastName is not None:
        user.LastName = profile.LastName
    if profile.UserName is not None:
        user.UserName = profile.UserName
    if profile.UserImage is not None:
        user.UserImage = profile.UserImage
    if profile.Bio is not None:
        user.Bio = profile.Bio
    if profile.PhoneNumber is not None:
        user.PhoneNumber = profile.PhoneNumber

    # Guardar los cambios en la base de datos
    db.commit()

    # Retornar los datos actualizados junto con un mensaje de éxito
    return {
        "UserID": user.UserID,
        "FirstName": user.FirstName,
        "LastName": user.LastName,
        "UserName": user.UserName,
        "UserImage": user.UserImage,
        "Bio": user.Bio,
        "PhoneNumber": user.PhoneNumber
    }