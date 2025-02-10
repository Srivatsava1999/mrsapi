## **🔥 Django Backend Deployment to Render**
### **✅ Step 1: Switch from SQLite to PostgreSQL**
#### **Changes in `settings.py`**
Modify the `DATABASES` setting to use **PostgreSQL** instead of SQLite:
```python
import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}
```
🔹 This dynamically sets up the database using the **DATABASE_URL** from `.env`.

---

### **✅ Step 2: Create a `.env` File (DO NOT COMMIT THIS)**
Create a `.env` file in the root directory and add:
```ini
DATABASE_URL=postgres://your-username:your-password@your-db-host.compute.amazonaws.com:5432/your-database-name
SECRET_KEY=your-secret-key
```
✅ **Do not include `DEBUG=False` yet to avoid breaking local debugging.**

---

### **✅ Step 3: Install Deployment Dependencies**
Ensure these are inside `requirements.txt`:
```
Django>=5.0
psycopg2-binary  # PostgreSQL adapter
dj-database-url  # Helps configure DB dynamically
gunicorn  # Production server
```
Then, install them:
```bash
pip install -r requirements.txt
```

---

### **✅ Step 4: Set Up Git Ignore**
Modify `.gitignore`:
```
.env
__pycache__/
db.sqlite3
```
✅ **You already have `mrsapi/` in `.gitignore`, so keep it.**

---

### **✅ Step 5: Apply Migrations for PostgreSQL**
Run:
```bash
python manage.py makemigrations
python manage.py migrate
```
✅ This ensures the PostgreSQL database is **properly initialized**.

---

### **✅ Step 6: Deploy on Render**
1. **Go to Render.com**
2. **Create a new Web Service**  
   - **Link your GitHub repo**
   - **Select branch** (e.g., `main` or `master`)
   - **Set Build Command**:  
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Set Start Command**:  
     ```bash
     gunicorn movie_reservation.wsgi:application
     ```
3. **Add Environment Variables in Render**
   - `DATABASE_URL` → Copy from your PostgreSQL database.
   - `SECRET_KEY` → Copy from `.env`.
4. **Deploy the app.** 🎉

---

### **✅ Step 7: Create a Superuser**
Once deployed, **if needed**, create a superuser:
```bash
python manage.py createsuperuser
```
Then login at:
```
https://your-app.onrender.com/admin/
```

---

## **💾 FINAL CHECKLIST**
✅ `DATABASES` configured with `dj_database_url`  
✅ `.env` file created **(but not committed to Git)**  
✅ `requirements.txt` updated  
✅ `.gitignore` updated  
✅ Migrations applied  
✅ Render deployment configured  
✅ Superuser created (if needed)  