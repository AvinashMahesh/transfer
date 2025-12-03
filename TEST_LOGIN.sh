#!/bin/bash
# Test login API with email and password

echo "========================================"
echo "Testing Login API"
echo "========================================"
echo ""

# Test login endpoint
echo "1. Testing login with analyst account..."
response=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@deloitte.com",
    "password": "password123"
  }')

# Check if we got a token
if echo "$response" | grep -q "access_token"; then
    echo "✅ LOGIN SUCCESSFUL!"
    echo ""
    
    # Extract token (basic extraction)
    token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    user=$(echo "$response" | grep -o '"full_name":"[^"]*"' | cut -d'"' -f4)
    role=$(echo "$response" | grep -o '"role":"[^"]*"' | cut -d'"' -f4)
    
    echo "Logged in as: $user"
    echo "Role: $role"
    echo "Token: ${token:0:50}..."
    echo ""
    
    echo "2. Testing authenticated endpoint..."
    profile=$(curl -s "http://localhost:8000/api/v1/users/me" \
      -H "Authorization: Bearer $token")
    
    if echo "$profile" | grep -q "email"; then
        echo "✅ AUTHENTICATED REQUEST SUCCESSFUL!"
        echo ""
        echo "Your profile was retrieved successfully!"
    else
        echo "❌ Authenticated request failed"
    fi
else
    echo "❌ LOGIN FAILED"
    echo ""
    echo "Response:"
    echo "$response"
    echo ""
    echo "Make sure the server is running:"
    echo "  docker-compose up -d"
fi

echo ""
echo "========================================"
echo "Test complete!"
echo "========================================"
