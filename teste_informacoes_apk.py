from pyaxmlparser import APK
import os

apk_path = r'C:\Users\lucas.saraujo\Downloads\maxpan.apk'

apk = APK(apk_path)
print(apk.package)
print(apk.version_name)
print(apk.version_code)
print(apk.get_min_sdk_version())
print(apk.get_target_sdk_version())

tamanho_bytes = os.path.getsize(apk_path)
print(f"Tamanho em Bytes: {tamanho_bytes}")

tamanho_mb = tamanho_bytes / (1024 * 1024)
print(f"Tamanho em MB: {tamanho_mb.__round__(1)}")
