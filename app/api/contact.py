from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.contact import Contact
from app.models.user import User
from app.schemas.contact import ContactResponse, ContactListResponse

router = APIRouter()

@router.post("/add_contact_request/{useridprop}", response_model=ContactResponse)
async def add_contact_request(useridprop: int, useridrec: int, db: Session = Depends(get_db)):

    if useridprop == useridrec:
        raise HTTPException(status_code=400, detail="No puedes enviarte una solicitud de contacto a ti mismo")

    # Verificar si los dos usuarios existen
    user_prop = db.query(User).filter(User.UserID == useridprop).first()
    user_rec = db.query(User).filter(User.UserID == useridrec).first()

    if not user_prop or not user_rec:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si ya existe la solicitud de contacto entre los dos usuarios
    existing_contact = db.query(Contact).filter(
        or_(
            and_(Contact.UserIDProp == useridprop, Contact.UserIDRec == useridrec),
            and_(Contact.UserIDProp == useridrec, Contact.UserIDRec == useridprop)
        )
    ).first()


    if existing_contact:
        raise HTTPException(status_code=400, detail="Solicitud de contacto ya existente")

    # Crear una nueva solicitud de contacto
    new_contact = Contact(UserIDProp=useridprop, UserIDRec=useridrec, Status=1)  # Status 1 = Pendiente
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {
        "contactid": new_contact.ContactID,
        "useridprop": new_contact.UserIDProp,
        "useridrec": new_contact.UserIDRec,
        "status": new_contact.Status
    }

@router.get("/list_contact_requests/{useridrec}", response_model=list[ContactResponse])
def list_contact_requests(useridrec: int, db: Session = Depends(get_db)):
    contacts  = db.query(Contact).filter(
        Contact.UserIDRec == useridrec,
        Contact.Status == 1
    ).all()

    contactsresponse = [
        ContactResponse(
            contactid=c.ContactID,
            useridprop=c.UserIDProp,
            useridrec=c.UserIDRec,
            status=c.Status
        )
        for c in contacts
    ]
    
    return contactsresponse

@router.put("/response_contact_requests/{contactid}", response_model=ContactResponse)
def response_contact_requests(contactid: int, status: int, db: Session = Depends(get_db)):
    if status not in [2, 3]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    contact = db.query(Contact).filter(Contact.ContactID == contactid, Contact.Status == 1).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Solicitud de contacto no encontrada")

    contact.Status = status
    db.commit()
    db.refresh(contact)

    return ContactResponse(
        contactid=contact.ContactID,
        useridprop=contact.UserIDProp,
        useridrec=contact.UserIDRec,
        status=contact.Status
    )

@router.get("/list_contacts/{user_id}", response_model=list[ContactListResponse])
def list_contacts(user_id: int, db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(
        or_(
            Contact.UserIDProp == user_id,
            Contact.UserIDRec == user_id
        ),
        Contact.Status == 2  # Solo contactos aceptados
    ).all()

    contact_list = [
        ContactListResponse(
            contactid=contact.ContactID,
            contact_user_id=contact.UserIDRec if contact.UserIDProp == user_id else contact.UserIDProp
        )
        for contact in contacts
    ]

    return contact_list
