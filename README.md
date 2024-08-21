<h1>Shop Parser</h1>
<h5>Bu loyiha elektiron magazin bo'lib mahsulotlar sotiladi. Bu loyiha Djangoda yozilgan</h5>
<h2>Ishga tushurish</h2>

      python -m venv venv

      pip freeze > requirements.txt
      
      python manage.py makemigrations

      python manage.py migrate

      python manage.py runserver
http://127.0.0.1:8000/api/schema/swagger-ui/

<h2>Parser qilish uchun</h2>

    python manage.py parse_products
<h6>Parser qilishdan oldin product/parsers.py faylini o'zingizga mostashtirib oling</h6>
  
