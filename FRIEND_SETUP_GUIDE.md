# 🚀 NewsAggregator Setup Guide for Friends

## 📥 **Step 1: Download & Extract**
1. Download the NewsAggregator project folder
2. Extract it to your desired location (e.g., `C:\Users\YourName\Documents\NewsAggregator`)

## 🐍 **Step 2: Install Python Dependencies**
Open Command Prompt or PowerShell in the project folder and run:
```bash
pip install -r requirements.txt
```

## 🔧 **Step 3: IMPORTANT - Database Configuration**

**⚠️ CRITICAL:** Make sure the `.env` file contains:
```
USE_CLOUD_DB=True
```

If `USE_CLOUD_DB=False`, you'll see different news because you'll be using a local database!

### **Verify your .env file looks like this:**
```
# Supabase Database Configuration
DB_HOST=db.hiakbkfvjsygpkxrommx.supabase.co
DB_USER=postgres
DB_PASSWORD=Krishjam@2496
DB_PORT=5432
DB_NAME=postgres

# Complete database URL for easier connection (using session pooler)
DATABASE_URL=postgresql://postgres.hiakbkfvjsygpkxrommx:Krishjam@2496@aws-1-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require

# Enable cloud database connection
USE_CLOUD_DB=True
```

## ✅ **Step 4: Test Database Connection**
Run this command to verify you're connected to the shared database:
```bash
python check_database.py
```

**You should see:**
- ✅ Using CLOUD database (Supabase)
- 📊 Database Version: PostgreSQL 17.4...
- Same article count as the original

**If you see:**
- ⚠️ Using LOCAL SQLite database
- **FIX:** Check your `.env` file and ensure `USE_CLOUD_DB=True`

## 🌐 **Step 5: Start the Application**
```bash
python manage.py runserver 8000
```

Visit: **http://127.0.0.1:8000**

## 🔄 **Step 6: Sync News (Both see same articles)**
1. Go to `/scrape/` page
2. Click "Scrape News" 
3. **Both you and your friend will now see the same articles!**

---

## 🔍 **Troubleshooting**

### **Problem: Friend sees different news**
**Cause:** Using local SQLite database instead of shared Supabase
**Solution:** 
1. Check `.env` file has `USE_CLOUD_DB=True`
2. Run `python check_database.py` to verify
3. Restart the server

### **Problem: Can't connect to database**
**Cause:** Network or credential issues
**Solution:**
1. Check internet connection
2. Verify all credentials in `.env` are correct
3. Try running `python check_database.py`

### **Problem: No articles showing**
**Cause:** Database might be empty or connection issue
**Solution:**
1. Run `python check_database.py` to see article count
2. Use the scraping feature to add articles
3. Both users will see the same articles

---

## 🎯 **Expected Result**
✅ **Both computers show EXACTLY the same news articles**  
✅ **When one person scrapes news, both see it**  
✅ **Shared database with real-time updates**

---

## 📞 **Need Help?**
If you see "Using LOCAL SQLite database" in the checker, you're not connected to the shared database!

**Quick Fix:**
1. Open `.env` file
2. Change `USE_CLOUD_DB=False` to `USE_CLOUD_DB=True`
3. Restart the server
4. Run `python check_database.py` again
