from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserCreationResponse, LoginResponse

router = APIRouter()

@router.post("/create_user", response_model=UserCreationResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validar si el email ya está registrado
    existing_user = db.query(User).filter(User.Email == user.Email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Crear el nuevo usuario
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserCreationResponse(UserID=new_user.UserID, message="Registro satisfactorio")

@router.post("/login", response_model=LoginResponse)
def login(email: str, password: str, db: Session = Depends(get_db)):
    # Buscar al usuario por su email
    user = db.query(User).filter(User.Email == email).first()

    # Verificar si el usuario existe y si la contraseña es correcta
    if not user or user.Password != password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Si la autenticación es exitosa, devolver la respuesta con los datos del usuario
    return {
        "Status": "Success",
        "UserID": user.UserID,
        "FirstName": user.FirstName,
        "LastName": user.LastName,
        "UserName": user.UserName,
        "UserImage": user.UserImage,
        "Bio": user.Bio,
        "PhoneNumber": user.PhoneNumber
    }