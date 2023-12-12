# DBMS_final
## 建立 PostgreSQL 資料庫

在安裝 PostgreSQL 後，我們將為 Django 專案建立資料庫來儲存所需資料。

### 使用 pgAdmin 管理 PostgreSQL

在安裝過程中，系統會自動安裝 pgAdmin 工具，方便開發人員管理 PostgreSQL 資料庫。

1. **開啟 pgAdmin：**
   - 在 Windows，您可以透過搜尋「pgAdmin」來開啟它。
   - 或者，在安裝目錄（例如：`C:\\Program Files\\PostgreSQL\\12\\pgAdmin 4\\bin`）中找到 `pgAdmin4` 執行檔。

2. **登入 pgAdmin：**
   - 啟動 pgAdmin 後，系統會提示您輸入 PostgreSQL 的密碼。成功登入後，您將看到 pgAdmin 的主界面。

3. **建立 Server Group (伺服器群組)：**
   - 在 PostgreSQL 資料庫架構中，最頂層為 Server Group。您需要首先建立一個 Server Group。
   - 按照提示，輸入自訂的 Server Group 名稱。


4. **在 Server Group 下新增 Server (伺服器)：**
   - 在您創建的 Server Group 下，新增一個 Server。
   - 您需要為 Server 輸入自訂名稱，並設定位址及密碼。若在本地端執行，位址為 `localhost`。


5. **建立資料庫：**
   - 在新建立的 Server 下，建立一個資料庫。
   - 輸入資料庫名稱並儲存。


6. **還原資料庫：**
   - 若您有一個資料庫備份檔案（如 `DBMS_final_project_backup_v2.sql`），您可以透過以下步驟來還原它：
     1. 在 pgAdmin 中選擇您剛建立的資料庫。
     2. 點擊「工具」菜單中的「還原」選項。
     3. 選擇您的 `.sql` 備份檔案，並開始還原過程。


完成以上步驟後，您將擁有一個已還原的 PostgreSQL 資料庫，適用於 Django 專案。
## 設定 Django 連接 PostgreSQL

在建立好 PostgreSQL 資料庫之後，我們需要設定 Django 以便它可以與資料庫溝通。

### 安裝 psycopg2 套件

首先，安裝 `psycopg2` 套件，這個套件允許 Python 應用程式與 PostgreSQL 資料庫進行連接。

執行以下指令來安裝 `psycopg2`：

```
$ pip install psycopg2
```
### 更新 Django 設定

安裝完 `psycopg2` 後，您需要更新 Django 專案的 `settings.py` 檔案，以使用 PostgreSQL 資料庫。

打開 `settings.py`，並將 `DATABASES` 設定更改為以下內容：
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL
        'NAME': 'BOOKSTORE',  # 資料庫名稱
        'USER': 'postgres',  # 資料庫帳號
        'PASSWORD': '****',  # 資料庫密碼
        'HOST': 'localhost',  # Server(伺服器)位址
        'PORT': '5432'  # PostgreSQL Port號
    }
}

```
### 執行 Django Migration

接著，執行 Django Migration (資料遷移) 指令，將 Django Model 中的資料模型同步至 PostgreSQL 資料庫中。
```
 python manage.py migrate
```
完成這些步驟後，您的 Django 專案應該已經成功連接到 PostgreSQL 資料庫。