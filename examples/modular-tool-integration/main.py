"""Hello World - Single Agent Example with Modular Tool Integration."""
from glaip_sdk import Agent
from tools.flight_status import FlightStatusTool
from tools.stock_checker import StockCheckerTool
from tools.travel_math import TravelMathTool
from tools.weather import WeatherTool

travel_agent = Agent(
    name="travel-planning-assistant",
    instruction="You are a travel planning assistant.",
    tools=[WeatherTool, FlightStatusTool, StockCheckerTool, TravelMathTool],
)
travel_agent.deploy()
travel_agent.run("Check flight GA123 and weather in Bali.")
