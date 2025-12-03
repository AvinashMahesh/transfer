"""
Test authentication with email and password
"""
import sys
sys.path.insert(0, '/workspace')

from app.core.security import get_password_hash, verify_password

# Test password hashing and verification
print("=" * 60)
print("Testing Password Authentication")
print("=" * 60)

password = "password123"
print(f"\n1. Original password: {password}")

# Hash the password
hashed = get_password_hash(password)
print(f"2. Hashed password: {hashed[:50]}...")

# Verify correct password
is_valid = verify_password(password, hashed)
print(f"3. Verify correct password: {is_valid}")

# Verify incorrect password
is_invalid = verify_password("wrongpassword", hashed)
print(f"4. Verify incorrect password: {is_invalid}")

if is_valid and not is_invalid:
    print("\n✅ Password hashing and verification working correctly!")
else:
    print("\n❌ Password verification has issues!")
    sys.exit(1)

print("\n" + "=" * 60)
print("Testing Database Connection and User Creation")
print("=" * 60)

try:
    from app.core.database import SessionLocal
    from app.models.user import User, UserRole
    
    db = SessionLocal()
    
    # Test query
    user_count = db.query(User).count()
    print(f"\n✅ Database connection successful!")
    print(f"   Current users in database: {user_count}")
    
    if user_count > 0:
        # Show first user
        first_user = db.query(User).first()
        print(f"\n   Sample user:")
        print(f"   - Email: {first_user.email}")
        print(f"   - Name: {first_user.full_name}")
        print(f"   - Role: {first_user.role.value}")
        print(f"   - Has password hash: {bool(first_user.password_hash)}")
        
        # Test password verification for sample user
        if first_user.password_hash:
            test_valid = verify_password("password123", first_user.password_hash)
            print(f"   - Password 'password123' valid: {test_valid}")
    
    db.close()
    
except Exception as e:
    print(f"\n❌ Database error: {e}")
    print("\n💡 Tip: Make sure PostgreSQL is running and DATABASE_URL is configured")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All authentication tests passed!")
print("=" * 60)
print("\n📧 Test Credentials:")
print("   Email: analyst@deloitte.com")
print("   Password: password123")
print("\n   Email: leader@deloitte.com")
print("   Password: password123")
print("\n   Email: admin@deloitte.com")
print("   Password: password123")
print("=" * 60)
