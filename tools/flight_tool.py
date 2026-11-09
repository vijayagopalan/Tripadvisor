import os
from dotenv import load_dotenv
import airportsdata
load_dotenv()

aviation_key = os.getenv("AVIATION_STACK_API_KEY")
aviation_base_url = os.getenv("AVIATION_BASE_URL")
default_origin = os.getenv("DEFAULT_ORIGIN_DATA")
airports = airportsdata.load("IATA")

