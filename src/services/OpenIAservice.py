import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

client = OpenAI(
  api_key=os.getenv("API_KEY")
)

async def emojifyPhrase(phrase):    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    store=True,
    messages=[
        {"role": "user", "content": "Converta a próxima frase em emoji: " + phrase}
    ]
    )
    
    result  = completion.choices[0].message.content
    
    return result



