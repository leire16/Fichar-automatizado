from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import sys
import os
import time
sys.stdout.reconfigure(encoding='utf-8')

# Obtener credenciales desde variables de entorno
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

print("USERNAME:", USERNAME)
print("PASSWORD:", PASSWORD)

if not USERNAME or not PASSWORD:
    print("❌ ERROR: Las credenciales no están configuradas correctamente.")
    sys.exit(1)

# Configurar WebDriver para Edge
service = Service(EdgeChromiumDriverManager().install())
options = Options()
options.add_argument("--headless") #modo sin abrir el navegador

# Iniciar el navegador
driver = webdriver.Edge(service=service, options=options)

# URL de inicio de sesión
login_url = "https://erp.teknei.es/web#cids=1%2C72%2C77%2C78%2C79&menu_id=327&action=460"
driver.get(login_url)

try:
    # Esperar que los campos de usuario y contraseña estén presentes
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "login"))
    )
    print("✔ Página de inicio de sesión cargada con éxito")

    # Encontramos los campos de usuario y contraseña
    username_field = driver.find_element(By.ID, "login")  # Usamos el ID del campo de usuario
    password_field = driver.find_element(By.ID, "password")  # Usamos el ID del campo de contraseña

     # Ingresa tus credenciales usando las variables de entorno
    username_field.send_keys(USERNAME)  # Usuario
    password_field.send_keys(PASSWORD)  # Contraseña

    # Hacemos clic en el botón de inicio de sesión usando la clase del botón
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")  # Usamos el selector CSS de la clase
    login_button.click()

    # Esperar que la página de inicio después de iniciar sesión esté disponible
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    print("✔ Inicio de sesión exitoso")

    # Asegúrate de que el botón sea visible y esté habilitado
    boton_fichar = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'o_hr_attendance_sign_in_out_icon')]//span[contains(text(),'Entrada') or contains(text(),'Salida')]"))
    )

    # Imprimir el texto del botón encontrado, si es que hay algún texto
    print(f"Botón fichar encontrado con el texto: {boton_fichar.text}")
    
    # Realizar clic en el botón (descomenta si lo necesitas)
    boton_fichar.click()
    
    print("✔ Fichaje realizado con éxito")
except Exception as e:
    print(f"❌ No se pudo encontrar el botón de fichaje: {e}")
    
time.sleep(3)
driver.quit()  # Cierra Edge después de fichar


	  