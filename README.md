# 🚀 NewsAggregator - Shared Cloud Database

A Django-based news aggregation web app with **shared cloud database** using Supabase.

## ⚡ Quick Start for Friends

### **Step 1:** Install dependencies
```bash
pip install -r requirements.txt
```

### **Step 2:** Verify setup (IMPORTANT!)
```bash
python verify_setup.py
```

### **Step 3:** Start the app
```bash
python manage.py runserver 8000
```

### **Step 4:** Visit http://127.0.0.1:8000

---

## 🔧 **IMPORTANT:** 
Make sure `.env` file has `USE_CLOUD_DB=True` or you won't see the shared news!

## 📖 **Need Help?**
See `FRIEND_SETUP_GUIDE.md` for detailed setup instructions.

---

## ✅ **Expected Result:**
- ✅ Both computers show the SAME news articles
- ✅ When one person scrapes news, both see it  
- ✅ Shared database with real-time updates
