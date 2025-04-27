#!/usr/bin/env python3
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from requests import Session
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, SessionLocal, get_db
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from portfolio.model import portfolio
from user import UserDB, UserCreate, User, Token
from security import *
from portfolio.route import portfolio_router
from fastapi.staticfiles import StaticFiles
from portfolio.model import portfolio_create

app = FastAPI(title='PortfolioAPI', description='This is an API that can be used to manage a portfolio.', version='1.0.0') 
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
Base.metadata.create_all(bind=engine)


@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user_db(db, user)

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = await get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.last_name = user.last_name
    db_user.first_name = user.first_name
    db_user.adress = user.adress
    db_user.phone = user.phone
    db_user.age = user.age
    db_user.role = user.role
    db_user.facebook = user.facebook
    db_user.linkedin = user.linkedin
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):
    db_user = await get_user(db, user_id=user_id)
    if not db_user: 
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: SessionLocal = Depends(get_db)):
    db_user = await get_user(db, user_id=user_id)   
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
@app.get("/users/", response_model=list[User])
async def read_users(skip: int = 0, limit: int = 10, db: SessionLocal = Depends(get_db)):
    db_users = db.query(UserDB).offset(skip).limit(limit).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="No users found")
    return db_users

@app.get("/users/me/admin/", response_model=User)
async def read_users_me_admin(current_user: UserDB = Depends(get_current_active_admin)):
    return current_user
@app.get("/users/me/user/", response_model=User)
async def read_users_me_user(current_user: UserDB = Depends(get_current_active_user_or_admin)):
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = await get_user_by_username(db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_active_user)):
    return current_user

@app.get("/protected/", dependencies=[Depends(get_current_active_user)])
async def protected_route():
    return {"message": "This route is protected!"}

@app.get("/public/")
async def public_route():
    return {"message": "This route is public."}

template_list = [
	"template1.html",
	"template2.html",
]
templates = Jinja2Templates(directory="template")
app.mount('/static', StaticFiles(directory='static'), name='static')
@app.get("/port/{lien_portfolio}")
async def get_portfolio_by_lien_portfolio(lien_portfolio: str, request: Request,db: Session = Depends(get_db) ):
	db_portfolio = db.query(portfolio).join(UserDB).filter(portfolio.lien_portfolio == lien_portfolio).first()
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
    
    
    
	return templates.TemplateResponse(template_list[db_portfolio.template], {"request": request, "portfolio": db_portfolio})

@app.get("/{lien_portfolio}")
async def get_portfolio_by_lien_portfolio(lien_portfolio: str, request: Request,db: Session = Depends(get_db) ):
	db_portfolio = db.query(portfolio).join(UserDB).filter(portfolio.lien_portfolio == lien_portfolio).first()
    
    
    
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return {
        "username": db_portfolio.user.username,
        "firstname": db_portfolio.user.first_name,
        "lastname": db_portfolio.user.last_name,
        "email": db_portfolio.user.email,
        "phone": db_portfolio.user.phone,
        "adress": db_portfolio.user.adress,
        "age": db_portfolio.user.age,
        "facebook": db_portfolio.user.facebook,
        "linkedin": db_portfolio.user.linkedin,
        "template": db_portfolio.template,
        "titre": db_portfolio.titre,
        "loisir": db_portfolio.loisir,
        "parcours": db_portfolio.parcours,
        "nombre_visite": db_portfolio.nombre_visite,
        "langue": db_portfolio.langue,
        "lien_portfolio": db_portfolio.lien_portfolio,
        "id": db_portfolio.id,
        "lettre_introduction": db_portfolio.lettre_introduction,
        "domaine": db_portfolio.domaine,
        "experience_professionnelle": db_portfolio.experience_professionnelle,
        "skills": db_portfolio.skills,
        
    }

app.include_router(portfolio_router, tags=['portfolio'])
if __name__ == '__main__':
	uvicorn.run('main:app', host='0.0.0.0', port=8008, reload=True)
