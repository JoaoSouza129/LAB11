from flask import Flask



# create and configure the app
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=SECRET_KEY,
)


from . import auth
app.register_blueprint(auth.bp)

from . import store
app.register_blueprint(store.bp)

app.add_url_rule('/', endpoint='index')



