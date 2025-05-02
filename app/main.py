from fastapi import FastAPI, HTTPException, Request
from app.scheduler import scheduler, fetch_and_update_configs  # Scheduler code
from bot.main_bot import setup_webhook, bot
import telebot

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the V2Ray Config API!"}

@app.post("/")
async def handle_webhook(request: Request):
    """
    Handle Telegram webhook updates.
    """
    try:
        # Log the incoming request
        json_data = await request.json()
        print("Received webhook update:", json_data)

        # Process the update using telebot
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return {"ok": True}
    except Exception as e:
        print("Error processing webhook update:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
        
        

    
@app.get("/configs/{config_type}")
def get_configs(config_type: str, limit: int = 5):
    """
    Fetch configurations of the specified type and limit the results.
    Args:
        config_type (str): The type of configurations to fetch (e.g., "VMess").
        limit (int): The number of configurations to fetch.
    Returns:
        dict: Contains the type and a list of configurations.
    """
    from app.utils import read_configs
    configs = read_configs(config_type, count=limit)
    if not configs:
        raise HTTPException(status_code=404, detail=f"No configurations found for type '{config_type}'")

    return {
        "type": config_type,
        "configs": configs
    }

@app.on_event("startup")
async def startup_event():
    print("Starting application and initializing scheduler...")

    # Perform an initial fetch of configs
    fetch_and_update_configs()

    # Start the scheduler
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started successfully.")

    # Set up the bot webhook
    print("Setting up Telegram bot webhook...")
    setup_webhook()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down application...")

    # Stop the scheduler
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Scheduler shut down successfully.")
