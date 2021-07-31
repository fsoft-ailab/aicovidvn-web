import json
import time
import base64
from flask import Blueprint, request, jsonify
from common import url_constant, param_constant, constant
from werkzeug.exceptions import BadRequest, InternalServerError
from utils import log_service, utils, postgres_util, s3_util
from services.audio_collection_services import AudioCollectionServices
from services.audio_prediction_services import AudioPredCNNService
from services.audio_checking_services import AudioCheckServices
from instance import environment
from multiprocessing import Queue

mod = Blueprint('audio_prediction_app', __name__)

# Store flag
q = Queue()


@mod.route(url_constant.CHECK_EMAIL, methods=['POST', 'GET'])
def check_email():
    try:
        is_base64_email = False
        data = request.get_data()
        my_json = data.decode('utf8')
        json_data = json.loads(my_json)
        email = json_data["email"]

        if '@' not in email:
            is_base64_email = True

        if not is_base64_email:
            email = email.lower()

        db = postgres_util.PostgresDB()
        query = "SELECT * FROM collections WHERE email= %s"
        cursor = db.execute_query_with_data(query, data=(email,))
        data = cursor.fetchone()

        if data is None:
            response = {
                'email': email,
                'status_check': 'not exist',
                'health_status': 'None'
            }
        else:
            response = {
                'email': email,
                'status_check': 'exist',
                'health_status': data[7],
                'created_time': data[8].timestamp() * 1000,
                'updated_time': data[9].timestamp() * 1000
            }

        return jsonify(response)
    except:
        return jsonify({
            'check status': {
                'status_code': 500, 'message': 'Server internal error'
            }})


@mod.route(url_constant.AUDIO_PREDICTION_VGG16_V1, methods=['POST'])
def audio_prediction_vgg16_v1():
    submit_token = request.args.get(param_constant.PARAM_SUBMIT_ID)
    submit_time = request.args.get(param_constant.PARAM_SUBMIT_TIME)

    cough_sound = request.files.get(param_constant.PARAM_COUGH_SOUND)
    mouth_sound = request.files.get(param_constant.PARAM_MOUTH_SOUND)
    nose_sound = request.files.get(param_constant.PARAM_NOSE_SOUND)

    email = request.form.get(param_constant.PARAM_EMAIL)
    info = request.form.get(param_constant.PARAM_INFO)

    if cough_sound is None and mouth_sound is None and nose_sound is None:
        raise BadRequest()

    # Collect data
    collect_ser = AudioCollectionServices()
    submit_id = collect_ser.collect(info, cough_sound, mouth_sound, nose_sound)

    base_dir = "{}/{}".format(constant.TMP_DIR, submit_id)
    base_token_dir = "{}/{}".format(constant.RESULT_DIR, submit_token)

    try:
        # Create directory if not exist
        utils.create_directory(base_dir)

        audio_service = AudioPredCNNService(max_period=10, submit_id=submit_id, submit_time=submit_time)

        s3_cough_dir = None
        s3_mouth_dir = None
        s3_nose_dir = None
        cough_predict_result = ''
        mouth_predict_result = ''
        nose_predict_result = ''

        if cough_sound is not None:
            cough_sound_dir = "{}/{}_original.wav".format(base_dir, "cough")
            cough_save_dir = f"{base_token_dir}/{constant.COUGH}_original.wav"
            cough_predict_result = audio_service.predict(cough_sound_dir, type="cough")
            s3_util.upload_file(cough_sound_dir, cough_save_dir)
            s3_cough_dir = s3_util.generate_url(cough_save_dir)
        if mouth_sound is not None:
            mouth_sound_dir = "{}/{}_original.wav".format(base_dir, "mouth")
            mouth_save_dir = f"{base_token_dir}/{constant.MOUTH}_original.wav"
            mouth_predict_result = audio_service.predict(mouth_sound_dir, type="mouth")
            s3_util.upload_file(mouth_sound_dir, mouth_save_dir)
            s3_mouth_dir = s3_util.generate_url(mouth_save_dir)
        if nose_sound is not None:
            nose_sound_dir = "{}/{}_original.wav".format(base_dir, "nose")
            nose_save_dir = f"{base_token_dir}/{constant.NOSE}_original.wav"
            nose_predict_result = audio_service.predict(nose_sound_dir, type="nose")
            s3_util.upload_file(nose_sound_dir, nose_save_dir)
            s3_nose_dir = s3_util.generate_url(nose_save_dir)

        result = json.dumps({'cough_result': cough_predict_result,
                             'mouth_result': mouth_predict_result,
                             'nose_result': nose_predict_result})

        db = postgres_util.PostgresDB()
        query = "INSERT INTO results(id,cough,breathe_nose,breathe_mouth,results,email,info) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        db.execute_query_with_data(query,
                                   data=(
                                       submit_token, s3_cough_dir, s3_nose_dir, s3_mouth_dir, str(result), email, info))
        db.close_connection()

        utils.remove_folder(base_dir)

        return result
    except:
        utils.remove_folder(base_dir)
        return jsonify({
            'check status': {
                'status_code': 500, 'message': 'Server internal error'
            }})


@mod.route(url_constant.AUDIO_VISUALIZATION_VGG16_V1, methods=['GET'])
def audio_visualization_vgg16_v1():
    try:
        # Handle multi request
        if q.qsize() > 10:
            return json.dumps({'server_busy': True})

        q.put(constant.LOCK)
        submit_id = request.args.get(param_constant.PARAM_SUBMIT_ID)
        submit_time = request.args.get(param_constant.PARAM_SUBMIT_TIME)
        base_dir = "{}/{}".format(constant.TMP_DIR, submit_id)

        # Create directory if not exist
        utils.create_directory(base_dir)
        cough_sound_dir = "{}/{}_original.wav".format(base_dir, "cough")
        cough_save_dir = cough_sound_dir.replace(constant.TMP_DIR, constant.RESULT_DIR)
        mouth_sound_dir = "{}/{}_original.wav".format(base_dir, "mouth")
        mouth_save_dir = mouth_sound_dir.replace(constant.TMP_DIR, constant.RESULT_DIR)
        nose_sound_dir = "{}/{}_original.wav".format(base_dir, "nose")
        nose_save_dir = nose_sound_dir.replace(constant.TMP_DIR, constant.RESULT_DIR)

        if submit_id is None:
            raise BadRequest()

        is_cough_existed = s3_util.download_file(cough_save_dir, cough_sound_dir)
        is_mouth_existed = s3_util.download_file(mouth_save_dir, mouth_sound_dir)
        is_nose_existed = s3_util.download_file(nose_save_dir, nose_sound_dir)

        audio_service = AudioPredCNNService(max_period=10, submit_id=submit_id, submit_time=submit_time)

        feature_cough_url = None
        feature_nose_url = None
        feature_mouth_url = None

        if is_cough_existed:
            feature_cough_image_dir = audio_service.visualize(cough_sound_dir, dest="{}/{}.jpg".format(base_dir, "cough"))
            s3_util.upload_file(feature_cough_image_dir, feature_cough_image_dir,
                                extra_args=constant.S3_IMAGE_EXTRA_PARAM)
            feature_cough_url = s3_util.generate_url(feature_cough_image_dir)
        if is_mouth_existed:
            feature_mouth_image_dir = audio_service.visualize(mouth_sound_dir, dest="{}/{}.jpg".format(base_dir, "mouth"))
            s3_util.upload_file(feature_mouth_image_dir, feature_mouth_image_dir,
                                extra_args=constant.S3_IMAGE_EXTRA_PARAM)
            feature_mouth_url = s3_util.generate_url(feature_mouth_image_dir)
        if is_nose_existed:
            feature_nose_image_dir = audio_service.visualize(nose_sound_dir, dest="{}/{}.jpg".format(base_dir, "nose"))
            s3_util.upload_file(feature_nose_image_dir, feature_nose_image_dir,
                                extra_args=constant.S3_IMAGE_EXTRA_PARAM)
            feature_nose_url = s3_util.generate_url(feature_nose_image_dir)

        db = postgres_util.PostgresDB()
        query = "UPDATE results SET cough_img= %s, breathe_nose_img= %s, breathe_mouth_img= %s WHERE id = %s"
        db.execute_query_with_data(query, data=(feature_cough_url, feature_nose_url, feature_mouth_url, submit_id))
        db.close_connection()
        utils.remove_folder(base_dir)
        q.get()

        feature_cough_url_presined = s3_util.get_presigned_url_from_original_url(feature_cough_url)
        feature_mouth_url_presined = s3_util.get_presigned_url_from_original_url(feature_mouth_url)
        feature_nose_url_presined = s3_util.get_presigned_url_from_original_url(feature_nose_url)

        return json.dumps({'cough_feature_url': feature_cough_url_presined,
                           'mouth_feature_url': feature_mouth_url_presined,
                           'nose_feature_url': feature_nose_url_presined})
    except Exception as e:
        utils.remove_folder(base_dir)
        q.get()
        return jsonify({
            'check status': {
                'status_code': 500, 'message': 'Server internal error'
            }})


@mod.route(url_constant.AUDIO_GET_RESULT, methods=['GET'])
def get_results():
    submit_id = request.args.get(param_constant.PARAM_SUBMIT_ID)

    if submit_id is None:
        raise BadRequest()

    db = postgres_util.PostgresDB()
    query = "SELECT id, breathe_nose, breathe_mouth, cough, results, cough_img, breathe_nose_img, breathe_mouth_img " \
            "FROM results " \
            "WHERE id= %s"
    cursor = db.execute_query(query, (submit_id,))
    data = cursor.fetchone()
    db.close_connection()

    if data is None:
        raise BadRequest()

    result = {}
    result["id"] = data[0]
    result["nose"] = s3_util.get_presigned_url_from_original_url(data[1])
    result["mouth"] = s3_util.get_presigned_url_from_original_url(data[2])
    result["cough"] = s3_util.get_presigned_url_from_original_url(data[3])
    result["results"] = json.loads(data[4])

    if data[5] is not None:
        result['cough_feature_url'] = s3_util.get_presigned_url_from_original_url(data[5])
    if data[6] is not None:
        result['nose_feature_url'] = s3_util.get_presigned_url_from_original_url(data[6])
    if data[7] is not None:
        result['mouth_feature_url'] = s3_util.get_presigned_url_from_original_url(data[7])

    return json.dumps(result)


@mod.route(url_constant.ADD_FEEDBACK, methods=['GET'])
def get_feedback():
    submit_id = request.args.get(param_constant.PARAM_SUSBMIT_ID)

    if submit_id is None:
        raise BadRequest()

    db = postgres_util.PostgresDB()
    query = "SELECT id, type FROM feedbacks WHERE id= %s"
    cursor = db.execute_query(query, data=(submit_id))
    data = cursor.fetchone()
    db.close_connection()

    return ""


@mod.route(url_constant.ADD_FEEDBACK, methods=['POST'])
def add_feedback():
    submit_id = request.form.get(param_constant.PARAM_SUBMIT_ID)
    type = request.form.get(param_constant.PARAM_TYPE)

    if submit_id is None or type is None:
        raise BadRequest()

    db = postgres_util.PostgresDB()
    query = "SELECT id, type FROM feedbacks WHERE id= %s"
    cursor = db.execute_query_with_data(query, data=(submit_id,))
    data = cursor.fetchone()
    if data is None or data[0] is None:
        query = "INSERT INTO feedbacks(id, type) VALUES (%s,%s)"
        db.execute_query_with_data(query, data=(submit_id, type,))
    else:
        query = "UPDATE feedbacks SET type= %s WHERE id = %s"
        db.execute_query_with_data(query, data=(type, submit_id,))
    db.close_connection()

    return ""


@mod.route(url_constant.CHECK_AUDIO, methods=['POST'])
def check_audio():
    audio = request.files.get(param_constant.PARAM_AUDIO)
    millis = int(round(time.time() * 1000))
    base_dir = "{}/{}".format(constant.TMP_DIR, f'sound-checking-{millis}')

    if audio is None:
        raise BadRequest()

    try:
        # Create directory if not exist
        utils.create_directory(base_dir)

        sound_dir = "{}/{}_original.wav".format(base_dir, "audio")
        audio.save(sound_dir)

        check_services = AudioCheckServices(max_noise_period_weight=environment.NOISE_DURATION_WEIGHT_FILTER,
                                            max_period=environment.LENGTH_FILTER)

        result = check_services.check(sound_dir, fix_length=False)

        utils.remove_folder(base_dir)
        return result
    except Exception as e:
        utils.remove_folder(base_dir)
        raise InternalServerError(description=str(e))


@mod.route(url_constant.HEALTH_CHECK, methods=['GET'])
def health_check():
    log_service.info("health_check() Start")
    return "ok"
