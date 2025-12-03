# ✅ SQLite In-Memory Database Setup

## What Changed

The backend now uses **SQLite** instead of PostgreSQL for easy local development. No external database needed!

---

## 🎯 Benefits

- ✅ **No PostgreSQL required** - Works out of the box
- ✅ **No Docker needed** - Run directly with Python
- ✅ **Zero configuration** - Just install and run
- ✅ **Fast setup** - Ready in 30 seconds
- ✅ **Auto-creates database** - No manual setup
- ✅ **Sample data included** - Pre-loaded test accounts

---

## 🚀 Quick Start (No Docker!)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Server

```bash
python run.py
```

That's it! The server will:
- Create the SQLite database automatically
- Set up all tables
- Load sample data (3 users + 4 initiatives)
- Start on http://localhost:8000

### Step 3: Test the API

Open your browser:
```
http://localhost:8000/docs
```

Login with:
```json
{
  "email": "analyst@deloitte.com",
  "password": "password123"
}
```

---

## 📊 Database Details

### Database File Location

The SQLite database is stored at:
```
./deloitte_initiatives.db
```

### View Database Contents

You can use any SQLite browser:

```bash
# Using sqlite3 command line
sqlite3 deloitte_initiatives.db

# List tables
.tables

# Query users
SELECT email, full_name, role FROM users;

# Query initiatives
SELECT id, title, practice_area, status FROM initiatives;
```

Or use a GUI tool:
- DB Browser for SQLite: https://sqlitebrowser.org/
- TablePlus: https://tableplus.com/
- DBeaver: https://dbeaver.io/

---

## 🔄 Reset Database

To start fresh:

```bash
# Delete database file
rm deloitte_initiatives.db

# Run server again (will recreate)
python run.py
```

---

## 💾 Data Persistence

### File-Based (Default)
Data persists between restarts:
```python
DATABASE_URL=sqlite:///./deloitte_initiatives.db
```

### In-Memory Only
Data lost on restart (for testing):
```python
DATABASE_URL=sqlite:///:memory:
```

To use in-memory, edit `.env` or `app/core/config.py`.

---

## 🔧 Configuration

### .env File

```env
# SQLite database (file-based)
DATABASE_URL=sqlite:///./deloitte_initiatives.db

# OR in-memory only
# DATABASE_URL=sqlite:///:memory:

# Other settings
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Docker Option (Simplified)

If you prefer Docker but without PostgreSQL:

```bash
# Use simplified docker-compose
docker-compose -f docker-compose-simple.yml up -d
```

This version:
- ✅ Uses SQLite (no PostgreSQL)
- ✅ Only 2 containers (API + Qdrant)
- ✅ Faster startup
- ✅ Less memory usage

---

## 🎯 What Works

Everything works exactly the same as before:

- ✅ Email + password authentication
- ✅ All 25 API endpoints
- ✅ User profiles with skills & interests
- ✅ Initiative management
- ✅ Search & filtering
- ✅ AI recommendations
- ✅ Save/apply to initiatives
- ✅ Swagger documentation

---

## 📝 Test Credentials

Same as before:

| Email | Password | Role |
|-------|----------|------|
| analyst@deloitte.com | password123 | Analyst |
| leader@deloitte.com | password123 | Leader |
| admin@deloitte.com | password123 | Admin |

---

## 🔍 Database Schema

SQLite stores arrays as JSON strings:

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
    bio TEXT,
    practice TEXT,
    skills TEXT,           -- JSON: ["Python", "Data Analysis"]
    interests TEXT,        -- JSON: ["AI", "Healthcare"]
    industries TEXT,       -- JSON: ["Healthcare"]
    certifications TEXT,   -- JSON: ["PMP"]
    ...
);
```

### Initiatives Table
```sql
CREATE TABLE initiatives (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    practice_area TEXT,
    skills_needed TEXT,    -- JSON: ["Python", "ML"]
    industries TEXT,       -- JSON: ["Healthcare"]
    tags TEXT,            -- JSON: ["AI", "Research"]
    status TEXT NOT NULL,
    owner_id INTEGER,
    ...
);
```

Arrays are automatically converted between JSON and Python lists.

---

## 🚨 Troubleshooting

### Issue: "unable to open database file"

**Solution:**
```bash
# Ensure write permissions in current directory
chmod 755 .

# Or specify a writable path in .env
DATABASE_URL=sqlite:////tmp/deloitte_initiatives.db
```

### Issue: "Database is locked"

**Cause:** Multiple processes trying to write

**Solution:**
```bash
# Close other connections
# Restart the server
python run.py
```

### Issue: "No module named 'psycopg2'"

**Cause:** Old PostgreSQL requirement still cached

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📈 Performance

SQLite is perfectly fine for development and small deployments:

- ✅ Handles 100,000+ records easily
- ✅ Fast queries for typical use cases
- ✅ No network overhead (local file)
- ✅ ACID compliant
- ✅ Full SQL support

For production with high concurrency, consider PostgreSQL.

---

## 🔄 Migrating to PostgreSQL

When ready for production:

1. Update `.env`:
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/db
   ```

2. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

3. Run migrations:
   ```bash
   python run.py
   ```

The code automatically handles both SQLite and PostgreSQL!

---

## ✅ Summary

**Before (PostgreSQL):**
- ❌ Required Docker
- ❌ Required PostgreSQL installation
- ❌ Complex setup
- ❌ Slow startup

**Now (SQLite):**
- ✅ No Docker required
- ✅ No PostgreSQL needed
- ✅ One command to run
- ✅ Instant startup
- ✅ Same functionality

---

## 🎉 You're Ready!

Run the backend now:

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
python run.py

# Open Swagger UI
open http://localhost:8000/docs

# Login with: analyst@deloitte.com / password123
```

---

**No more Docker errors! No more database setup!** 🎊

Just install dependencies and run. That's it.

For questions, see the main documentation files.
