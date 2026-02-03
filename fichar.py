#from selenium import webdriver
#from selenium.webdriver.edge.service import Service
#from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
    "2026-03-19",  
    "2026-04-02",  # Jueves Santo
    "2026-04-03",  # Viernes Santo
    "2026-04-06",  # Festivo País Vasco
    "2025-05-01",  # Día del Trabajador
    # "2025-05-30",  # Musical Askartza Martxa
    "2026-07-25",  # Santiago Apóstol
    "2026-07-31",  # San Ignacio de Loyola
    "2026-08-15",  # Asunción de la Virgen
    "2026-08-22",  # Día Grande de Bilbao
    "2026-10-12",  # Día de la Hispanidad
    "2026-11-01",  # Todos los Santos
    "2026-12-06",  # Día de la Constitución
    "2026-12-08",  # Inmaculada Concepción
    "2026-12-24",  # Pre Navidad
    "2026-12-25",  # Navidad
    "2026-12-31",  # Fin Año
    "2027-01-01",  # Año Nuevo
    "2027-01-06",   # Reyes 

    # Vacaciones Enero
    "2026-01-26",
    "2026-01-27",
    "2026-01-28",
    "2026-01-29",
    "2026-01-30",

    # Vacaciones julio 

    # Vacaciones agosto 


    #Vacaciones Diciembre

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
#driver_path = "msedgedriver.exe"

#service = Service(executable_path=driver_path)
#service = Service(EdgeChromiumDriverManager().install())
#options = Options()
#options.add_argument("--headless") #modo sin abrir el navegador

# Iniciar el navegador
#driver = webdriver.Edge(service=service, options=options)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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
