import csv
from prettytable import PrettyTable
import pwinput
from datetime import datetime

studios = {

}
users = {}
booking = {
    1: [], 2: [], 3: [], 4: []
}
transactions = {

}

def load_studios():
    try:
        with open('studios.csv', mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 3:
                    studio_id, name, price = row
                    studios[studio_id] = {'name': name, 'price': int(price)}
    except FileNotFoundError:
        print("File 'studios.csv' tidak ditemukan, membuat file baru.")
        with open('studios_user.csv', mode='w', newline='') as file:
            pass  

def load_users():
    try:
        with open('username_user.csv', mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 4:
                    username, password, saldo, emoney, role = row
                    users[username] = {'password': password, 'saldo': int(saldo),'emoney':int(emoney), 'role': role}
    except FileNotFoundError:
        print("File 'username_user.csv' tidak ditemukan, membuat file baru.")
        with open('username_user.csv', mode='w', newline='') as file:
            pass  

def load_transactions():
    try:
        with open('invoice.csv', mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                studio_id = row['studio_id']
                if studio_id not in transactions:
                    transactions[studio_id] = []

                transactions[studio_id].append({
                    "username": row['username'],
                    "nama_studio": row['nama_studio'],
                    "durasi": float(row['durasi']),
                    "tanggal": row['tanggal'],
                    "jam_mulai": int(row['jam_mulai']),
                    "jam_selesai": int(row['jam_selesai']),
                    "harga_total": row['harga_total'],
                    "tanggal_transaksi": row['tanggal_transaksi']
                })

    except FileNotFoundError:
        print("File 'invoice.csv' tidak ditemukan.")
    return transactions

def save_studios(studios):
    try:
        with open('studios.csv', mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            for id, studio_data in studios.items():
                row = [id, studio_data['name'], studio_data['price']]
                csv_writer.writerow(row)
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data studio: {e}")


def save_transactions(transactions):
    try:
        with open('invoice.csv', mode='w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['studio_id', 'username', 'nama_studio', 'durasi', 'tanggal', 'jam_mulai', 'jam_selesai', 'harga_total','tanggal_transaksi'])
            csv_writer.writeheader()

            for studio_id, transaksis in transactions.items():
                for transaksi in transaksis:
                    row = {
                        'studio_id': studio_id,
                        'username': transaksi['username'],
                        'nama_studio': transaksi['nama_studio'],
                        'durasi': transaksi['durasi'],
                        'tanggal': transaksi['tanggal'],
                        'jam_mulai': transaksi['jam_mulai'],
                        'jam_selesai': transaksi['jam_selesai'],
                        'harga_total': transaksi['harga_total'],
                        'tanggal_transaksi': transaksi['tanggal_transaksi']
                    }
                    csv_writer.writerow(row)
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan transaksi: {e}")

def save_users(users):
    try:
        with open('username_user.csv', mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            for username, user_data in users.items():
                row = [
                    username,
                    user_data['password'],
                    user_data['saldo'],
                    user_data['emoney'],
                    user_data['role']
                ]
                csv_writer.writerow(row)

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data pengguna: {e}")

def main_menu():
    while True:
        print("\n================")
        print("\n===Menu Utama===")
        print("1. Registrasi")
        print("2. Login")
        print("3. Exit")
        print("\n================")
        choice = input("Pilih opsi: ")

        if choice == '1':
            register()
        elif choice == '2':
            username = login()
            if username:
                user_menu(username) 
        elif choice == '3':
            print("Terima kasih telah menggunakan aplikasi.")
            exit()
        else:
            print("Opsi tidak valid. Silahkan dicoba kembali!")

def register():
    username = input("Masukkan username: ")

    if username in users:
        print("Username sudah ada. Silakan pilih username lain.")
        return
    
    password = pwinput.pwinput("Masukkan password: ")
    saldo = 0
    emoney = 0
    role = 'user'
    users[username] = {'password': password, 'saldo': saldo, 'emoney' : emoney, 'role': 'user'}
    print("Akun berhasil dibuat!")

    with open('username_user.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([username, password, saldo, emoney, role])
    print(f"Data {username} berhasil ditambahkan.")

def login():
    load_users()
    x = 3  
    while x > 0:
        username = input("Masukkan username: ")
        password = pwinput.pwinput("Masukkan password: ")

        if username in users and users[username]['password'] == password and users[username]['role'] == 'admin':
            print("Login admin berhasil!")
            admin_menu()
            return
        elif username in users and users[username]['password'] == password and users[username]['role'] == 'user':
            print("Login berhasil!")
            return username
        else:
            x -= 1
            if x == 0:
                print("Anda telah mencoba login 3 kali. Program akan keluar.")
                exit()
            else:
                print(f"Username atau password salah. Sisa percobaan: {x}")
    
    return None

def user_menu(username):
    while True:
        print("\n=================")
        print("\n====Menu User====")
        print("1. Tampilkan Studio")
        print("2. Sewa Studio")
        print("3. Cek Saldo")
        print("4. Top up")
        print("5. Logout")
        print("\n=================")
        choice = input("Pilih opsi: ")
        
        if choice == '1':
            tampil_studios()
        elif choice == '2':
            sewa_studio(username)
        elif choice == '3':
            if users[username]["emoney"] == 0:
                print("Saldo E-Money Anda masih kosong.")
            else:
                print(f"Saldo E-Money Anda: {users[username].get('emoney', 0)}")
        elif choice == "4":
                print(f"Saldo anda saat ini: {users[username]['saldo']}")
                saldo = input("Apakah ingin top up saldo anda? \nTekan (iya/tidak): ")
                if saldo == 'iya':
                    try:
                        top_Up = int(input("Masukkan jumlah top up saldo anda: "))
                        if top_Up <= 0:
                            print("Jumlah top up tidak valid.")
                            continue
                        elif top_Up >  500000:
                            print("Top up saldo melebihi batas maksimal yaitu 500000")
                            continue
                    except ValueError:
                        print("Input harus berupa angka.")
                        continue
                    users[username]["saldo"] += top_Up
                    print(f"Saldo utama anda telah bertambah sebesar {top_Up}. Saldo saat ini: {users[username]['saldo']}")
                    save_users(users)
                elif saldo == 'tidak':
                    print("Top up saldo dibatalkan.")
                else:
                    print("Pilihan tidak valid.")
                    print("")

                money = input("Apakah ingin top up E-Money anda? \nTekan (iya/tidak): ").lower()
                if money == 'iya':
                    try:
                        top_up_emoney = int(input("Masukkan jumlah top up E-Money: "))
                        if top_up_emoney <= 0:
                            print("Jumlah top up E-Money tidak valid.")
                            continue
                    except ValueError:
                        print("Input harus berupa angka.")
                        continue

                    if top_up_emoney <= users[username]["saldo"]:
                        users[username]["saldo"] -= top_up_emoney
                        users[username]["emoney"] = users[username].get("emoney", 0) + top_up_emoney
                        print(f"E-Money berhasil ditambahkan. Saldo E-Money anda: {users[username]['emoney']}")
                        save_users(users)
                    else:
                        print("Saldo utama anda tidak mencukupi untuk top up E-Money.")
                elif money == 'tidak':
                    print("Top up E-Money dibatalkan.")
                else:
                    print("Pilihan tidak valid.")
        elif choice == '5':
            main_menu()
            print("Logout berhasil.")
            break
        else:
            print("Opsi tidak valid.")



def tampil_studios():
    table = PrettyTable(["ID", "Nama Studio", "Harga"])
    for studio_id, info in studios.items():
        table.add_row([studio_id, info['name'], info['price']])
    print(table)


def sewa_studio(username):
    tampil_studios()
    waktu_sekarang = datetime.now().strftime("%Y/%m/%d %H:%M")
    try:
        studio_id = input("Masukkan ID studio yang ingin disewa: ")
        
        if studio_id not in studios:
            print("Studio tidak ditemukan.")
            return

        if studio_id not in transactions:
            transactions[studio_id] = []

        tahun = int(input("masukan tahun: "))
        bulan = int(input("masukan bulan: "))
        if bulan < 1 or bulan > 12:
            print("Bulan tidak valid. Masukkan antara 1 hingga 12.")
            return
        hari = int(input("masukan hari tanggal: "))
        if hari < 1 or hari > 30:
            print("Hari tidak valid. Masukkan antara 1 hingga 30.")
            return
        
        jam_mulai = int(input("Masukkan jam mulai (misal: 18): "))
        jam_selesai = int(input("Masukkan jam selesai (misal: 20): "))

        tanggal = f"{tahun}-{bulan:02d}-{hari:02d}"
        tanggal_cek = datetime.strptime(f"{tanggal} {jam_mulai:02d}:00", "%Y-%m-%d %H:%M")
        if tanggal_cek < datetime.now():
            print("Tanggal tidak valid. Tidak boleh di masa lalu.")
            return

        if jam_mulai <= 0 or jam_selesai <= 0:
            print("Jam tidak boleh 0 atau kurang.")
            return

        if jam_mulai >= 24 or jam_selesai > 24:
            print("Jam hanya valid antara 0 hingga 24.")
            return

        if jam_mulai >= jam_selesai:
            print("Jam selesai harus lebih besar dari jam mulai.")
            return

    except ValueError:
        print("Input jam harus berupa angka bulat.")
        return

    try:
        with open('invoice.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['studio_id'] == str(studio_id) and row['tanggal'] == tanggal:
                    existing_jam_mulai = int(row['jam_mulai'])
                    existing_jam_selesai = int(row['jam_selesai'])
                    
                    if (jam_mulai < existing_jam_selesai and jam_selesai > existing_jam_mulai):
                        print(f"Studio {row['nama_studio']} sudah dipesan pada tanggal {tanggal} dari jam {existing_jam_mulai} sampai {existing_jam_selesai}. Silakan pilih waktu lain.")
                        return
    except FileNotFoundError:
        print("File 'invoice.csv' tidak ditemukan.")

    durasi = jam_selesai - jam_mulai
    total_price = studios[studio_id]['price'] * durasi

    if users[username]['emoney'] < total_price:
        print("Saldo E-Money tidak cukup.")
        return

    users[username]['emoney'] -= total_price

    transactions[studio_id].append({
        'studio': studio_id,
        'username': username,
        'nama_studio' : studios[studio_id]['name'],
        'durasi': durasi,
        'tanggal': tanggal,
        'jam_mulai': jam_mulai,
        'jam_selesai': jam_selesai,
        'harga_total': total_price,
        'tanggal_transaksi' : waktu_sekarang
    })

    print(f"Studio {studios[studio_id]['name']} berhasil dipesan oleh {username} pada tanggal {tanggal} dari jam {jam_mulai:.2f} sampai {jam_selesai:.2f}. Total harga: Rp{total_price:,.0f}.")
    save_transactions(transactions)
    save_users(users)
    print_invoice(studio_id, username, durasi, tanggal, jam_mulai, jam_selesai, total_price, waktu_sekarang)


def print_invoice(studio_id, username, hours, tanggal, jam_mulai, jam_selesai, total_price, tanggal_transaksi):
    table = PrettyTable()
    table.field_names = ["Deskripsi", "Detail"]

    table.add_row(["Tanggal Transaksi", tanggal_transaksi])
    table.add_row(["Studio ID", studio_id])
    table.add_row(["Nama Studio", studios[studio_id]['name']])
    table.add_row(["Penyewa ", username])
    table.add_row(["Durasi (jam)", hours])
    table.add_row(["Tanggal Penyewaan", tanggal])
    table.add_row(["Jam Mulai", f"{jam_mulai:.2f}"])
    table.add_row(["Jam Selesai", f"{jam_selesai:.2f}"])
    table.add_row(["Total Harga", f"Rp{total_price:,.0f}"])

    print("\n===== INVOICE =====")
    print(table)
    print("===================\n")


def admin_menu():
    while True:
        print("\n==============")
        print("\n==Menu Admin==")
        print("1. Studio")
        print("2. Booking")
        print("3. Isi Saldo")
        print("4. Daftar User")
        print("5. Manage User")
        print("6. Search (bonus)")
        print("7. Log Out")
        print("\n==============")
        choice = input("Pilih opsi: ")
        
        if choice == '1':
            admin_menu_studio()
        elif choice == '2':
            admin_menu_booking()
        elif choice == '3':
            isi_saldo_user()
        elif choice == '4':
            tampilkan_data_users()
        elif choice == '5':
            manage_user()
        elif choice == '6':
            arr = [22,34,54,62,67,71]
            print (arr)
            element = input("cari indeks: ")
            print(jump_search(arr,element))
        elif choice == '7':
            main_menu()
            print("Logout berhasil.")
            break
        else:
            print("Opsi tidak valid.")

def isi_saldo_user():
    tampilkan_data_users()
    username = input("Masukkan username pengguna: ")
    if username not in users:
        print("Username tidak ditemukan.")
        return
    opsi = input(f"apakah anda yakin ingin top up e-money untuk akun {username}? 1/any :")
    if opsi == '1':
        try:
            saldo_add = int(input("Masukkan jumlah saldo e-money yang ingin ditambahkan: "))
            if saldo_add > 0:
                users[username]['emoney'] += saldo_add
                print(f"Saldo e-money untuk {username} berhasil ditambahkan. Saldo e-money sekarang: {users[username]['emoney']}")
                save_users(users)
            else:
                print("Jumlah saldo harus positif.")
        except ValueError:
            print("Input tidak valid. Harap masukkan angka.")
    else:
        print("adidaw kacaw")
        return


def admin_menu_studio():
    while True:
        print("\n=====================")
        print("\n==Menu Admin Studio==")
        print("1. Tambah Studio")
        print("2. Tampilkan Studio")
        print("3. Ubah Studio")
        print("4. Hapus Studio")
        print("5. Kembali ke menu awal")
        print("\n=====================")
        choice = input("Pilih opsi: ")

        if choice == '1':
            tambah_studio()
        elif choice == '2':
            tampil_studios()
        elif choice == '3':
            ubah_studio()
        elif choice == '4':
            del_studio()
        elif choice == '5':
            admin_menu()
            break
        else:
            print("Opsi tidak valid.")

def tambah_studio():
    load_studios() 

    name = input("Masukkan nama studio: ")
    if any(studio['name'].lower() == name.lower() for studio in studios.values()):
        print("Nama studio sudah ada. Silakan pilih nama studio lain.")
        return

    try:
        price = int(input("Masukkan harga sewa per jam: "))
        if price <= 0:
            print("Harga sewa tidak valid. Harap masukkan harga yang lebih besar dari 0.")
            return
    except ValueError:
        print("Harga sewa harus berupa angka.")
        return

    studio_id = str(len(studios) + 1) 
    studios[studio_id] = {'name': name, 'price': price}
    print(f"Studio '{name}' berhasil ditambahkan dengan harga sewa Rp{price:,.0f} per jam.")
    
    save_studios(studios)


def ubah_studio():
    load_studios() 
    tampil_studios() 
    
    try:
        studio_id = input("Masukkan ID studio yang ingin diubah: ")
    except ValueError:
        print("ID studio harus berupa angka.")
        return
    
    if studio_id not in studios:
        print("ID studio tidak valid.")
        return

    studio = studios[studio_id]
    print(f"Studio yang dipilih: {studio['name']} (Harga: Rp{studio['price']:,.0f})")

    new_name = input("Masukkan nama studio baru: ")
    
    if any(studio['name'].lower() == new_name.lower() for studio in studios.values()):
        print("Nama studio sudah ada. Silakan pilih nama studio lain.")
        return
    
    try:
        new_price = int(input("Masukkan harga sewa per jam baru: "))
        if new_price <= 0:
            print("Harga sewa tidak valid. Harap masukkan harga yang lebih besar dari 0.")
            return
    except ValueError:
        print("Harga sewa harus berupa angka.")
        return

    studios[studio_id] = {'name': new_name, 'price': new_price}
    print(f"Studio berhasil diubah menjadi '{new_name}' dengan harga sewa Rp{new_price:,.0f} per jam.")
    save_studios(studios)


def del_studio():
    tampil_studios()
    try:
        studio_id = input("Masukkan ID studio yang ingin dihapus: ")
    except ValueError:
        print("ID studio harus berupa angka.")
        return
    
    if studio_id not in studios:
        print("ID studio tidak valid.")
        return

    if transactions.get(studio_id):
        print(f"Studio {studios[studio_id]['name']} memiliki transaksi yang belum dibatalkan!")
        return
    del studios[studio_id]
    print("Studio berhasil dihapus!")
    save_studios(studios)


#menu admin booking
def admin_menu_booking():
    while True:
        print("\n======================")
        print("\n==Menu Admin Booking==")
        print("1. Daftar Sewa")
        print("2. Tambah Sewa")
        print("3. Hapus Sewa")
        print("4. Kembali ke menu awal")
        print("\n=====================")
        choice = input("Pilih opsi: ")

        if choice == '1':
            daftar_sewa()
        elif choice == '2':
            tambah_sewa()
        elif choice == '3':
            hapus_sewa()
        elif choice == '4':
            admin_menu()
            break
        else:
            print("Opsi tidak valid.")

def daftar_sewa():
    if not any(transactions.values()):
        print("Tidak ada booking yang tersedia.")
        return
    
    table = PrettyTable()
    table.field_names = ["Studio ID", "Penyewa", "Nama Studio", "Durasi", "Tanggal", "Jam Mulai", "Jam Selesai", "Harga Total"]

    for studio_id, transaksis in transactions.items():
        for trans in transaksis:
            table.add_row([
                studio_id,
                trans["username"],
                trans["nama_studio"],
                trans["durasi"],
                trans["tanggal"],
                trans["jam_mulai"],
                trans["jam_selesai"],
                trans["harga_total"]
            ])

    print(table)


def tambah_sewa():
    tampil_studios()
    username = input("Masukkan Penyewa: ")
    waktu_sekarang = datetime.now().strftime("%Y/%m/%d %H:%M")
    try:
        studio_id = input("Masukkan ID studio yang ingin disewa: ")
        
        if studio_id not in studios:
            print("Studio tidak ditemukan.")
            return

        if studio_id not in transactions:
            transactions[studio_id] = []

        tahun = int(input("masukan tahun: "))
        bulan = int(input("masukan bulan: "))
        if bulan < 1 or bulan > 12:
            print("Bulan tidak valid. Masukkan antara 1 hingga 12.")
            return
        hari = int(input("masukan hari tanggal: "))
        if hari < 1 or hari > 30:
            print("Hari tidak valid. Masukkan antara 1 hingga 30.")
            return
        
        jam_mulai = int(input("Masukkan jam mulai (misal: 18): "))
        jam_selesai = int(input("Masukkan jam selesai (misal: 20): "))

        tanggal = f"{tahun}-{bulan:02d}-{hari:02d}"
        tanggal_cek = datetime.strptime(f"{tanggal} {jam_mulai:02d}:00", "%Y-%m-%d %H:%M")
        if tanggal_cek < datetime.now():
            print("Tanggal tidak valid. Tidak boleh di masa lalu.")
            return

        if jam_mulai <= 0 or jam_selesai <= 0:
            print("Jam tidak boleh 0 atau kurang.")
            return

        if jam_mulai >= 24 or jam_selesai > 24:
            print("Jam hanya valid antara 0 hingga 24.")
            return

        if jam_mulai >= jam_selesai:
            print("Jam selesai harus lebih besar dari jam mulai.")
            return

    except ValueError:
        print("Invalid Input.")
        return

    try:
        with open('invoice.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['studio_id'] == str(studio_id) and row['tanggal'] == tanggal:
                    existing_jam_mulai = int(row['jam_mulai'])
                    existing_jam_selesai = int(row['jam_selesai'])
                    
                    if (jam_mulai < existing_jam_selesai and jam_selesai > existing_jam_mulai):
                        print(f"Studio {row['nama_studio']} sudah dipesan pada tanggal {tanggal} dari jam {existing_jam_mulai} sampai {existing_jam_selesai}. Silakan pilih waktu lain.")
                        return
    except FileNotFoundError:
        print("File 'invoice.csv' tidak ditemukan.")


    durasi = jam_selesai - jam_mulai
    total_price = studios[studio_id]['price'] * durasi

    transactions[studio_id].append({
        'studio': studio_id,
        'username': username,
        'nama_studio' : studios[studio_id]['name'],
        'durasi': durasi,
        'tanggal': tanggal,
        'jam_mulai': jam_mulai,
        'jam_selesai': jam_selesai,
        'harga_total': total_price,
        'tanggal_transaksi' : waktu_sekarang
    })

    print(f"Studio {studios[studio_id]['name']} berhasil dipesan oleh {username} pada tanggal {tanggal} dari jam {jam_mulai:.2f} sampai {jam_selesai:.2f}. Total harga: Rp{total_price:,.0f}.")
    save_transactions(transactions)
    print_invoice(studio_id, username, durasi, tanggal, jam_mulai, jam_selesai, total_price, waktu_sekarang)

def hapus_sewa():
    daftar_sewa()
    username = input("Masukkan username yang ingin dihapus sewanya: ")
    transaksi_ditemukan = False

    transaksi_terpilih = []

    for studio_id, transaksis in transactions.items():
        for transaksi in transaksis:
            if transaksi['username'] == username:
                transaksi_terpilih.append((studio_id, transaksi))
                transaksi_ditemukan = True

    if transaksi_ditemukan:
        for studio_id, transaksi in transaksi_terpilih:
            print("\nTransaksi ditemukan:")
            print(f"Studio: {transaksi['nama_studio']}")
            print(f"Tanggal: {transaksi['tanggal']}")
            print(f"Jam Mulai: {transaksi['jam_mulai']}")
            print(f"Jam Selesai: {transaksi['jam_selesai']}")
            print(f"Harga Total: {transaksi['harga_total']}")

            konfirmasi = input("Apakah Anda ingin menghapus transaksi ini? (y/n): ")
            if konfirmasi.lower() == 'y':
                transactions[studio_id].remove(transaksi)
                print(f"Transaksi untuk studio {transaksi['nama_studio']} berhasil dihapus.")
                save_transactions(transactions)
                return
            else:
                print("Transaksi tidak dihapus.")
    else:
        print(f"Tidak ditemukan transaksi dengan username {username}.")



def tampilkan_data_users():
    table = PrettyTable(["Username", "Saldo", "emoney", "Role"])
    
    for username, info in users.items():
        table.add_row([username, info['saldo'],info['emoney'], info['role']])
    
    print(table)

def manage_user():
    tampilkan_data_users()
    username = input("masukan username yang ingin di angkat menjadi admin: ")
    if username not in users:
        print("Username tidak ditemukan.")
        return
    if users[username]['role'] == 'admin':
        print(f"{username} sudah merupakan admin")
    else:
        users[username]['role'] = 'admin'
        print(f"Berhasil mengubah status {username} ke admin.")
        save_users(users)

def jump_search(arr, element):
    jump_size = round(len(arr)(1/2))
    current = 0

    element = int(element)

    while arr[current] < element:
        if current + jump_size > len(arr) - 1:
            current = len(arr) - 1
        else:
            current += jump_size

    for i in range(current, current - jump_size, -1):
        if element == arr[i]:
            return f"element ditemukan pada index {i}"
    return "element tidak ditemukan"

if __name__ == "__main__":
    load_studios()
    transactions = load_transactions()
    load_users()
    main_menu()