from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, field_validator
from typing import Union, Optional
import uvicorn
import shutil
import os
from tinydes import TinyDES

# Copy hình ảnh lý thuyết vào static folder nếu chưa có
def ensure_theory_image():
    source = "Lý thuyết/CautruccuaTinyDes.png"
    destination = "static/CautruccuaTinyDes.png"
    
    if os.path.exists(source) and not os.path.exists(destination):
        try:
            shutil.copy(source, destination)
            print(f"Đã copy hình ảnh lý thuyết từ {source} đến {destination}")
        except Exception as e:
            print(f"Không thể copy hình ảnh: {e}")

# Đảm bảo hình ảnh lý thuyết có sẵn
ensure_theory_image()

# Khởi tạo FastAPI app
app = FastAPI(
    title="TinyDES Web Application",
    description="Ứng dụng web cho thuật toán mã hóa TinyDES",
    version="1.0.0"
)

# Cấu hình templates và static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Khởi tạo TinyDES instance
tinydes = TinyDES()

# Pydantic models cho request/response
class EncryptRequest(BaseModel):
    plaintext: str
    key: str
    
    @field_validator('plaintext', 'key')
    @classmethod
    def validate_input(cls, v):
        if not v.strip():
            raise ValueError('Input không được để trống')
        return v.strip()

class DecryptRequest(BaseModel):
    ciphertext: str
    key: str
    
    @field_validator('ciphertext', 'key')
    @classmethod
    def validate_input(cls, v):
        if not v.strip():
            raise ValueError('Input không được để trống')
        return v.strip()

class TestFunctionRequest(BaseModel):
    input_data: str
    
    @field_validator('input_data')
    @classmethod
    def validate_input(cls, v):
        if not v.strip():
            raise ValueError('Input không được để trống')
        return v.strip()

class CompressKeyRequest(BaseModel):
    kl: str
    kr: str
    
    @field_validator('kl', 'kr')
    @classmethod
    def validate_input(cls, v):
        if not v.strip():
            raise ValueError('Input không được để trống')
        return v.strip()

class Response(BaseModel):
    success: bool
    message: str
    data: dict = None

# Utility function để convert input
def convert_input(user_input: str, expected_bits: int) -> Union[str, None]:
    """Chuyển đổi input từ người dùng thành binary string"""
    user_input = user_input.strip().lower()
    
    try:
        # Nếu là binary
        if all(c in '01' for c in user_input):
            if len(user_input) == expected_bits:
                return user_input
            elif len(user_input) < expected_bits:
                return user_input.zfill(expected_bits)
            else:
                return None
        
        # Nếu là hex
        elif user_input.startswith('0x'):
            hex_value = user_input[2:]
            if len(hex_value) <= 2 and all(c in '0123456789abcdef' for c in hex_value):
                decimal = int(hex_value, 16)
                return format(decimal, f'0{expected_bits}b')
        
        # Nếu là decimal
        elif user_input.isdigit():
            decimal = int(user_input)
            if 0 <= decimal < 2**expected_bits:
                return format(decimal, f'0{expected_bits}b')
        
        return None
        
    except ValueError:
        return None

# Web Routes

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Trang chủ với giao diện TinyDES"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/encrypt", response_class=HTMLResponse)
async def encrypt_form(request: Request, plaintext: str = Form(...), key: str = Form(...)):
    """Xử lý form mã hóa"""
    try:
        # Convert inputs
        plaintext_bin = convert_input(plaintext, 8)
        key_bin = convert_input(key, 8)
        
        if plaintext_bin is None:
            error = "Định dạng plaintext không hợp lệ"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error,
                "plaintext": plaintext,
                "key": key
            })
        
        if key_bin is None:
            error = "Định dạng key không hợp lệ"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error,
                "plaintext": plaintext,
                "key": key
            })
        
        # Encrypt
        ciphertext = tinydes.encrypt(plaintext_bin, key_bin)
        
        result = {
            "type": "encrypt",
            "plaintext": plaintext_bin,
            "key": key_bin,
            "ciphertext": ciphertext,
            "ciphertext_hex": hex(int(ciphertext, 2)),
            "ciphertext_decimal": int(ciphertext, 2)
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": result,
            "plaintext": plaintext,
            "key": key
        })
        
    except Exception as e:
        error = f"Lỗi mã hóa: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": error,
            "plaintext": plaintext,
            "key": key
        })

@app.post("/decrypt", response_class=HTMLResponse)
async def decrypt_form(request: Request, ciphertext: str = Form(...), key: str = Form(...)):
    """Xử lý form giải mã"""
    try:
        # Convert inputs
        ciphertext_bin = convert_input(ciphertext, 8)
        key_bin = convert_input(key, 8)
        
        if ciphertext_bin is None:
            error = "Định dạng ciphertext không hợp lệ"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error,
                "ciphertext": ciphertext,
                "key": key
            })
        
        if key_bin is None:
            error = "Định dạng key không hợp lệ"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error,
                "ciphertext": ciphertext,
                "key": key
            })
        
        # Decrypt
        plaintext = tinydes.decrypt(ciphertext_bin, key_bin)
        
        result = {
            "type": "decrypt",
            "ciphertext": ciphertext_bin,
            "key": key_bin,
            "plaintext": plaintext,
            "plaintext_hex": hex(int(plaintext, 2)),
            "plaintext_decimal": int(plaintext, 2)
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": result,
            "ciphertext": ciphertext,
            "key": key
        })
        
    except Exception as e:
        error = f"Lỗi giải mã: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": error,
            "ciphertext": ciphertext,
            "key": key
        })

# API Endpoints (Optional - có thể xóa nếu không cần)

@app.get("/api/info")
async def get_info():
    """Lấy thông tin về TinyDES"""
    return {
        "algorithm": "TinyDES",
        "description": "Phiên bản thu nhỏ của thuật toán DES",
        "specifications": {
            "block_size": "8 bit",
            "key_size": "8 bit",
            "rounds": 3,
            "subkey_size": "6 bit"
        },
        "components": {
            "expand": "4 bit → 6 bit",
            "sbox": "6 bit → 4 bit (4x16 matrix)",
            "pbox": "4 bit → 4 bit (permutation)",
            "key_schedule": "8 bit → 6 bit (compression)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "TinyDES Web App is running"}

# Test Functions Routes

@app.post("/test/expand", response_class=HTMLResponse)
async def test_expand(request: Request, input: str = Form(...)):
    """Test expand function"""
    try:
        # Validate input
        if not all(c in '01' for c in input) or len(input) != 4:
            error = "Input phải là chuỗi binary 4-bit"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error
            })
        
        # Test expand function
        result = tinydes.expand(input)
        
        test_result = {
            "function": "expand",
            "input": input,
            "output": result
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "test_result": test_result
        })
        
    except Exception as e:
        error = f"Lỗi test expand: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": error
        })

@app.post("/test/sbox", response_class=HTMLResponse)
async def test_sbox(request: Request, input: str = Form(...)):
    """Test S-box lookup function"""
    try:
        # Validate input
        if not all(c in '01' for c in input) or len(input) != 6:
            error = "Input phải là chuỗi binary 6-bit"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error
            })
        
        # Test S-box function
        result = tinydes.sbox_lookup(input)
        
        # Calculate row and column for display
        b0, b1, b2, b3, b4, b5 = input[0], input[1], input[2], input[3], input[4], input[5]
        row = int(b0 + b5, 2)
        col = int(b1 + b2 + b3 + b4, 2)
        
        test_result = {
            "function": "sbox",
            "input": input,
            "output": result,
            "row": row,
            "column": col
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "test_result": test_result
        })
        
    except Exception as e:
        error = f"Lỗi test S-box: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": error
        })

@app.post("/test/pbox", response_class=HTMLResponse)
async def test_pbox(request: Request, input: str = Form(...)):
    """Test P-box permutation function"""
    try:
        # Validate input
        if not all(c in '01' for c in input) or len(input) != 4:
            error = "Input phải là chuỗi binary 4-bit"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error
            })
        
        # Test P-box function
        result = tinydes.pbox_permute(input)
        
        test_result = {
            "function": "pbox",
            "input": input,
            "output": result
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "test_result": test_result
        })
        
    except Exception as e:
        error = f"Lỗi test P-box: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": error
        })

@app.post("/test/compress", response_class=HTMLResponse)
async def test_compress(request: Request, kl: str = Form(...), kr: str = Form(...)):
    """Test compress key function"""
    try:
        # Validate inputs
        if not all(c in '01' for c in kl) or len(kl) != 4:
            error = "KL0 phải là chuỗi binary 4-bit"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error
            })
        
        if not all(c in '01' for c in kr) or len(kr) != 4:
            error = "KR0 phải là chuỗi binary 4-bit"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error
            })
        
        # Test compress function
        result = tinydes.compress_key(kl, kr)
        
        test_result = {
            "function": "compress",
            "kl": kl,
            "kr": kr,
            "output": result
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "test_result": test_result
        })
        
    except Exception as e:
        error = f"Lỗi test compress: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": error
        })

@app.post("/test/encrypt", response_class=HTMLResponse)
async def test_encrypt(request: Request, plaintext: str = Form(...), key: str = Form(...)):
    """Test full encryption function"""
    try:
        # Validate inputs
        if not all(c in '01' for c in plaintext) or len(plaintext) != 8:
            error = "Plaintext phải là chuỗi binary 8-bit"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error
            })
        
        if not all(c in '01' for c in key) or len(key) != 8:
            error = "Key phải là chuỗi binary 8-bit"
            return templates.TemplateResponse("index.html", {
                "request": request, 
                "error": error
            })
        
        # Test encryption
        result = tinydes.encrypt(plaintext, key)
        
        # Get subkeys for display
        kl0 = key[:4]
        kr0 = key[4:]
        subkeys = []
        for i in range(3):
            subkey = tinydes.compress_key(kl0, kr0)
            subkeys.append(subkey)
            # Rotate for next round
            kl0, kr0 = kr0, kl0
        
        test_result = {
            "function": "encrypt",
            "plaintext": plaintext,
            "key": key,
            "output": result,
            "subkeys": " → ".join(subkeys)
        }
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "test_result": test_result
        })
        
    except Exception as e:
        error = f"Lỗi test encryption: {str(e)}"
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": error
        })

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
