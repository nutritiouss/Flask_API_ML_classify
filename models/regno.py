import os
# from configparser import ConfigParser
import logging
import numpy as np
import re
import pandas as pd
import calendar
from catboost import CatBoostClassifier

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(name)s: %(message)s',
    level=logging.INFO
)


class regno:
    """
    Description:
    Классификация автомобильных номеров
    Usage:
    Используются входные параметры, поступющие извне
    camera_regno, nn_regno, camera_score, nn_score, nn_sym_scores, nn_len_scores, camera_type,
    camera_class,time_check, direction, model_name
    Result:
    Вероятности принаделжности к позитивному или негативному классу
    """

    def __init__(self):
        self.ai_sym = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'D', 'А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р',
                       'С', 'Т', 'У', 'Х']
        self.old_cyrillic_sym = ['И', 'Й', 'Ц', 'Г', 'Ш', 'Щ', 'З', 'Ъ', 'Ф', 'Ы', 'П', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч',
                                 'Ь', 'Б', 'Ю']
        self.lat_sym = ['Q', 'W', 'R', 'Y', 'U', 'I', 'S', 'F', 'G', 'J', 'L', 'Z', 'V', 'N']

    def __d(self,alist, blist):
        zipped = (zip(alist, blist))
        um1 = dict(sorted(zipped, key=lambda t: t[1], reverse=True))
        return um1

    def __get_ai_syms(self,nn_regno, nn_sym_scores):
        letters = self.__d(nn_regno, nn_sym_scores)
        for s in self.ai_sym:
            if s not in letters:
                letters[s] = 1
        return letters

    def __regno_category(self,regno):

        if re.fullmatch('^[А-Я]\d{3}[А-Я]{2}\d{2}(|\d)$', regno):
            return 'private car'
        elif re.fullmatch('^[А-Я]{2}\d{5}(|\d)$', regno):
            return ' lk_taxi_r_pricep'
        elif re.fullmatch('^[А-Я]{2}\d{6}(|\d)$', regno):
            return 'lk_pricep_r_transit'
        elif re.fullmatch('^\d{4}[А-Я]{2}\d{2}(|\d)$', regno):
            return 'lk_moto_tract'
        elif re.fullmatch('^[А-Я]{1}\d{4}[А-Я]{2}$', regno):
            return 'some'
        elif re.fullmatch('^[А-Я]{2}\d{3}[А-Я]\d{2}(|\d)$', regno):
            return 'lk_transit'
        elif re.fullmatch('^(T|Т)[А-Я]{2}\d{5}(|\d)$', regno):
            return 'lk_export'
        elif re.fullmatch('^[А-Я]\d{6}(|\d)$', regno):
            return 'lk_mvd_avto'
        elif re.fullmatch('^\d{4}[А-Я]\d{2}(|\d)$', regno):
            return 'lk_mvd_moto'
        elif re.fullmatch('^\d{3}[А-Я]\d{2}(|\d)$', regno):
            return 'lk_mvd_pricep'
        elif re.fullmatch('^\d{3}(CD|СD|D|T|Т)\d{3}(|\d)(|\d)(|\d)$', regno):
            return 'lk_diplomat'
        elif re.fullmatch('^\d{4}[А-Я]{2}\d{2}(|\d)$', regno):
            return 'lk_army'
        else:
            return 'unknown'

    def __count_foreign_syms(self,regno):
        i = 0
        for s in regno:
            if s not in (self.ai_sym + self.old_cyrillic_sym + self.lat_sym):
                i += 1

    def __str_to_list(self,s):
        if s != '[]':
            s = s[1:-1].split(',')
            return [float(i) for i in s]
        else:
            return [0]

    def pick_regno(self,camera_regno, nn_regno, camera_score, nn_score, nn_sym_scores, nn_len_scores, camera_type,
                   camera_class,
                   time_check, direction, model_name):
        # model_name - path to the model

        x = {}
        x['afts_regno_ai_score'] = nn_score
        x['direction'] = direction
        x['recognition_accuracy'] = camera_score

        logger.info(f" before execute __str_to_list function")
        nn_sym_scores = self.__str_to_list(nn_sym_scores)
        nn_len_scores = self.__str_to_list(nn_len_scores)

        x['max_sym_score'] = np.max(nn_sym_scores)
        x['min_sym_score'] = np.min(nn_sym_scores)
        x['max_len_score'] = np.max(nn_len_scores)

        x['ai_len'] = len(nn_regno)
        x['cam_len'] = len(camera_regno)

        x['regno_recognize_text'] = ' '.join(camera_regno)
        x['afts_regno_ai_text'] = ' '.join(nn_regno)

        x['camera_type'] = camera_type
        x['camera_class'] = camera_class

        time_check = pd.to_datetime(time_check)
        x['weekday'] = calendar.day_name[time_check.dayofweek]
        x['month'] = calendar.month_name[time_check.month]
        x['hour'] = time_check.hour

        x['regno_template'] = self.__regno_category(camera_regno)
        x['regno_template_ai'] = self.__regno_category(nn_regno)

        x['foreign_sym'] = self.__count_foreign_syms(camera_regno)
        # print(x)

        letters = self.__get_ai_syms(nn_regno, nn_sym_scores)


        x.update(letters)

        model = CatBoostClassifier()
        model.load_model(model_name)
        logger.info(f"load Catboost model with features {model.feature_names_}")
        # print()
        # print(sorted(model.feature_names_))
        # print()
        # print(pd.Series(x))

        y = model.predict_proba(pd.Series(x)[model.feature_names_])

        return y

