from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.tools.sql_generator import sql_generator
import psycopg2
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chat(BaseModel):
    message: str

def fetch_data(sql_query):
    conn = psycopg2.connect(
      host="aws-1-ap-southeast-1.pooler.supabase.com",
      database="postgres",
      user="postgres.ddmzvulqgwojyfnswvif",
      password="Soumyajit@185",
      port=5432,
      sslmode="require"
    )
    cur = conn.cursor()
    cur.execute(sql_query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return columns, rows

@app.get("/")
def health():
    return {
        "success": True,
        "message": "API is running"
    }

@app.post("/chat")
def chat(prompt: Chat):
    try:
        result = json.loads(sql_generator(prompt.message))
        sql = result["sql_query"]
        chart_type = result["chart_type"]

        columns, rows = fetch_data(sql)
        data = [dict(zip(columns, row)) for row in rows]

        return {
            "success": True,
            "prompt": prompt.message,
            "sql_query": sql,
            "chart_type": chart_type,
            "data": data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

