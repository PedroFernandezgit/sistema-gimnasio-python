import pandas as pd
from datetime import datetime, timedelta
import yagmail
import unicodedata
import os

# ================== CONFIGURACIÓN ==================

ARCHIVO = "clientes.csv"  # Archivo real (no subir con datos reales)
DIAS_PLAN = 30
AVISO_DIAS = 5
MOSTRAR_DIAS = 7

# Credenciales desde variables de entorno
EMAIL_GIMNASIO = os.getenv("EMAIL_GIMNASIO")
PASSWORD_APP = os.getenv("PASSWORD_APP")

# ===================================================


def limpiar_texto(texto):
    return (
        unicodedata
        .normalize("NFKD", str(texto))
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def cargar_clientes():
    if not os.path.exists(ARCHIVO):
        print("❌ No existe el archivo clientes.csv")
        return pd.DataFrame()

    df = pd.read_csv(ARCHIVO)

    if "fecha_pago" not in df.columns:
        print("❌ El archivo debe contener la columna 'fecha_pago'")
        return pd.DataFrame()

    df["fecha_pago"] = pd.to_datetime(
        df["fecha_pago"].astype(str).str.strip(),
        errors="coerce"
    )

    df = df.dropna(subset=["fecha_pago"])
    return df


def fecha_vencimiento(fecha_pago):
    return fecha_pago + timedelta(days=DIAS_PLAN)


def enviar_correos_vencimientos():
    if not EMAIL_GIMNASIO or not PASSWORD_APP:
        print("❌ Configura las variables de entorno EMAIL_GIMNASIO y PASSWORD_APP")
        return

    df = cargar_clientes()
    if df.empty:
        print("No hay clientes cargados.")
        return

    hoy = datetime.now().date()

    try:
        yag = yagmail.SMTP(EMAIL_GIMNASIO, PASSWORD_APP)
    except Exception as e:
        print(f"❌ Error al iniciar sesión SMTP: {e}")
        return

    enviados = 0

    for _, fila in df.iterrows():
        vence = fecha_vencimiento(fila["fecha_pago"]).date()
        dias_restantes = (vence - hoy).days

        if dias_restantes <= AVISO_DIAS:
            nombre = limpiar_texto(fila.get("nombre", "Cliente"))
            email = fila.get("email")

            if not email:
                continue

            if dias_restantes < 0:
                estado = f"Tu cuota está vencida desde hace {abs(dias_restantes)} días."
            elif dias_restantes == 0:
                estado = "Tu cuota vence hoy."
            else:
                estado = f"Te quedan {dias_restantes} días para renovar tu cuota."

            mensaje = f"""
Hola {nombre},

{estado}

Para seguir entrenando sin interrupciones, pasa por el gimnasio a renovar.

Muchas gracias.
"""

            try:
                yag.send(
                    to=email,
                    subject="Recordatorio de cuota",
                    contents=mensaje
                )
                print(f"✅ Mail enviado a {nombre} ({email})")
                enviados += 1
            except Exception as e:
                print(f"❌ Error enviando mail a {nombre}: {e}")

    if enviados == 0:
        print("ℹ️ No hay vencimientos para avisar.")


def mostrar_vencimientos():
    df = cargar_clientes()
    if df.empty:
        print("No hay clientes cargados.")
        return

    hoy = datetime.now().date()
    print("\n📋 Vencimientos próximos:\n")

    hay = False

    for _, fila in df.iterrows():
        vence = fecha_vencimiento(fila["fecha_pago"]).date()
        dias_restantes = (vence - hoy).days

        if dias_restantes <= MOSTRAR_DIAS:
            nombre = limpiar_texto(fila.get("nombre", "Cliente"))

            if dias_restantes < 0:
                estado = f"VENCIDO hace {abs(dias_restantes)} días"
            elif dias_restantes == 0:
                estado = "VENCE HOY"
            else:
                estado = f"Vence en {dias_restantes} días"

            print(f"- {nombre} | {estado} | {vence}")
            hay = True

    if not hay:
        print("No hay vencimientos próximos.")


def main():
    while True:
        print("\n===== SISTEMA DE GIMNASIO =====")
        print("1 - Enviar correos (vencen en 5 días o menos)")
        print("2 - Mostrar vencimientos próximos")
        print("0 - Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            enviar_correos_vencimientos()
        elif opcion == "2":
            mostrar_vencimientos()
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
