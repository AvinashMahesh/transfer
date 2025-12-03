"""
Development server runner
"""
import uvicorn
from app.core.init_db import init_db, seed_sample_data

if __name__ == "__main__":
    print("=" * 60)
    print("Deloitte Initiative Discovery Platform - Backend")
    print("=" * 60)
    
    # Initialize database
    print("\n[1/2] Initializing database...")
    try:
        init_db()
        seed_sample_data()
    except Exception as e:
        print(f"Warning: Database initialization issue: {e}")
    
    # Start server
    print("\n[2/2] Starting FastAPI server...")
    print("\n" + "=" * 60)
    print("Server starting at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative docs: http://localhost:8000/redoc")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
