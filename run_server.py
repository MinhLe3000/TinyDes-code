#!/usr/bin/env python3
"""
Script để chạy FastAPI server cho TinyDES
"""

import uvicorn
import sys
import os

def main():
    """Chạy FastAPI server"""
    print("🚀 Đang khởi động TinyDES API Server...")
    print("📡 Server sẽ chạy tại: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Health Check: http://localhost:8000/health")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="debug"
        )
    except KeyboardInterrupt:
        print("\n👋 Đã dừng server!")
    except Exception as e:
        print(f"❌ Lỗi khi khởi động server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
