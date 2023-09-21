<h3> Новый учебный сайт на джанго</h3>
<h2>Для запуска</h2>
<code>pip install -r requirements.txt | python app.py</code>


<h2>В новой версии БД сохраняется в папке instance. В командной строке пишем: </h2>
<code>
from app import app, db
app.app_context().push()
db.create_all()
</code>