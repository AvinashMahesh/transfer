"""
Script to test the API and generate OpenAPI schema
"""
import sys
import json
from app.main import app

def test_swagger():
    """Test that Swagger/OpenAPI schema is generated correctly"""
    print("=" * 60)
    print("Testing Swagger/OpenAPI Documentation")
    print("=" * 60)
    
    # Get OpenAPI schema
    openapi_schema = app.openapi()
    
    print("\n✓ OpenAPI schema generated successfully!")
    print(f"\nAPI Title: {openapi_schema['info']['title']}")
    print(f"API Version: {openapi_schema['info']['version']}")
    print(f"API Description: {openapi_schema['info']['description'][:100]}...")
    
    # Count endpoints
    paths = openapi_schema['paths']
    endpoint_count = sum(len(methods) for methods in paths.values())
    
    print(f"\n📊 API Statistics:")
    print(f"  - Total Paths: {len(paths)}")
    print(f"  - Total Endpoints: {endpoint_count}")
    
    # List all endpoints
    print(f"\n📋 Available Endpoints:\n")
    
    for path, methods in sorted(paths.items()):
        for method, details in methods.items():
            summary = details.get('summary', 'No summary')
            tags = details.get('tags', ['Untagged'])
            print(f"  [{method.upper():6}] {path:50} - {summary} ({', '.join(tags)})")
    
    # List tags
    tags = openapi_schema.get('tags', [])
    print(f"\n🏷️  API Tags:")
    for tag in tags:
        print(f"  - {tag['name']}: {tag['description']}")
    
    # Save schema to file
    with open('openapi.json', 'w') as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"\n✓ OpenAPI schema saved to: openapi.json")
    
    # Verify key endpoints exist
    print(f"\n✅ Verification:")
    required_endpoints = [
        '/api/v1/auth/login',
        '/api/v1/users/me',
        '/api/v1/initiatives',
        '/api/v1/search',
        '/api/v1/recommendations',
        '/api/v1/engagement/save'
    ]
    
    missing = []
    for endpoint in required_endpoints:
        if endpoint in paths:
            print(f"  ✓ {endpoint}")
        else:
            print(f"  ✗ {endpoint} - MISSING")
            missing.append(endpoint)
    
    if missing:
        print(f"\n⚠️  Warning: {len(missing)} endpoints missing!")
        return False
    else:
        print(f"\n🎉 All required endpoints are present!")
        return True

if __name__ == "__main__":
    success = test_swagger()
    sys.exit(0 if success else 1)
