#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional
from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
	

class parcours(BaseModel):
	titre: str
	annee: str
	etablissement: str

class experience_professionnelle(BaseModel):
	titre: str
	annee: str
	entreprise: str
class skills(BaseModel):
	titre: str
	niveau: int
class langue(BaseModel):
	titre: str
	niveau: int
 
class portfolio_create(BaseModel):

	lien_portfolio: str
	template: int
	titre: str
	lettre_introduction: str
	loisir: list
	domaine: str
	parcours: list[parcours]
	experience_professionnelle: list[experience_professionnelle]
	skills: list[skills]
	langue: list[langue]
	nombre_visite: int
	id_user: int
 
	

class portfolio_update(BaseModel):

	lien_portfolio: Optional[str] = None
	template: Optional[int] = None
	titre: Optional[str] = None
	lettre_introduction: Optional[str] = None
	loisir: Optional[list] = None
	domaine: Optional[str] = None
	parcours: Optional[list] = None
	experience_professionnelle: Optional[list] = None
	skills: Optional[list] = None
	langue: Optional[list] = None
	nombre_visite: Optional[int] = None
	id_user: Optional[int] = None


class portfolio(Base):

	__tablename__ = 'portfolio'

	id = Column(Integer, primary_key=True, index=True)

	lien_portfolio= Column(String(255), nullable= False)
	template= Column(Integer, nullable= False)
	titre= Column(String(255), nullable= False)
	photo= Column(String(255), nullable= True, default="default.png")
	lettre_introduction= Column(String(255), nullable= False)
	loisir= Column(JSON, nullable= False)
	domaine= Column(String(255), nullable= False)
	parcours= Column(JSON, nullable= False)
	experience_professionnelle= Column(JSON, nullable= False)
	nombre_visite= Column(Integer, nullable= False)
	skills= Column(JSON, nullable= False)
	langue= Column(JSON, nullable= False)
	id_user= Column(Integer, ForeignKey("users.id"), nullable=False)
	user = relationship("UserDB", back_populates="portfolios")
