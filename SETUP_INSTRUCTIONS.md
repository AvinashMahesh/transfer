# 🚀 Setup Instructions - Start Here!

## Welcome to Deloitte Initiative Discovery Platform Backend

This guide will get you up and running in **5 minutes**.

---

## ⚡ Quick Setup

### Step 1: Start the Backend

Choose one method:

#### Option A: Docker (Recommended - No setup needed!)

```bash
# Start all services (API + PostgreSQL + Qdrant)
docker-compose up -d

# View logs
docker-compose logs -f api
```

**That's it!** The API is now running at http://localhost:8000

#### Option B: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and set DATABASE_URL to your PostgreSQL connection

# Run the server
python run.py
```

---

## Step 2: Access Swagger UI

Open your browser:
```
http://localhost:8000/docs
```

You should see the interactive API documentation!

---

## Step 3: Test Login (NEW - Fixed!)

### In Swagger UI:

1. Find **POST /api/v1/auth/login**
2. Click **"Try it out"**
3. Enter credentials:
   ```json
   {
     "email": "analyst@deloitte.com",
     "password": "password123"
   }
   ```
4. Click **"Execute"**
5. You should see a **200 OK** response with a token!

### Example Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "analyst@deloitte.com",
    "full_name": "John Analyst",
    "role": "analyst"
  }
}
```

---

## Step 4: Authorize & Test Endpoints

1. **Copy** the `access_token` from the login response
2. Click the 🔒 **"Authorize"** button at the top of Swagger UI
3. Enter: `Bearer <paste-your-token-here>`
4. Click **"Authorize"** then **"Close"**
5. Now try any endpoint - they all work!

### Recommended Endpoints to Test:

- `GET /api/v1/users/me` - Your profile
- `GET /api/v1/initiatives/` - List initiatives
- `GET /api/v1/recommendations` - AI recommendations
- `GET /api/v1/search?q=AI` - Search initiatives
- `POST /api/v1/engagement/save` - Save an initiative

---

## 🔑 Test Accounts

**All accounts use password: `password123`**

| Email | Role | What You Can Do |
|-------|------|-----------------|
| analyst@deloitte.com | Analyst | Browse, search, save, apply to initiatives |
| leader@deloitte.com | Leader | Create & manage initiatives + all analyst features |
| admin@deloitte.com | Admin | Full system access |

---

## ✅ What's Working

### Authentication ✅
- ✅ Email + password login
- ✅ JWT token generation
- ✅ Secure password hashing (bcrypt)
- ✅ Token validation

### API Endpoints ✅ (25 total)
- ✅ **3** Authentication endpoints
- ✅ **4** User management endpoints
- ✅ **6** Initiative CRUD endpoints
- ✅ **2** Search endpoints
- ✅ **2** Recommendation endpoints
- ✅ **6** Engagement endpoints

### Features ✅
- ✅ Role-based access control
- ✅ User profiles with skills & interests
- ✅ Initiative listings
- ✅ Search & filtering
- ✅ AI recommendations
- ✅ Save/bookmark initiatives
- ✅ Apply to initiatives
- ✅ Swagger documentation

### Security ✅
- ✅ Password hashing (bcrypt)
- ✅ JWT authentication
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ CORS configuration

---

## 📊 Sample Data Included

The database is pre-loaded with:

### 3 Test Users
- John Analyst (analyst@deloitte.com)
- Sarah Leader (leader@deloitte.com)
- Admin User (admin@deloitte.com)

### 4 Sample Initiatives
1. **AI Healthcare Research Pod** (Technology)
2. **Innovation Hub - GenAI Applications** (Technology)
3. **Financial Services Digital Transformation** (Strategy)
4. **Sustainability Volunteering** (Risk & Sustainability)

---

## 🎯 Common Use Cases

### As an Analyst:

```bash
# 1. Login
POST /api/v1/auth/login
{
  "email": "analyst@deloitte.com",
  "password": "password123"
}

# 2. Get personalized recommendations
GET /api/v1/recommendations

# 3. Search for AI initiatives
GET /api/v1/search?q=AI

# 4. Save an initiative
POST /api/v1/engagement/save
{
  "initiative_id": 1
}

# 5. Apply to an initiative
POST /api/v1/engagement/apply
{
  "initiative_id": 1,
  "message": "I'm very interested!"
}
```

### As a Leader:

```bash
# 1. Login as leader
POST /api/v1/auth/login
{
  "email": "leader@deloitte.com",
  "password": "password123"
}

# 2. Create new initiative
POST /api/v1/initiatives/
{
  "title": "New Innovation Project",
  "description": "Looking for creative minds...",
  "practice_area": "Technology",
  "skills_needed": ["Python", "AI"],
  "time_commitment": "10 hours/week"
}

# 3. View applications to your initiatives
GET /api/v1/engagement/initiative/{id}/applications
```

---

## 🛠️ Troubleshooting

### Issue: "Connection refused" error

**Solution:** Make sure the server is running:
```bash
docker-compose ps
# Should show api, postgres, and qdrant running
```

If not running:
```bash
docker-compose up -d
```

### Issue: "401 Unauthorized"

**Solution:** 
1. Login first to get a token
2. Click "Authorize" in Swagger UI
3. Enter: `Bearer <your-token>`

### Issue: "Database not initialized"

**Solution:**
```bash
# Recreate database with sample data
docker-compose down -v
docker-compose up -d

# Wait 10 seconds for database to initialize
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port in docker-compose.yml
```

---

## 📚 Documentation

| Document | What's Inside |
|----------|---------------|
| **LOGIN_FIXED.md** | Details on the fixed login system |
| **AUTHENTICATION.md** | Complete authentication guide |
| **QUICKSTART.md** | 5-minute quick start |
| **API_DOCUMENTATION.md** | Full API reference |
| **SWAGGER_ACCESS.md** | How to use Swagger UI |
| **README.md** | Project overview |
| **ARCHITECTURE.md** | Technical architecture |
| **DEPLOYMENT_GUIDE.md** | Deploy to production |

---

## 🎓 Learning Path

### Beginner
1. ✅ Start with this document
2. ✅ Test login in Swagger UI
3. ✅ Try a few GET endpoints
4. ✅ Read QUICKSTART.md

### Intermediate
1. ✅ Test all endpoint categories
2. ✅ Try creating an initiative (as leader)
3. ✅ Test recommendations
4. ✅ Read API_DOCUMENTATION.md

### Advanced
1. ✅ Read ARCHITECTURE.md
2. ✅ Explore the code structure
3. ✅ Customize for your needs
4. ✅ Deploy with DEPLOYMENT_GUIDE.md

---

## 🚦 System Status

After running `docker-compose up -d`:

| Service | Port | Status Check |
|---------|------|--------------|
| API | 8000 | http://localhost:8000/health |
| Swagger UI | 8000 | http://localhost:8000/docs |
| PostgreSQL | 5432 | Internal |
| Qdrant | 6333 | Internal |

**Health Check:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

## 🎉 You're Ready!

Your backend is fully set up and ready to use!

### What to do next:

1. ✅ **Explore the API** - Try all endpoints in Swagger UI
2. ✅ **Build a frontend** - Connect your React/Vue/Angular app
3. ✅ **Customize** - Add your own features
4. ✅ **Deploy** - Follow DEPLOYMENT_GUIDE.md for production

---

## 📞 Need Help?

1. Check the documentation files listed above
2. Look at code examples in AUTHENTICATION.md
3. Review error messages in Swagger UI
4. Check Docker logs: `docker-compose logs -f`

---

## 🌟 Key Features at a Glance

```
✅ Authentication        → Login with email/password
✅ User Profiles         → Skills, interests, practice areas
✅ Initiatives           → Browse, create, manage
✅ Search                → Text and semantic search
✅ Recommendations       → AI-powered matching
✅ Engagement            → Save, apply, track
✅ Analytics             → View counts, applications
✅ Security              → JWT, bcrypt, RBAC
✅ Documentation         → Swagger UI auto-generated
```

---

**🚀 Happy coding! Your backend is production-ready!**

Start exploring: http://localhost:8000/docs