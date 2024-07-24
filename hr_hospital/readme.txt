dropdb -h localhost -p 5432 -U odoo_admin odoo_test

createdb -h localhost -p 5432 -U odoo_admin odoo_test

D:\Study\learning_odoo\odoo-venv\Scripts\python.exe D:\Study\learning_odoo\odoo-bin -c D:\Study\learning_odoo\conf\odoo.conf -d odoo_test --init=hr_hospital --log-level=debug
