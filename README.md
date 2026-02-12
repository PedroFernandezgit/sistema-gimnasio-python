 # Sistema de Gestión de Cuotas - Gimnasio

Aplicación desarrollada en Python para gestionar vencimientos de cuotas de socios y enviar recordatorios automáticos por correo electrónico.

## Funcionalidades

- Cálculo automático de vencimientos
- Envío de correos recordatorios (SMTP)
- Visualización de vencimientos próximos
- Manejo de datos con Pandas
- Uso de variables de entorno para credenciales

## Tecnologías

- Python
- Pandas
- Yagmail
- datetime

## Configuración

Las credenciales deben configurarse como variables de entorno:

```
EMAIL_GIMNASIO=tu_email
PASSWORD_APP=tu_password
```

## Archivo de clientes

El sistema requiere un archivo llamado:

clientes.csv

El archivo debe contener las siguientes columnas:

nombre,email,fecha_pago

Ejemplo:

Juan Perez,juan@example.com,2025-01-01
Maria Lopez,maria@example.com,2025-01-15

La fecha debe estar en formato:

YYYY-MM-DD

Se incluye un archivo `clientes_ejemplo.csv` como referencia.

## Ejecución

```
python gimnasio.py
```
