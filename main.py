from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class PhoneNumber(BaseModel):
    number: str

def validate_brazilian_phone(number: str) -> bool:
    """
    Valida um número de celular brasileiro no formato +55XXXXXXXXXX
    ou (XX)9XXXX-XXXX.
    """
    pattern = r"^\+55\d{11}$"  # Validação para formato +55XXXXXXXXXXX (com código do Brasil)
    local_pattern = r"^\(?\d{2}\)?9\d{4}-?\d{4}$"  # Validação para formato (XX)9XXXX-XXXX
    return bool(re.match(pattern, number) or re.match(local_pattern, number))

@app.post("/validate-phone/")
async def validate_phone(phone: PhoneNumber):
    if validate_brazilian_phone(phone.number):
        return {"status": "valid", "message": "Número de celular válido."}
    else:
        raise HTTPException(status_code=400, detail="Número de celular inválido.")
