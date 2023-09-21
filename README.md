
<h2>В новой версии БД сохраняется в папке instance. В командной строке пишем: </h2>
<code>
from app import app, db
app.app_context().push()
db.create_all()
</code>