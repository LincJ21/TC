# routers/consulta.py
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from utils import consultar_productos

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/consulta")
async def consulta(request: Request, cc: str = Form(...)):
    try:
        productos_familiar, productos_internet, productos_entretenimiento = consultar_productos(cc)
        
        return templates.TemplateResponse(
            "listacompras.html",
            {"request": request, "productos_familiar": productos_familiar,
             "productos_internet": productos_internet, "productos_entretenimiento": productos_entretenimiento}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la consulta: {e}")
