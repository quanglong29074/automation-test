import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, Browser, BrowserProfile

# Load biến môi trường từ file .env
load_dotenv()

async def run_testcase_from_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        steps = f.read()

    profile = BrowserProfile(headless=False)
    browser = Browser(browser_profile=profile)

    agent = Agent(
        browser=browser,
        task=steps,
        model="openrouter/sonoma-dusk-alpha" , # chỉ định model rõ ràng
        max_tokens=1024,
    )
    result = await agent.run()
    print("Kết quả:", result)

if __name__ == "__main__":
    asyncio.run(run_testcase_from_file("tests/testcase1.yaml"))
