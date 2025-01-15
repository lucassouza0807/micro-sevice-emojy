from fastapi import FastAPI, Request, HTTPException
from src.services.OpenIAservice import emojifyPrase

async def get_body(request: Request):
    try:
        # Tentando pegar o corpo da requisição
        body = await request.json()
        
        # Verificando se a chave 'prompt' está presente
        if 'prompt' not in body:
            raise HTTPException(status_code=400, detail="Missing 'prompt' key in request body.")
        
        # Chamando a função para 'emojificar' a frase
        emojifiedPrase = emojifyPrase(body['prompt'])
        
        # Criando o resultado
        result = {"phrase": emojifiedPrase}
        
        return JSONResponse(content=result)

    except KeyError as e:
        # Caso a chave 'prompt' não esteja presente no corpo da requisição
        return JSONResponse(
            status_code=400,
            content={"error": f"Missing key: {str(e)}"}
        )
    
    except Exception as e:
        # Capturando qualquer outro erro
        return JSONResponse(
            status_code=500,
            content={"error": f"An unexpected error occurred: {str(e)}"}
        )
