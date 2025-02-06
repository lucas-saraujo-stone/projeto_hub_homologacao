from pyaxmlparser import APK
import os

def tamanho_apk(path_apk, versionamento):
    tamanho_bytes = os.path.getsize(path_apk)
    print(f"Tamanho em Bytes: {tamanho_bytes}")

    tamanho_mb = tamanho_bytes / (1024 * 1024)
    print(f"Tamanho em MB: {tamanho_mb.__round__(1)}")

    if tamanho_mb > 70:
        print("Olá parceiro!\n\nO apk " + path_apk + " possui um tamanho acima do limite de 70MB exigido em documentação.")
        versionamento.status = "RECUSADO"
        versionamento.motivo_recusa = "Olá parceiro!\n\n- O apk possui um tamanho acima do limite de 70MB exigido em documentação."
    else:
        print("Apk " + path_apk + " dentro do tamanho limite de 70MB exigido em documentação")

    return versionamento

def dados_apk(path_apk, versionamento):
    apk = APK(path_apk)
    versionamento.version_name = apk.version_name
    versionamento.version_code = apk.version_code
    versionamento.min_sdk_version = apk.get_min_sdk_version()
    versionamento.target_sdk_version = apk.get_target_sdk_version()

    return versionamento



#apk_path = r'C:\Users\lucas.saraujo\Downloads\maxpan.apk'

''''apk = APK(apk_path)
print(apk.package)
print(apk.version_name)
print(apk.version_code)
print(apk.get_min_sdk_version())
print(apk.get_target_sdk_version())

tamanho_bytes = os.path.getsize(apk_path)
print(f"Tamanho em Bytes: {tamanho_bytes}")

tamanho_mb = tamanho_bytes / (1024 * 1024)
print(f"Tamanho em MB: {tamanho_mb.__round__(1)}")'''
