from fastapi import APIRouter,Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
from security import *
from portfolio.model import portfolio, portfolio_create, portfolio_update 
from db import get_db
from requests import Session

portfolio_router = APIRouter(prefix="/portfolio", tags=['portfolio'])



@portfolio_router.get("/", dependencies=[Depends(get_current_active_user)])
async def get_all_portfolio(db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).all()	
	return db_portfolio

@portfolio_router.get("/{id}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_id(id: int, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.id == id).first()
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.post("/", dependencies=[Depends(get_current_active_user)])
async def create_portfolio(portfolio_post: portfolio_create,db: Session = Depends(get_db)):
	db_portfolio = portfolio(**portfolio_post.model_dump())
	
	db.add(db_portfolio)
	db.commit()
	db.refresh(db_portfolio)
	return db_portfolio

@portfolio_router.patch("/upload/photo/{id}", dependencies=[Depends(get_current_active_user)])
async def loadPhoto(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.id == id).first()
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	if file.content_type != "image/jpeg" :
		raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
	
	if not os.path.exists("upload"):
		os.mkdir("upload", exist=True)
	if os.path.exists("upload/"+db_portfolio.photo): 
		os.remove("upload/"+db_portfolio.photo)
	db_portfolio.photo = file.filename
	with open("upload/"+file.filename, "wb") as buffer:
		buffer.write(file.file.read())
	db.commit()
	db.refresh(db_portfolio)
	return db_portfolio

@portfolio_router.put("/{id}", dependencies=[Depends(get_current_active_user)])
async def update_portfolio(id: int, portfolio_put: portfolio_update, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.id == id).first()
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	for key, value in portfolio_put.model_dump().items():
		if value is not None:
			setattr(db_portfolio, key, value)
	db.commit()
	db.refresh(db_portfolio)
	return db_portfolio

@portfolio_router.delete("/{id}", dependencies=[Depends(get_current_active_user)])
async def delete_portfolio(id: int, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.id == id).first()
	if not portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	if os.path.exists("upload/"+db_portfolio.photo):
		os.remove("upload/"+db_portfolio.photo)
	db.delete(db_portfolio)
	db.commit()
	return {"message": "portfolio deleted successfully"}

@portfolio_router.get("/photo/{id}")
async def get_image(id: int, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.id == id).first()
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return FileResponse("upload/"+db_portfolio.photo)

@portfolio_router.get("/{lien_portfolio}")
async def get_portfolio_by_lien_portfolio(lien_portfolio: str, request: Request,db: Session = Depends(get_db) ):
	db_portfolio = db.query(portfolio).filter(portfolio.lien_portfolio == lien_portfolio).first()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")


	return templates.TemplateResponse(template_list[db_portfolio.template], {"request": request, "portfolio": db_portfolio})

@portfolio_router.get("/{template}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_template(template: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.template == template).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.get("/{titre}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_titre(titre: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.titre == titre).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.get("/{loisir}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_loisir(loisir: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.loisir == loisir).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.get("/{domaine}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_domaine(domaine: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.domaine == domaine).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.get("/{parcours}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_parcours(parcours: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.parcours == parcours).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.get("/{experience_professionnelle}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_experience_professionnelle(experience_professionnelle: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.experience_professionnelle == experience_professionnelle).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.get("/{nombre_visite}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_nombre_visite(nombre_visite: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.nombre_visite == nombre_visite).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio

@portfolio_router.get("/{id_user}", dependencies=[Depends(get_current_active_user)])
async def get_portfolio_by_id_user(id_user: str, db: Session = Depends(get_db)):
	db_portfolio = db.query(portfolio).filter(portfolio.id_user == id_user).all()	
	if not db_portfolio:
		raise HTTPException(status_code=404, detail="portfolio not found")
	return db_portfolio
