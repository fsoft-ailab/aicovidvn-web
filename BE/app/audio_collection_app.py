import json
import time
import datetime
from flask import Blueprint, request
from common import url_constant, param_constant, constant
from werkzeug.exceptions import BadRequest, InternalServerError
from utils import log_service, utils, postgres_util, s3_util

mod = Blueprint('audio_collection_app', __name__)


@mod.route(url_constant.AUDIO_REPORT, methods=['GET'])
def audio_report():
    db = postgres_util.PostgresDB()
    query = "SELECT * FROM collections ORDER BY (created_date) ASC"
    cursor = db.execute_query(query)
    user_result = cursor.fetchall()
    db.close_connection()

    ids = []
    borrowed = []
    date_time = []
    health = []
    good_health = 0
    bad_health = 0
    list_date = []

    for i in user_result:
        try:
            # date_time_obj = datetime.datetime.strptime(i[8], '%Y-%m-%d %H:%M:%S.%f')
            date_time_obj = i[8]
            date_time.append(str(date_time_obj.date()))
            health.append(i[7])
            if str(i[7]) == '0':
                good_health += 1
            elif str(i[7]) == '1':
                bad_health += 1
            ids.append(i[0])
            if i[7] == 'borrowed':
                borrowed.append("true")
            else:
                borrowed.append("false")
            if str(date_time_obj.date()) not in list_date:
                list_date.append(str(date_time_obj.date()))
        except:
            pass

    number_submit = []
    new_date = []

    if list_date != 0:
        count_date = 0
        for i in list_date:
            year = i.split('-')[0]
            month = i.split('-')[1]
            date_of_month = i.split('-')[2]
            new_date.append(date_of_month + '/' + month)
            for j in date_time:
                if j == i:
                    count_date += 1
            number_submit.append(count_date)
            count_date = 0

    return json.dumps({'new_date': new_date, 'number_submit': number_submit, 'good_health': good_health,
                       'bad_health': bad_health})


@mod.route(url_constant.AUDIO_COLLECTION, methods=['POST'])
def audio_collection():
    is_update = False
    submit_id = int(time.time())
    submit_time = str(datetime.datetime.now())
    form_data = request.form['form_data']
    cough_sound = request.files.get(param_constant.PARAM_COUGH_SOUND)
    cough_sound_name = cough_sound.filename
    mouth_sound = request.files.get(param_constant.PARAM_MOUTH_SOUND)
    mouth_sound_name = mouth_sound.filename
    nose_sound = request.files.get(param_constant.PARAM_NOSE_SOUND)
    nose_sound_name = nose_sound.filename

    if len(form_data) == 0:
        raise BadRequest()

    if cough_sound is None or mouth_sound is None or nose_sound is None:
        raise BadRequest()

    base_dir = "{}/{}".format(constant.TMP_DIR, submit_id)
    try:
        # Convert to json
        form_data_json = json.loads(form_data)

        try:
            email = form_data_json['email']
        except:
            email = None

        try:
            borowedDevice = form_data_json['borowedDevice']
        except:
            borowedDevice = None

        if email is not None:
            db = postgres_util.PostgresDB()
            query = "SELECT id, email " \
                    "FROM collections " \
                    "WHERE email= %s"
            cursor = db.execute_query(query, (email,))
            data = cursor.fetchone()
            db.close_connection()

            if data is not None and data[0] is not None:
                submit_id = data[0]
                is_update = True

        base_dir = "{}/{}".format(constant.TMP_DIR, submit_id)

        # Create directory if not exist
        utils.create_directory(base_dir)

        if (('None' in form_data_json['medical_condition_choice']) and (
                'None' in form_data_json['symptoms_status_choice'])):
            health = 'good_'
            health_status = 0
        else:
            health = 'bad_'
            health_status = 1

        cough_sound_dir = "{}/{}_original.wav".format(base_dir, "cough")
        cough_save_dir = f"{constant.COLLECTION_DIR}/{constant.COUGH}/{health + cough_sound_name}.wav"
        mouth_sound_dir = "{}/{}_original.wav".format(base_dir, "mouth")
        mouth_save_dir = f"{constant.COLLECTION_DIR}/{constant.MOUTH}/{health + mouth_sound_name}.wav"
        nose_sound_dir = "{}/{}_original.wav".format(base_dir, "nose")
        nose_save_dir = f"{constant.COLLECTION_DIR}/{constant.NOSE}/{health + nose_sound_name}.wav"

        cough_sound.save(cough_sound_dir)
        mouth_sound.save(mouth_sound_dir)
        nose_sound.save(nose_sound_dir)

        s3_util.upload_file(mouth_sound_dir, mouth_save_dir)
        s3_util.upload_file(nose_sound_dir, nose_save_dir)
        s3_util.upload_file(cough_sound_dir, cough_save_dir)

        s3_mouth_dir = s3_util.generate_url(mouth_save_dir)
        s3_nose_dir = s3_util.generate_url(nose_save_dir)
        s3_cough_dir = s3_util.generate_url(cough_save_dir)

        db = postgres_util.PostgresDB()
        if  not is_update:
            query = "INSERT INTO collections(id,email,cough,breathe_nose,breathe_mouth,info,health_status,borowed_device,submit_time) " \
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            db.execute_query_with_data(query, data=(
                str(submit_id), str(email), s3_cough_dir, s3_nose_dir, s3_mouth_dir, str(form_data),
                health_status, borowedDevice, submit_time))
        else:
            update_query = "UPDATE collections " \
                           "SET cough=%s, breathe_nose=%s, breathe_mouth=%s, info=%s, health_status=%s, borowed_device=%s, submit_time=%s " \
                           "WHERE submit_id=%s"
            db.execute_query_with_data(update_query, data=(
                s3_cough_dir, s3_nose_dir, s3_mouth_dir, str(form_data),
                health_status, borowedDevice, submit_time))

        db.close_connection()

        return "true"
    except Exception as e:
        utils.remove_folder(base_dir)
        log_service.exception(str(e))
        raise InternalServerError(description=str(e))
