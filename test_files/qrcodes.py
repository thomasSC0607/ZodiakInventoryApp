import qrcode

# Datos que deseas codificar
data = "https://www.youtube.com"

# Crear el objeto QR Code
qr = qrcode.QRCode(
    version=1,  # Controla el tamaño del QR (1 es el más pequeño, 40 es el más grande)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
    box_size=10,  # Tamaño de cada cuadro del QR
    border=4,  # Tamaño del borde (mínimo es 4)
)

# Agregar datos al QR
qr.add_data(data)
qr.make(fit=True)

# Crear la imagen del QR
img = qr.make_image(fill_color="blue", back_color="yellow")

# Guardar la imagen
img.save("qrcodeblue.png")