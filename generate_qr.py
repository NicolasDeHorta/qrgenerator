import qrcode
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel, Field

class QRCodeData(BaseModel):
    border_width: int = Field(default=4, description="Width of the QR code border")
    box_size: int = Field(default=10, description="Size of each box in the QR code")
    text: str = Field(default="", description="Text to encode in the QR code")
    fill_color: str = Field(default="black", description="Color of the QR code")
    back_color: str = Field(default="white", description="Background color of the QR code")

def generate_qr_code(qr_data: QRCodeData) ->  Image.Image:
    """
    Generate a QR code from the given data and save it to a file.
    
    :param data: The data to encode in the QR code.
    :param filename: The filename to save the QR code image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=qr_data.box_size,
        border=qr_data.border_width,
    )

    qr.add_data(qr_data.text)
    qr.make(fit=True)

    img = qr.make_image(fill_color=qr_data.fill_color, back_color=qr_data.back_color)
    return img.get_image()

def add_logo(qr_img, logo_path, bg_color, logo_size_ratio=0.2, padding_ratio=1.4):
    logo = Image.open(logo_path).convert("RGBA")

    # Redimensionar logo proporcional al tamaño del QR
    qr_width, qr_height = qr_img.size
    logo_size = int(min(qr_width, qr_height) * logo_size_ratio)
    logo = logo.resize((logo_size, logo_size))

    circle_size = int(logo_size * padding_ratio)
    circle = Image.new("RGBA", (circle_size, circle_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, circle_size, circle_size), fill=(bg_color))
    # Calcular posición centrada

    offset = ((circle_size - logo_size) // 2, (circle_size - logo_size) // 2)
    circle.paste(logo, offset, mask=logo)

    # Pegar logo sobre QR (con transparencia)
    qr_img = qr_img.convert("RGBA")
    pos = ((qr_width - circle_size) // 2, (qr_height - circle_size) // 2)
    qr_img.paste(circle, pos, mask=circle)

    return qr_img.convert("RGB")


def add_bottom_text(qr_img, bg_color, fill_color, text, text_ratio=0.07, padding_ratio=0.15):
    qr_width, qr_height = qr_img.size

    # Estimar altura del área para el texto
    bar_height = int(qr_height * padding_ratio)
    font_size = int(qr_height * text_ratio)

    # Crear nueva imagen con espacio adicional para el texto
    new_img = Image.new("RGB", (qr_width, qr_height + bar_height), bg_color)
    new_img.paste(qr_img, (0, 0))

    # Dibujar fondo del texto
    draw = ImageDraw.Draw(new_img)
    draw.rectangle([(0, qr_height), (qr_width, qr_height + bar_height)], fill=bg_color)

    # Cargar fuente y medir texto
    font = ImageFont.load_default(font_size)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Dibujar texto centrado
    text_x = (qr_width - text_width) // 2
    text_y = qr_height*0.98 + (bar_height - text_height) // 2
    draw.text((text_x, text_y), text, fill=fill_color, font=font, stroke_width=0.3)

    return new_img