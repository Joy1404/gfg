from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.workflow import chatbot, config
from langchain_core.messages import HumanMessage, ToolMessage
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
        print("Received message:", prompt.message)
        # Invoke the LangGraph chatbot — it decides whether to use tools
        response = chatbot.invoke(
            {"messages": [HumanMessage(content=prompt.message)]},
            config=config
        )

        messages = response["messages"]
        ai_response = messages[-1].content

        # Check if sql_generator tool was called
        tool_result = None
        for msg in messages:
            if isinstance(msg, ToolMessage):
                try:
                    parsed_msg = json.loads(msg.content)
                    if isinstance(parsed_msg, dict) and "sql_query" in parsed_msg:
                        tool_result = parsed_msg
                except (json.JSONDecodeError, TypeError):
                    pass

        if tool_result and "sql_query" in tool_result:
            # Data query — fetch results and return with chart info
            sql = tool_result["sql_query"]
            chart_type = tool_result["chart_type"]
            x_axis = tool_result.get("x_axis")
            y_axis = tool_result.get("y_axis")

            columns, rows = fetch_data(sql)
            data = [dict(zip(columns, row)) for row in rows]

            return {
                "success": True,
                "type": "data",
                "prompt": prompt.message,
                "response": ai_response,
                "sql_query": sql,
                "chart_type": chart_type,
                "x_axis": x_axis,
                "y_axis": y_axis,
                "data": data
            }
        else:
            # Normal chat — just return the conversational response
            return {
                "success": True,
                "type": "chat",
                "prompt": prompt.message,
                "response": ai_response
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
