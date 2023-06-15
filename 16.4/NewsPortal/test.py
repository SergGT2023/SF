from dotenv import load_dotenv

from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


a = os.getenv("PASS_KEY")
b = os.getenv("DEFF_EMAIL")
c = os.getenv("HOST_EMAIL")


print(a,b,c)