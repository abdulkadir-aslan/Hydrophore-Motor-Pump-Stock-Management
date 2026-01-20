from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import *
from warehouses.models import WorkshopExitSlip
from datetime import datetime, timedelta
import csv,io
from django.contrib import messages


@login_required(login_url="login")
@administrator
def index(request):
    return render(request,"index.html")

def excel_serial_to_date(serial):
    """
    Excel seri tarih numarasını datetime.date objesine çevirir.
    Excel'de 1 = 1900-01-01
    """
    try:
        serial = int(serial)
        return (datetime(1899, 12, 30) + timedelta(days=serial)).date()
    except:
        return None

def data_load(request):
    if request.method == "POST":
        selected_model = request.POST.get("model")
        csv_file = request.FILES.get("csv_file")

        if not selected_model:
            messages.warning(request, "Lütfen bir model seçin.")
            return render(request, "data_load.html")

        if not csv_file:
            messages.warning(request, "Lütfen bir CSV dosyası yükleyin.")
            return render(request, "data_load.html")

        # CSV dosyasını UTF-8-sig ile okuma
        decoded_file = io.StringIO(csv_file.read().decode('utf-8-sig'))

        # Satır sonu karakterlerini temizleyelim (Alt+Enter sorununu çözüyoruz)
        cleaned_data = []
        for line in decoded_file:
            # Alt+Enter'ı (yeni satır karakteri) boşluk ile değiştiriyoruz
            # Böylece her hücreyi tek satırda tutuyoruz
            cleaned_data.append(line.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').strip())

        # Temizlenmiş veriyi tekrar StringIO'ya yazıyoruz
        cleaned_file = io.StringIO("\n".join(cleaned_data))

        # CSV okuyucu ile veriyi okuyoruz
        reader = csv.reader(cleaned_file, delimiter='$', quotechar='"')

        if selected_model == "WorkshopExitSlip":
            for row in reader:
                # Satırdaki her hücreyi temizliyoruz
                lines = [x.strip() for x in row]

                # Eğer gelen veri 19 alanlıysa işle, aksi takdirde uyarı ver
                if len(lines) < 19:
                    messages.warning(request, f"Gelen veri eksik. Beklenen 19 alan, gelen: {len(lines)}")
                    continue

                try:
                    # Tarih alanını kontrol et
                    raw_date = lines[0]
                    if raw_date.isdigit():
                        date_obj = excel_serial_to_date(raw_date)
                        if date_obj is None:
                            raise ValueError("Excel tarih serisi hatalı.")
                    else:
                        # Tarih formatı hatası olmaması için BOM temizleme
                        raw_date = raw_date.strip()  # BOM karakterinden kurtulmak için
                        date_obj = datetime.strptime(raw_date, "%d.%m.%Y").date()

                    # Veriyi kaydediyoruz
                    WorkshopExitSlip.objects.create(
                        date=date_obj,
                        slip_no=lines[1],
                        well_no=lines[2],
                        district=lines[3],
                        address=lines[4],
                        motor_type=lines[5],
                        hydrofor_no=lines[6],
                        brand=lines[7],
                        power=lines[8],
                        pump_type=lines[9],
                        pump_brand=lines[10],
                        submersible=lines[11],
                        motor=lines[12],
                        pump=lines[13],
                        hydrofor=lines[14],
                        main_pipe=lines[15],
                        secondary_pipe=lines[16],
                        maintenance_status=lines[17],
                        overall_status=lines[18],
                    )
                    messages.success(request, f"{lines[1]} kaydı başarıyla eklendi.")
                except Exception as e:
                    messages.warning(request, f"{lines[1]} kaydı sırasında hata: {str(e)}")

    return render(request, "data_load.html")
