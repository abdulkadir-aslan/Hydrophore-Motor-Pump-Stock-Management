from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import administrator
from warehouses.models import (
    WorkshopExitSlip, Inventory, Pump, Engine,
    Mark, Power, Seconhand, NewWarehousePump
)
from hydrophore.models import Power as HydrophorePower, PumpType, Hydrophore
from datetime import datetime, timedelta
import io, re
from django.contrib import messages
from django.db import transaction
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast, Substr


@login_required(login_url="login")
@administrator
def index(request):
    return render(request, "index.html")


# -------------------------------------------------
# GENEL YARDIMCI FONKSİYONLAR
# -------------------------------------------------

def excel_serial_to_date(serial):
    try:
        serial = int(serial)
        return (datetime(1899, 12, 30) + timedelta(days=serial)).date()
    except:
        return None


def merge_broken_lines(file_obj):
    buffer = ""
    for line in file_obj:
        line = line.rstrip("\n")
        buffer = buffer + " " + line if buffer else line
        if buffer.count('"') % 2 == 0:
            yield buffer
            buffer = ""
    if buffer:
        yield buffer


def parse_broken_csv_line(line):
    line = line.strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]
    line = line.replace('""', '"')
    return [c.strip() for c in line.split('$')]


# -------------------------------------------------
# DATA LOAD VIEW
# -------------------------------------------------

def data_load(request):
    if request.method == "POST":
        model = request.POST.get("model")
        file = request.FILES.get("csv_file")

        if not model:
            messages.warning(request, "Lütfen bir model seçin.")
            return render(request, "data_load.html")

        if not file:
            messages.warning(request, "Lütfen bir CSV dosyası seçin.")
            return render(request, "data_load.html")

        try:
            if model == "Inventory":
                count = load_inventory_from_csv(file, request)

            elif model == "Seconhand":
                count = load_seconhand_from_csv(file, request)

            elif model == "Hydrophore":
                count = load_hydrophore_from_csv(file, request)

            elif model == "NewEngine":
                count = load_new_engine_from_csv(file, request, location="5")

            elif model == "mütahit":
                count = load_new_engine_from_csv(file, request, location="6")

            elif model == "NewWarehousePump":
                count = load_new_warehouse_pump_from_csv(file, request)

            elif model == "WorkshopExitSlip":
                count = load_workshop_exit_slip_from_csv(file, request)
                 
            else:
                messages.warning(request, "Geçersiz model seçimi.")
                return render(request, "data_load.html")

            messages.success(request, f"{count} kayıt başarıyla işlendi.")

        except Exception as e:
            messages.error(request, f"Hata oluştu: {str(e)}")

    return render(request, "data_load.html")


# -------------------------------------------------
# PARSE FONKSİYONLARI
# -------------------------------------------------

def parse_mark(value):
    # Boş / None / sadece boşluk ise "-"
    if not value or not value.strip():
        name = "-"
    else:
        name = re.sub(
            r'\s+',
            ' ',
            value.replace('"', '').strip().upper()
        )

    return Mark.objects.get_or_create(
        engine_mark=name
    )[0]

def parse_power(value):
    if not value:
        return None
    raw = value.lower()
    match = re.search(r'(\d+(\.\d+)?)', raw)
    if not match:
        return None
    power_val = float(match.group(1))
    if power_val.is_integer():
        power_val = int(power_val)
    return Power.objects.get_or_create(engine_power=power_val)[0]


ENGINE_TYPE_MAP = {
    "3′": "1", "4′": "2", "5′": "3", "6′": "4",
    "7′": "5", "8′": "6", "9′": "7",
    "10′": "8", "11′": "9",
    "ASENKRON": "10", "-": "11"
}

SERIAL_COUNTER = 1


def parse_engine(engine_type_raw, engine_power_raw, engine_mark_raw, serial_raw, location):
    global SERIAL_COUNTER
    engine_type = ENGINE_TYPE_MAP.get(engine_type_raw.strip(), "11")
    serial = serial_raw.strip() if serial_raw else None

    if not serial:
        serial = f"GİRİLMEMİŞ-{SERIAL_COUNTER}"
        SERIAL_COUNTER += 1

    return Engine.objects.get_or_create(
        serialnumber=serial,
        defaults={
            "engine_type": engine_type,
            "engine_power": parse_power(engine_power_raw),
            "engine_mark": parse_mark(engine_mark_raw),
            "location": location,
        }
    )[0]


def parse_pump(pump_type_raw, pump_mark_raw):
    if not pump_type_raw:
        return None
    pump_type_clean = pump_type_raw.upper()
    return Pump.objects.get_or_create(
        pump_type=pump_type_clean,
        pump_mark=parse_mark(pump_mark_raw),
        pump_breed="5"
    )[0]

# -------------------------------------------------
# WORKSHOP EXIT SLIP
# -------------------------------------------------

def load_workshop_exit_slip_from_csv(file, request):
    raw_file = io.TextIOWrapper(
        file.file,
        encoding="utf-8-sig",
        errors="ignore"
    )

    created = 0
    skipped = 0

    for logical_line in merge_broken_lines(raw_file):
        columns = parse_broken_csv_line(logical_line)

        if len(columns) != 19:
            messages.warning(
                request,
                f"Satır atlandı. Alan sayısı: {len(columns)}"
            )
            skipped += 1
            continue

        try:
            # ---------------- DATE ----------------
            raw_date = columns[0].strip()

            if raw_date.isdigit():
                date_obj = excel_serial_to_date(raw_date)
                if not date_obj:
                    raise ValueError("Excel tarih hatası")
            else:
                date_obj = datetime.strptime(
                    raw_date, "%d.%m.%Y"
                ).date()

            WorkshopExitSlip.objects.create(
                date=date_obj,
                slip_no=columns[1],
                well_no=columns[2],
                district=columns[3],
                address=columns[4],
                motor_type=columns[5],
                hydrofor_no=columns[6],
                brand=columns[7],
                power=columns[8],
                pump_type=columns[9],
                pump_brand=columns[10],
                submersible=columns[11],
                motor=columns[12],
                pump=columns[13],
                hydrofor=columns[14],
                main_pipe=columns[15],
                secondary_pipe=columns[16],
                maintenance_status=columns[17],
                overall_status=columns[18],
            )

            created += 1

        except Exception as e:
            messages.warning(
                request,
                f"Kayıt hatası (Slip No: {columns[1]}): {str(e)}"
            )
            skipped += 1

    messages.success(
        request,
        f"{created} çıkış fişi eklendi, {skipped} satır atlandı."
    )

    return created


# -------------------------------------------------
# INVENTORY
# -------------------------------------------------

def load_inventory_from_csv(file, request):
    raw = io.TextIOWrapper(file.file, encoding="utf-8-sig", errors="ignore")
    count = 0

    for i, line in enumerate(raw, 1):
        cols = [c.strip() for c in line.split('$')]
        if len(cols) < 14:
            messages.warning(request, f"Satır {i}: Eksik kolon")
            continue

        well_no = cols[0].replace('"', '')
        if Inventory.objects.filter(well_number=well_no).exists():
            messages.warning(request, f"{well_no} zaten kayıtlı.")
            continue

        engine = parse_engine(cols[8], cols[10], cols[9], cols[11], "1")
        pump = parse_pump(cols[12], cols[13])
        
        Inventory.objects.create(
            well_number=well_no,
            district=cols[1],
            address=cols[2],
            disassembly_depth=int(cols[3]) if cols[3].isdigit() else 0,
            mounting_depth=int(cols[4]) if cols[4].isdigit() else 0,
            tank_info=cols[5] or "-",
            pipe_type=cols[6] or "-",
            cable=cols[7] or "-",
            engine=engine,
            pump=pump,
        )
        count += 1

    return count


# -------------------------------------------------
# SECONHAND
# -------------------------------------------------

def ensure_seconhand_rows(limit=350):
    with transaction.atomic():
        max_num = Seconhand.objects.annotate(
            num=Cast(Substr('row_identifier', 2), IntegerField())
        ).aggregate(Max('num'))['num__max'] or 0

        for i in range(max_num + 1, limit + 1):
            Seconhand.objects.create()


def load_seconhand_from_csv(file, request):
    ensure_seconhand_rows()
    raw = io.TextIOWrapper(file.file, encoding="utf-8-sig", errors="ignore")
    updated = 0

    for i, line in enumerate(raw, 1):
        cols = [c.strip() for c in line.split('$')]
        if len(cols) < 7:
            messages.warning(request, f"Satır {i}: Eksik kolon")
            continue

        try:
            seconhand = Seconhand.objects.get(row_identifier=cols[0])
        except Seconhand.DoesNotExist:
            messages.warning(request, f"Depo bulunamadı: {cols[0]}")
            continue

        engine = parse_engine(cols[1], cols[3], cols[2], cols[4], "3") if cols[4] else None
        pump = parse_pump(cols[5], cols[6]) if cols[5] else None

        seconhand.engine = engine
        seconhand.pump = pump
        seconhand.save()
        updated += 1

    return updated


# -------------------------------------------------
# NEW ENGINE (TEK FONKSİYON)
# -------------------------------------------------

def load_new_engine_from_csv(file, request, location):
    raw = io.TextIOWrapper(file.file, encoding="utf-8-sig", errors="ignore")
    created, skipped = 0, 0

    for i, line in enumerate(raw, 1):
        cols = [c.strip() for c in line.split('$')]
        if len(cols) < 4:
            messages.warning(request, f"Satır {i}: Eksik kolon")
            skipped += 1
            continue

        serial = cols[3].replace('"', '')
        if not serial:
            messages.warning(request, f"Satır {i}: Seri numarası boş")
            skipped += 1
            continue

        parse_engine(cols[0], cols[1], cols[2], serial, location)
        created += 1

    messages.success(request, f"{created} motor eklendi, {skipped} atlandı.")
    return created


# -------------------------------------------------
# NEW WAREHOUSE PUMP
# -------------------------------------------------

def load_new_warehouse_pump_from_csv(file, request):
    raw = io.TextIOWrapper(file.file, encoding="utf-8-sig", errors="ignore")
    count = 0

    for i, line in enumerate(raw, 1):
        cols = [c.strip() for c in line.split('$')]
        if len(cols) < 3:
            messages.warning(request, f"Satır {i}: Eksik kolon")
            continue

        try:
            qty = int(cols[2])
        except:
            messages.warning(request, f"Satır {i}: Geçersiz miktar")
            continue

        pump = parse_pump(cols[0], cols[1])
        if not pump:
            messages.warning(request, f"Satır {i}: Pompa oluşturulamadı")
            continue

        obj, _ = NewWarehousePump.objects.get_or_create(pump=pump)
        obj.quantity = qty
        obj.save()
        count += 1

    return count


# -------------------------------------------------
# HIDROPHORE PARSE FONKSİYONLARI
# -------------------------------------------------

def parse_hydrophore_power(value):
    """
    '2.2 KW', '3 kw', '4.0kw' -> 2.2, 3, 4.0
    """
    if not value:
        return None

    raw = value.lower().replace('"', '').strip()

    if 'kw' not in raw:
        return None

    match = re.search(r'(\d+(\.\d+)?)', raw)
    if not match:
        return None

    power_value = float(match.group(1))

    obj, _ = HydrophorePower.objects.get_or_create(
        power=power_value
    )
    return obj


def parse_hydrophore_pump_type(value):
    if not value:
        return None

    pump_type = value.replace('"', '').strip().upper()
    pump_type = re.sub(r'\s+', ' ', pump_type)

    if not pump_type or pump_type == "-":
        return None

    obj, _ = PumpType.objects.get_or_create(type=pump_type)
    return obj


def parse_district(value):
    if not value:
        return None

    value = value.replace('"', '').strip().lower()

    district_map = {
        v.lower(): k for k, v in Hydrophore.DISTRICT_CHOICES
    }
    return district_map.get(value)


def parse_location(value):
    if not value:
        return "1"  # default: Atölyede

    value = value.replace('"', '').strip().lower()

    location_map = {
        "atölye": "1",
        "atölyede": "1",
        "atölyede tamir bekliyor": "2",
        "tamir bekliyor": "2",
        "elektrikçi": "3",
        "elektrikçide": "3",
        "kuyu": "4",
        "kuyuda": "4",
        "tamir": "5",
        "tamirde": "5",
        "sıfır": "6",
        "sıfır depo": "6",
        "pert": "7",
        "pert depo": "7",
    }

    return location_map.get(value, "1")


# -------------------------------------------------
# HIDROPHORE CSV LOAD
# -------------------------------------------------

def load_hydrophore_from_csv(file, request):
    """
    CSV Sırası:
    HIDROFOR SERI NO$MOTOR GUCU$MOTOR MARKASI$POMPA TIPI$ILCE$MAHALLE$KONUM
    """

    raw = io.TextIOWrapper(
        file.file,
        encoding="utf-8-sig",
        errors="ignore"
    )

    created = 0
    skipped = 0

    for line_no, line in enumerate(raw, start=1):
        line = line.strip()
        if not line:
            continue

        cols = [c.strip() for c in line.split('$')]

        if len(cols) < 7:
            messages.warning(request, f"Satır {line_no}: Eksik kolon")
            skipped += 1
            continue

        (
            serial_raw,
            power_raw,
            engine_brand_raw,
            pump_type_raw,
            district_raw,
            neighborhood_raw,
            location_raw,
            *_  # AG vb. fazlalıklar
        ) = cols

        serial_number = serial_raw.replace('"', '').strip().upper()
        if not serial_number:
            messages.warning(request, f"Satır {line_no}: Seri numarası boş")
            skipped += 1
            continue

        if Hydrophore.objects.filter(serial_number=serial_number).exists():
            messages.warning(
                request,
                f"Satır {line_no}: Mükerrer seri no ({serial_number})"
            )
            skipped += 1
            continue

        engine_power = parse_hydrophore_power(power_raw)
        pump_type = parse_hydrophore_pump_type(pump_type_raw)
        district = parse_district(district_raw)
        location = parse_location(location_raw)

        engine_brand = engine_brand_raw.replace('"', '').strip().upper()
        neighborhood = (
            neighborhood_raw.replace('"', '').strip().upper()
            if district else None
        )

        Hydrophore.objects.create(
            serial_number=serial_number,
            engine_power=engine_power,
            engine_brand=engine_brand,
            pump_type=pump_type,
            district=district,
            neighborhood=neighborhood,
            location=location,
        )

        created += 1

    messages.success(
        request,
        f"{created} hidrofor eklendi, {skipped} satır atlandı."
    )

    return created
