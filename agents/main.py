import os
import sys
import json
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
from google import genai
from google.genai import types
import redis.asyncio as redis

class AgentFileResponse(BaseModel):
    file_path: str = Field(description="The absolute path where the file should be saved, e.g., /app/project/tailwind/research/button-spec.md")
    content: str = Field(description="The actual markdown or code content to be written to the file.")

# --- 1. Environment Setup ---
AGENT_TYPE = os.getenv('AGENT_TYPE', 'main')
PROMPT_PATH = f"/app/agents/prompts/{AGENT_TYPE}.md"
COMMON_GOAL_PATH = "/app/project/common-goal.md"
REDIS_HOST = "redis" # Matches the service name in docker-compose.yml
REDIS_PORT = 6379

# --- 2. Load Prompts at Startup ---
try:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        persona_prompt = f.read()
    with open(COMMON_GOAL_PATH, "r", encoding="utf-8") as f:
        common_goal = f.read()

    SYSTEM_INSTRUCTION = f"{persona_prompt}\n\n---\n# APPENDIX: System-Wide Common Goal\n{common_goal}"
    print(f"[{AGENT_TYPE}] Successfully loaded persona and common goal.")
except FileNotFoundError as e:
    print(f"CRITICAL: Could not load prompt files for {AGENT_TYPE}. Error: {e}")
    sys.exit(1)

# --- 3. Initialize Gemini Client ---
try:
    client = genai.Client()
except Exception as e:
    print(f"CRITICAL: Failed to initialize Gemini Client. Error: {e}")
    sys.exit(1)

# --- 4. Redis Background Listener (For Sub-Agents) ---
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def listen_for_tasks():
    queue_name = f"queue:{AGENT_TYPE}"
    print(f"[{AGENT_TYPE}] Listening for tasks on Redis queue: '{queue_name}'...")
    
    while True:
        try:
            result = await redis_client.blpop(queue_name, timeout=0)
            if result:
                _, message_data = result
                task = json.loads(message_data)
                task_id = task.get("task_id")
                prompt = task.get("prompt")
                
                print(f"[{AGENT_TYPE}] Received Task {task_id}. Generating blueprint...")
                
                # 1. Ask Gemini to generate the content AS A JSON OBJECT
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Task: {prompt}\n\nAnalyze this task and provide your specification blueprint. You must return a JSON object with 'file_path' and 'content'.",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.2,
                        # Force strict JSON output matching our Pydantic schema
                        response_mime_type="application/json",
                        response_schema=AgentFileResponse, 
                    )
                )
                
                # 2. Parse the JSON response
                try:
                    # Gemini returns the stringified JSON in response.text
                    generated_data = json.loads(response.text)
                    file_path = generated_data.get("file_path")
                    file_content = generated_data.get("content")
                    
                    # Security/Sanity Check: Ensure they are writing to the shared project volume
                    if not file_path.startswith("/app/project/"):
                        # Force it into the correct directory if the agent hallucinates a weird path
                        filename = os.path.basename(file_path)
                        # Remove the prefix "sub-agent-" to just get "tailwind" or "shadcn"
                        agent_dir = AGENT_TYPE.replace("sub-agent-", "") 
                        file_path = f"/app/project/{agent_dir}/research/{filename}"
                    
                    # 3. Write the file to disk
                    # Ensure the directory exists before writing
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(file_content)
                        
                    print(f"[{AGENT_TYPE}] Successfully wrote blueprint to {file_path}")
                    
                except json.JSONDecodeError as parse_error:
                    print(f"[{AGENT_TYPE}] Failed to parse LLM JSON output: {parse_error}")
                    # You might want to push a "failed" status to Redis here
                
                # 4. Notify Main Agent
                await redis_client.rpush(f"result:{task_id}", json.dumps({"status": "success", "agent": AGENT_TYPE, "file_written": file_path}))
                
        except Exception as e:
            print(f"[{AGENT_TYPE}] Error processing queue: {e}")
            await asyncio.sleep(5)

# --- 5. FastAPI Application & Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: If this is a sub-agent, start the Redis listener background task
    listener_task = None
    if AGENT_TYPE != "main":
        listener_task = asyncio.create_task(listen_for_tasks())
    yield
    # Shutdown: Clean up the background task
    if listener_task:
        listener_task.cancel()
    await redis_client.aclose()

app = FastAPI(title=f"Gemini Agent: {AGENT_TYPE}", lifespan=lifespan)

class TaskRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "online", "agent": AGENT_TYPE}

@app.post("/delegate")
async def delegate_task(request: TaskRequest):
    """Endpoint ONLY for the Main Agent to trigger sub-agents."""
    if AGENT_TYPE != "main":
        raise HTTPException(status_code=403, detail="Only the main agent can delegate tasks.")
    
    import uuid
    task_id = str(uuid.uuid4())
    
    # 1. Main agent constructs specific prompts for ALL THREE sub-agents
    tailwind_prompt = f"Provide styling and Tailwind utility classes for: {request.prompt}"
    shadcn_prompt = f"Provide shadcn component structure and accessibility requirements for: {request.prompt}"
    nextjs_prompt = f"Provide the Next.js App Router architecture, rendering strategy (Server vs Client), and data flow for: {request.prompt}"
    
    # 2. Push tasks to all three sub-agent queues
    await redis_client.rpush("queue:sub-agent-tailwind", json.dumps({"task_id": task_id, "prompt": tailwind_prompt}))
    await redis_client.rpush("queue:sub-agent-shadcn", json.dumps({"task_id": task_id, "prompt": shadcn_prompt}))
    await redis_client.rpush("queue:sub-agent-nextjs", json.dumps({"task_id": task_id, "prompt": nextjs_prompt}))
    
    # 3. Wait for ALL THREE sub-agents to finish
    print(f"[main] Dispatched task {task_id}. Waiting for 3 sub-agents...")
    results_received = 0
    
    while results_received < 3: 
        result = await redis_client.blpop(f"result:{task_id}", timeout=120)
        
        if result is None:
            raise HTTPException(
                status_code=504, 
                detail="Sub-agents timed out. They took longer than 120 seconds or crashed."
            )
            
        _, result_data = result
        results_received += 1
        print(f"[main] Received sub-agent result {results_received}/3")
        
    # 4. Read the generated blueprints to write the final code
    final_prompt = (
        f"The sub-agents have written their blueprints to /app/project/tailwind/research, "
        f"/app/project/shadcn/research, and /app/project/nextjs/research. "
        f"Using those exact architectural and styling instructions, write the final, production-ready Next.js code for: {request.prompt}"
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-pro', # Or whichever model string worked for you!
        contents=final_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2
        )
    )
    
    return {"status": "success", "task_id": task_id, "final_code": response.text}

if __name__ == "__main__":
    # Passing 'app' directly instead of a string fixes the import path error
    uvicorn.run(app, host="0.0.0.0", port=8000)