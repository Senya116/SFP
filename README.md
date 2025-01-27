# SFP - Smart Fridge Project
## Общая информация
В данном репозитории размещены все достаточные и необходимые коды для работы приложения Smart Fridge QR Control & IoT Sync для Кейса №2 Московской Предпрофессиональной олимпиады.

Проект создан Бакулиным Глебом, Кижапкиным Александром, Малышевым Игнатом.
## Пояснение к файлам

### Папка [приложения](Приложение)

Основной алгоритм программы реализован в файле [main.py](Приложение/main.py).

Система управления базами данных реализована в файле [app](Приложение/app.py).

Генератор QR-кодов расположен в файле [generate_qr_codes](Приложение/generate_qr_codes.py).

Фрагмент кода, отвечающий за сканирование QR-кодов находится в файле [qr_scanner](Приложение/qr_scanner.py).

### Папка [QR-кодов](QR-коды)

Во всех файлах данной папк находятся изображения QR-кодов, сгенерированные кодом в [generate_qr_codes](Приложение/generate_qr_codes.py). В этих кодах содержится данные о Тушенке, Йогурте, Хлебе (Батон нарезной), Картошка.
