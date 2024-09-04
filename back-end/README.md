# Back-end

Ενδεικτικά περιεχόμενα:

- Πηγαίος κώδικας εφαρμογής για εισαγωγή, διαχείριση και
  πρόσβαση σε δεδομένα (backend).
- Database dump (sql ή json)
- Back-end functional tests.
- Back-end unit tests.
- RESTful API.

## Database Configuration & Connection

### .env template 
```bash
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_DATABASE=ntuaflix  # or the name you want for the Database
DEBUG=1
HOST=localhost
PORT=8000 # should be the same as the port defined in front-end/src/api/api.js
DB_TYPE=postgres  # optional if postgres, for MySQL, DB_TYPE=mysql
SECRET_KEY=your_secret_key
ALGORITHM=your_algorithm
FORGET_PWD_SECRET_KEY=your_forget_pwd_secret_key
```

### MySQL helping scripts 

- Quick script for dropping and creating a new database `ntuaflix` in MySQL CLI.
```bash
drop schema ntuaflix;
create schema ntuaflix;
use ntuaflix;
show tables;
```

- MySQL check after `models.py`
```bash
show tables;
show triggers;
```

Note: To see the changes between mysql and postgres in `models.py`, you can Ctrl + F : `DIFFERENT` 
