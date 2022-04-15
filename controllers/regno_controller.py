import os
import json
from flask import Blueprint, request,jsonify
from models import regno
from components.timer import time_of_function
import logging
from configparser import ConfigParser



logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(name)s: %(message)s',
    level=logging.INFO
)

config_ini = f"{os.path.dirname(__file__)}/../config/config.ini"

config = ConfigParser()
config.read(config_ini)
x_api_key = config["global_settings"]["api_key"]


reg = regno.regno()
regno_controller = Blueprint(name="regno",
                             import_name=__name__
                        ,url_prefix='/reg')


@regno_controller.route(rule="/", methods=["POST"])
@time_of_function
def regno_control():
    """ get request, parse them, send to regno model
    В эндпоинте запроса в конце должна быть обязательно косая черта и двойные кавычки в словаре"""

    if request.method == 'POST':
        logger.info(f"GET params: {request.json }")
    regno_data = request.json
    logger.info(f"handling request for regno score")
    try:
        regno_data = json.loads(regno_data)
    except Exception:
        logger.info(f"No succed attempt to transform from Json to dict")
    logger.info(f"take data {regno_data}")
    logger.info(f"handling request from  regno_control to get score")
    score = reg.pick_regno(*regno_data.values(), f"{os.path.dirname(__file__)}/micromodel.cbm")
    json_score = {'positive':score[1],'negative':score[0]}
    logger.info(f"The score is {json_score}")

    return jsonify({"body": json_score, "status": "ok"}), 200

