from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

import models, schemas, crud
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CREATE
@app.post("/contacts", response_model=schemas.ContactResponse)
def create(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


# READ ALL
@app.get("/contacts")
def read_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)


# READ ONE
@app.get("/contacts/{contact_id}")
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    return crud.get_contact(db, contact_id)


# UPDATE
@app.put("/contacts/{contact_id}")
def update(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    return crud.update_contact(db, contact_id, contact)


# DELETE
@app.delete("/contacts/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db)):
    return crud.delete_contact(db, contact_id)


# SEARCH
@app.get("/search")
def search(query: str, db: Session = Depends(get_db)):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.contains(query)) |
        (models.Contact.last_name.contains(query)) |
        (models.Contact.email.contains(query))
    ).all()


# BIRTHDAYS (7 days)
@app.get("/birthdays")
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)

    contacts = db.query(models.Contact).all()

    result = []
    for c in contacts:
        if today.month == c.birthday.month and today.day <= c.birthday.day <= end_date.day:
            result.append(c)

    return result
