import requests
import time


targets = [

"/admin",
"/config",
"/debug-console",
"/admin-dev-x3"

]


for t in targets:

    try:

        url = f"http://127.0.0.1:9000{t}"

        requests.get(url)

        print("Attacked:", t)

    except:

        pass

    time.sleep(2)