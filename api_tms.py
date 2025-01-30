import requests

api_url = "https://portal-tms.stone.com.br/api"
api_key = "" #Commit sem a chave até criptografar ela
header = {
    "Authorization": api_key,
    "Accept": "application/json"
}

def executa_req(url, header, params):
    response = requests.get(url, headers=header, params=params)

    if(response.status_code == 200):
        dados = response.json()
        print(dados)
        return dados
    else:
        print(f"Erro {response.status_code}: {response.text}")

def get_application_id(application_name):
    url = f"{api_url}/applications"
    params = {"name": application_name}

    retorno = executa_req(url, header, params)
    id = retorno["Data"]["ResultSet"][0]["ApplicationId"]
    print(id)
    return id

def get_releases(application_name):
    url = f"{api_url}/releases"

    application_id = get_application_id(application_name)
    params = {"applicationIds": application_id}

    retorno = executa_req(url, header, params)
    releases = retorno["Data"]["ResultSet"]

    for release in releases:
        #Pending = 1, Staging = 2, WaitingApproval = 3, ApprovalAccepted = 4,
        #ApprovalDeclined = 5, Pilot = 6, Rollout = 7, Disabled = 8, Obsolete = 9
        if release["ReleaseState"] == 6 or release["ReleaseState"] == 7:
            versionName = release["Packages"][0]["Version"]
            versionCode = release["Packages"][0]["ManufacturerVersion"]

            break

    print(versionCode)
    print(versionName)
    return versionName, versionCode
    

get_releases("br.com.festpay.vendas")