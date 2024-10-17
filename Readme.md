# Sistem Informasi FastAPI (REST API)

Proyek ini adalah aplikasi web yang dibangun menggunakan FastAPI, yang menyediakan sistem informasi untuk mengelola pengguna dan item. Berikut adalah rincian penting yang perlu diketahui untuk memahami dan menjalankan proyek ini.

## Struktur Folder

```txt
Sistem-Informasi-FastAPI/
├── main.py
├── .env
├── requirements.txt
├── models/
│   ├── items_model.py
│   └── users_model.py
├── routers/
│   ├── item_router.py
│   ├── public_router.py
│   └── user_router.py
└── services/
    ├── auth.py
    ├── database.py
    └── migration.py
```

### Deskripsi File

- **`main.py`**: Titik masuk aplikasi yang menginisialisasi FastAPI dan menyertakan router.
- **`.env`**: File konfigurasi lingkungan yang berisi variabel seperti SECRET_KEY dan URL database.
- **`requirements.txt`**: Daftar dependensi yang diperlukan untuk menjalankan aplikasi.
- **`models/`**: Berisi model data untuk item dan pengguna, menggunakan SQLAlchemy dan Pydantic.
- **`routers/`**: Menyediakan endpoint API untuk mengelola item dan pengguna.
- **`services/`**: Berisi logika bisnis, autentikasi, koneksi database, dan migrasi skema database.

## Instalasi

1. **Clone Repository**

   ```bash
   git clone https://github.com/iannstronaut/Sistem-Informasi-FastAPI.git

   cd Sistem-Informasi-FastAPI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Konfigurasi .env**
   Ubah `.env.example` menjadi **`.env`** dan ganti isinya menjadi:

   ```txt
   ROOT_PASSWORD = root
   DATABASE = <nama database>
   USER = <user>
   PASSWORD = <password>

   URL_DATABASE = "mysql+pymysql://${USER}:${PASSWORD}@localhost:3306/${DATABASE}"

   SECRET_KEY = <random character>

   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```

4. **Menjalankan Aplikasi**
   ```bash
   uvicorn main:app --reload
   ```
   Aplikasi akan berjalan di `http://127.0.0.1:8000`.

## API Endpoint

- **Pengguna**
  - POST **`/register`**: Mendaftar pengguna baru.
  - POST **`/login`**: Masuk sebagai pengguna.
  - GET **`/api/user/`**: Mengambil informasi pengguna saat ini.
  - PUT **`/api/user/`**: Memperbarui informasi pengguna.
  - DELETE **`/api/user/`**: Menghapus akun pengguna.
- **Item**
  - GET **`/api/item/`**: Mengambil semua item milik pengguna saat ini.
  - GET **`/api/item/{item_id}`**: Mengambil detail item berdasarkan ID.
  - POST **`/api/item/`**: Membuat item baru.
  - PUT **`/api/item/{item_id}`**: Memperbarui item berdasarkan ID.
  - DELETE **`/api/item/{item_id}`**: Menghapus item berdasarkan ID.
