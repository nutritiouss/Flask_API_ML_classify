from flask import Flask,  request
import os
from configparser import ConfigParser
#import sentry_sdk
#from sentry_sdk.integrations.flask import FlaskIntegration
import logging
from werkzeug.middleware.proxy_fix import ProxyFix
import components.response as response
from prometheus_flask_exporter import PrometheusMetrics
from controllers.regno_controller import regno_controller

#читаем конфиг
config_ini = f"{os.path.dirname(__file__)}/config/config.ini"
config = ConfigParser()
config.read(config_ini)


# мониторинг sentry
dsn = config["monitoring"]["sentry_dsn"]
# sentry_sdk.init(
#     dsn=dsn,
#     integrations=[FlaskIntegration()]
# )


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
)

app = Flask(__name__)

PrometheusMetrics(app, group_by='endpoint')
app.register_blueprint(blueprint=regno_controller)


x_api_key = config["global_settings"]["api_key"]
# Проверяем авторизацию и обходим метрики.
@app.before_request
def auth():
    api_key = request.headers.get("x-api-key", default=None)
    logger.info(f"request url {request.url}")
    if request.url != 'http://flask:5000/metrics':
        if api_key != x_api_key:
            return response.response_fail_auth()


@app.errorhandler(code_or_exception=500)
def internal_server_error(exception):
    return response.response_internal_server_error(exception)


@app.errorhandler(code_or_exception=401)
def unauthorized():
    return response.response_fail_auth()


@app.errorhandler(code_or_exception=404)
def page_not_found():
    return response.response_not_found()


@app.errorhandler(code_or_exception=400)
def bad_request(exception):
    return response.response_bad_request(str(exception))


@app.errorhandler(code_or_exception=405)
def method_not_allowed():
    return response.response_method_not_allowed()


@app.route(rule="/")
def default_page():
    return response.response_success("ok")


def main():
    app.run(port=5000, host="0.0.0.0")#, debug=True ,threaded=True

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    main()



