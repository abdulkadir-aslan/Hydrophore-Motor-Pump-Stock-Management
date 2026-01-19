import sqlite3
db = sqlite3.connect("db.sqlite3")
im = db.cursor()

from datetime import datetime

def marka():
    with open('veri yükleme/marka.txt',encoding="utf-8") as f:
        for item in f.readlines():
            engine_mark = item.strip()
            try:
                im.execute("INSERT INTO warehouses_mark (engine_mark) VALUES (?)", (engine_mark,))
                print(f"Marka eklendi: {engine_mark}")
            except sqlite3.IntegrityError:
                # Marka zaten varsa, hata vermez sadece geçer
                print(f"Marka zaten mevcut: {engine_mark}")
    
    db.commit()
    # Veritabanındaki tüm markaları alalım
    im.execute("SELECT *FROM warehouses_mark")
    rows = im.fetchall()

    with open('veri yükleme/read.txt', 'w', encoding="utf-8") as read_file:
        # Dosyayı sıfırladık, şimdiden sadece güncel veriler yazılacak
        for row in rows:
            # `read.txt` dosyasına id ve marka yazalım
            read_file.write(f"{row[0]},{row[1]}\n")

def güç():
    with open('veri yükleme/güç.txt', encoding="utf-8") as f:
        for item in f.readlines():
            power = item.strip()
            try:
                im.execute("INSERT INTO warehouses_power (engine_power) VALUES (?)", (power,))
                print(f"Motor gücü eklendi: {power}")
            except sqlite3.IntegrityError:
                # Güç zaten varsa, hata vermez sadece geçer
                print(f"Motor gücü zaten mevcut: {power}")

    db.commit()

    # Veritabanındaki tüm güçleri alalım
    im.execute("SELECT * FROM warehouses_power")
    rows = im.fetchall()

    with open('veri yükleme/read.txt', 'w', encoding="utf-8") as read_file:
        # Dosyayı sıfırladık, şimdiden sadece güncel veriler yazılacak
        for row in rows:
            # `read.txt` dosyasına id ve motor gücünü yazalım
            read_file.write(f"{row[0]}/{row[1]}\n")

def motor():
    with open('veri yükleme/motor.txt', encoding="utf-8") as f:
        for item in f.readlines():
            a = item.strip().split("+")
            try:
                im.execute("INSERT INTO warehouses_engine (engine_type, engine_power_id, engine_mark_id, serialnumber, location) VALUES (?,?,?,?,?)", (a[0],a[2],a[1],a[3],3))
                print(f"Motor gücü eklendi: {a}")
            except sqlite3.IntegrityError:
                # Güç zaten varsa, hata vermez sadece geçer
                print(f"Motor gücü zaten mevcut: {a}")

    db.commit()

    # Veritabanındaki tüm güçleri alalım
    im.execute("SELECT * FROM warehouses_engine")
    rows = im.fetchall()

    with open('veri yükleme/read.txt', 'w', encoding="utf-8") as read_file:
        # Dosyayı sıfırladık, şimdiden sadece güncel veriler yazılacak
        for row in rows:
            # `read.txt` dosyasına id ve motor gücünü yazalım
            read_file.write(f"{row[0]}-{str(row[2])}\n")

def pompa():
    with open('veri yükleme/pompa.txt', encoding="utf-8") as f:
        for item in f.readlines():
            a = item.strip().split("+")
            try:
                im.execute("INSERT INTO warehouses_pump (pump_type, pump_breed, number_stages, pump_mark_id,comment) VALUES (?,?,?,?,?)", (a[0],a[2],a[1],a[3],""))
                print(f"Motor gücü eklendi: {a}")
            except sqlite3.IntegrityError:
                # Güç zaten varsa, hata vermez sadece geçer
                print(f"Motor gücü zaten mevcut: {a}")

    db.commit()

    # Veritabanındaki tüm güçleri alalım
    im.execute("SELECT * FROM warehouses_pump")
    rows = im.fetchall()

    with open('veri yükleme/read.txt', 'w', encoding="utf-8") as read_file:
        # Dosyayı sıfırladık, şimdiden sadece güncel veriler yazılacak
        for row in rows:
            # `read.txt` dosyasına id ve motor gücünü yazalım
            read_file.write(f"{row[0]}\n")

def kuyu():
    with open('veri yükleme/kuyu.txt', encoding="utf-8") as f:
        for item in f.readlines():
            a = item.strip().split("/+")
            try:
                im.execute("INSERT INTO warehouses_inventory (well_number, district, address, disassembly_depth, mounting_depth,tank_info, pipe_type, cable, engine_id, pump_id, flow,created_at,updated_at,comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9],a[10],datetime.now(),datetime.now(),""))
                print(f"kuyu eklendi: {a}")
            except sqlite3.IntegrityError:
                # Güç zaten varsa, hata vermez sadece geçer
                print(f"Motor gücü zaten mevcut: {a}")

    db.commit()

    # Veritabanındaki tüm güçleri alalım
    im.execute("SELECT * FROM warehouses_inventory")
    rows = im.fetchall()

    with open('veri yükleme/read.txt', 'w', encoding="utf-8") as read_file:
        # Dosyayı sıfırladık, şimdiden sadece güncel veriler yazılacak
        for row in rows:
            # `read.txt` dosyasına id ve motor gücünü yazalım
            read_file.write(f"{row[0]}\n")

def ikincieldepo():
    with open('veri yükleme/ikincieldepo.txt', encoding="utf-8") as f:
        for item in f.readlines():
            seconhand = item.strip().split("-")

            row_identifier = seconhand[0]
            engineid = seconhand[1] if seconhand[1] != "" else None
            pump_id  = seconhand[2] if seconhand[2] != "" else None

            # Önce row_identifier var mı diye bak
            im.execute(
                "SELECT engine_id, pump_id FROM warehouses_seconhand WHERE row_identifier = ?",
                (row_identifier,)
            )
            result = im.fetchone()

            if result:
                # Varsa güncelle
                im.execute(
                    """
                    UPDATE warehouses_seconhand
                    SET engine_id = ?, pump_id = ?
                    WHERE row_identifier = ?
                    """,
                    (engineid, pump_id, row_identifier)
                )
                print(f"Güncellendi: {row_identifier} -> {engineid}, {pump_id}")
            else:
                print(f"Kayıt bulunamadı, atlandı: {row_identifier}")
    
    db.commit()
    # Veritabanındaki tüm markaları alalım
    im.execute("SELECT *FROM warehouses_seconhand")
    rows = im.fetchall()

    with open('veri yükleme/read.txt', 'w', encoding="utf-8") as read_file:
        # Dosyayı sıfırladık, şimdiden sadece güncel veriler yazılacak
        for row in rows:
            # `read.txt` dosyasına id ve marka yazalım
            read_file.write(f"{row[0]},{row[1]}\n")

def hidrofor():
    with open('veri yükleme/hidrofor.txt', encoding="utf-8") as f:
        for item in f.readlines():
            a = item.strip().split("+")
            try:
                im.execute("INSERT INTO hydrophore_hydrophore (serial_number, engine_power_id, engine_brand, pump_type_id,location,district,neighborhood) VALUES (?,?,?,?,?,?,?)", (a[0],a[1],a[2],a[3],"4","siverek",a[4]))
                print(f"hidrofor eklendi: {a}")
            except sqlite3.IntegrityError:
                # Güç zaten varsa, hata vermez sadece geçer
                print(f"Hidrofor zaten mevcut: {a}")

    db.commit()

    # Veritabanındaki tüm güçleri alalım
    im.execute("SELECT * FROM hydrophore_hydrophore")
    rows = im.fetchall()

    with open('veri yükleme/read.txt', 'w', encoding="utf-8") as read_file:
        # Dosyayı sıfırladık, şimdiden sadece güncel veriler yazılacak
        for row in rows:
            # `read.txt` dosyasına id ve motor gücünü yazalım
            read_file.write(f"{row[0]}-{str(row[2])}\n")

hidrofor()

db.close()