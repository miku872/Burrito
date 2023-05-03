import requests


def getResponse(url):
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except:
        print("error accessing the api")
        raise

# def getResponse(uri, method, authToken, params, Bearer):
#     return

