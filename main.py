import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq


load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================
# TOOL FUNCTION
# =====================
@tool
def getWeatherDetails(city: str) -> str:
    """
    Returns weather details for a given city.
    """
    c = city.lower()

    if c == "patiala":
        return "10°C"
    if c == "mohali":
        return "15°C"
    if c == "bangalore":
        return "23°C"
    if c == "chandigarh":
        return "11°C"
    if c == "delhi":
        return "16°C"

    return "Weather data not available"

# =====================
# PROMPT (CITY EXTRACT)
# =====================
CITY_EXTRACT_PROMPT = """
You are an AI assistant.
Extract ONLY the city name from the user message.
Return the result strictly in JSON format.

Example:
User: What is the weather of Patiala?
Output:
{ "city": "Patiala" }
"""

# =====================
# USER INPUT
# =====================
user_input = "Can you tell me the weather in Delhi today?"

# =====================
# AGENT LOGIC
# =====================
def run_agent():
    print("STATE: START")
    print(user_input)

    # ---- CITY EXTRACTION ----
    response = llm.invoke([
        SystemMessage(content=CITY_EXTRACT_PROMPT),
        HumanMessage(content=user_input)
    ])

    raw_text = response.content
    print("\nSTATE: CITY EXTRACT RAW")
    print(raw_text)

    try:
        city = eval(raw_text)["city"]
    except Exception:
        print("❌ Could not extract city")
        return

    # ---- ACTION ----
    print("\nSTATE: ACTION")
    print(f'getWeatherDetails(city="{city}")')

    # ---- OBSERVATION ----
    weather = getWeatherDetails.invoke(city)
    print("\nSTATE: OBSERVATION")
    print(weather)

   
    print("\nSTATE: OUTPUT")
    print(f"✅ FINAL OUTPUT:\nWeather of {city}: {weather}")


run_agent()
