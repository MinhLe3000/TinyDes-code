# Hướng dẫn chạy HỆ THỐNG MÃ HÓA TINYDES

## Yêu cầu hệ thống

- Python 3.7 trở lên
- pip (Python package manager)

## Cách chạy dự án

### Bước 1: Cài đặt dependencies

Mở terminal/command prompt và chạy lệnh:

```bash
pip install -r requirements.txt
```

Hoặc trên Windows PowerShell:
```powershell
pip install -r requirements.txt
```

### Bước 2: Chạy server

Có 2 cách để chạy server:

#### Cách 1: Sử dụng file `run_server.py` (Khuyến nghị)

```bash
python run_server.py
```

Hoặc trên Windows:
```powershell
python run_server.py
```

#### Cách 2: Sử dụng uvicorn trực tiếp

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Hoặc với reload (tự động reload khi code thay đổi):
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Bước 3: Truy cập ứng dụng

Sau khi server khởi động thành công, mở trình duyệt và truy cập:

- **🌐 Giao diện web**: http://localhost:8000
- **📚 API Documentation (Swagger)**: http://localhost:8000/docs
- **🔧 Health Check**: http://localhost:8000/health
- **📊 API Info**: http://localhost:8000/api/info

## Cấu trúc lệnh chi tiết

### Trên Windows (PowerShell)

1. **Mở PowerShell** trong thư mục dự án

2. **Cài đặt dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Chạy server**:
   ```powershell
   python run_server.py
   ```

### Trên Linux/Mac (Terminal)

1. **Mở Terminal** trong thư mục dự án

2. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy server**:
   ```bash
   python run_server.py
   ```

## Kiểm tra server đã chạy

Khi server khởi động thành công, bạn sẽ thấy thông báo:

```
============================================================
🚀 Đang khởi động HỆ THỐNG MÃ HÓA TINYDES
📚 Đại học Kinh tế Quốc dân (NEU) - Khoa CNTT
============================================================
📡 Server sẽ chạy tại: http://0.0.0.0:8000
🌐 Giao diện web: http://localhost:8000
📚 API Documentation: http://0.0.0.0:8000/docs
🔧 Health Check: http://0.0.0.0:8000/health
📊 API Info: http://0.0.0.0:8000/api/info
============================================================
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Dừng server

Để dừng server, nhấn `Ctrl + C` trong terminal.

## Xử lý lỗi thường gặp

### Lỗi: ModuleNotFoundError

Nếu gặp lỗi `ModuleNotFoundError`, hãy đảm bảo đã cài đặt đầy đủ dependencies:

```bash
pip install -r requirements.txt
```

### Lỗi: Port đã được sử dụng

Nếu port 8000 đã được sử dụng, bạn có thể:

1. **Thay đổi port trong `run_server.py`**
2. **Hoặc dừng ứng dụng đang sử dụng port 8000**
3. **Hoặc chạy với port khác**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

### Lỗi: Permission denied

Trên Linux/Mac, nếu gặp lỗi permission, thử:

```bash
sudo python run_server.py
```

## Chạy trên môi trường production

Để chạy trên môi trường production (như Render), server sẽ tự động sử dụng biến môi trường `PORT` nếu có.

## Truy cập trực tuyến

Nếu không muốn chạy local, bạn có thể truy cập phiên bản đã deploy tại:

**https://tinydes.onrender.com/**


