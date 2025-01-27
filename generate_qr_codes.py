import qrcode
import json

# Пример данных о продукте
products = [
    {
        "name": "Батон нарезной",
        "type": "Хлеб",
        "manufacture_date": "2025-01-26",
        "expiry_date": "2025-02-07",
        "mass_volume": "500",
        "unit": "гр",
        "nutritional_value": "250 ккал",
        "measurement_type": "вес"
    },
    {
        "name": "Йогурт",
        "type": "Молочные продукты",
        "manufacture_date": "2025-01-25",
        "expiry_date": "2025-02-01",
        "mass_volume": "1",
        "unit": "шт",
        "nutritional_value": "100 ккал",
        "measurement_type": "штуки"
    },
    {
        "name": "Картофель",
        "type": "Овощ",
        "manufacture_date": "2024-08-14",
        "expiry_date": "2025-04-14",
        "mass_volume": "1",
        "unit": "кг",
        "nutritional_value": "830 ккал",
        "measurement_type": "вес"
    },
    {
        "name": "Тушёнка",
        "type": "Консервы",
        "manufacture_date": "1986-07-04",
        "expiry_date": "2006-07-04",
        "mass_volume": "1",
        "unit": "шт",
        "nutritional_value": "250 ккал",
        "measurement_type": "штуки"
    },
    # Добавьте больше продуктов по необходимости
]

# Функция для генерации QR-кода
def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(data))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

# Генерация QR-кодов для всех продуктов
for index, product in enumerate(products):
    filename = f"qr_code_{index + 1}.png"
    generate_qr_code(product, filename)
    print(f"QR-код для продукта '{product['name']}' сгенерирован и сохранен как {filename}")