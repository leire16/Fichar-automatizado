from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.microsoft import EdgeChromiumDriverManager
import sys
import os
import time
sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime
import sys

# Lista de festivos en España (País Vasco) en formato YYYY-MM-DD (2025) mas vacaciones
FESTIVOS = {
    "2025-01-01",  # Año Nuevo
    "2025-01-06",  # Reyes Magos
    "2025-04-17",  # Jueves Santo
    "2025-04-18",  # Viernes Santo
    "2025-04-21",  # Festivo País Vasco
    "2025-05-01",  # Día del Trabajador
    "2025-05-30",  # Musical Askartza Martxa
    "2025-06-12",  # Viaje Port Aventura
    "2025-06-13",  # Viaje Port Aventura
    "2025-07-25",  # Santiago Apóstol
    "2025-07-31",  # San Ignacio de Loyola
    "2025-08-15",  # Asunción de la Virgen
    "2025-08-22",  # Día Grande de Bilbao
    "2025-10-12",  # Día de la Hispanidad
    "2025-11-01",  # Todos los Santos
    "2025-12-06",  # Día de la Constitución
    "2025-12-08",  # Inmaculada Concepción
    "2025-12-25",  # Navidad

    # Vacaciones julio (solo lunes a viernes)
    "2025-07-18",
    "2025-07-21",
    "2025-07-22",
    "2025-07-23",

    # Vacaciones agosto (solo lunes a viernes)
    "2025-08-01",
    "2025-08-04",
    "2025-08-05",
    "2025-08-06",
    "2025-08-07",
    "2025-08-08",
    "2025-08-11",
    "2025-08-12",
    "2025-08-13",
    "2025-08-14",
    # "2025-08-15",  # Ya estaba
    "2025-08-18",
    "2025-08-19",
    "2025-08-20",
    "2025-08-21",
    # "2025-08-22",  # Ya estaba
    "2025-08-25"
}

# Obtener la fecha actual
hoy = datetime.today().strftime('%Y-%m-%d')

# Comprobar si hoy es festivo
if hoy in FESTIVOS:
    print(f"📅 Hoy ({hoy}) es festivo. No se ejecutará el fichaje.")
    sys.exit(0)

print(f"✅ Hoy ({hoy}) no es festivo. Procediendo con el fichaje...")


# Obtener credenciales desde variables de entorno
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not USERNAME or not PASSWORD:
    print("❌ ERROR: Las credenciales no están configuradas correctamente.")
    sys.exit(1)

# Configurar WebDriver para Edge
# Como está en la misma carpeta, solo pones el nombre del archivo
driver_path = "msedgedriver.exe"

service = Service(executable_path=driver_path)
#service = Service(EdgeChromiumDriverManager().install())
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

    # Esperar un momento a que se cargue un posible mensaje de error
    time.sleep(2)

    # Verificar si aparece el mensaje de error de login
    error_elements = driver.find_elements(By.XPATH, "//p[contains(@class, 'alert-danger') and contains(text(), 'Nombre de usuario o contraseña incorrectos')]")

    if error_elements:
        print("❌ ERROR: Usuario o contraseña incorrectos.")
        driver.quit()
        sys.exit(1)

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
