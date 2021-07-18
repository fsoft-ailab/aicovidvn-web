import time
import json
from common import constant
from utils import log_service, utils, postgres_util, s3_util


class AudioCollectionServices():
    def __init__(self, base_dir=None):
        self.base_dir = base_dir


    def collect(self, form_data, cough_sound, mouth_sound, nose_sound):
        is_update = False
        submit_id = int(time.time())

        if cough_sound is not None:
            cough_sound_name = cough_sound.filename
        if mouth_sound is not None:
            mouth_sound_name = mouth_sound.filename
        if nose_sound is not None:
            nose_sound_name = nose_sound.filename

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

            try:
                device_model = form_data_json['devicetype']
                del form_data_json['devicetype']
            except:
                device_model = 'Laptop/Desktop'

            form_data_json['device_model'] = device_model

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

            self.base_dir = "{}/{}".format(constant.TMP_DIR, submit_id)

            # Create directory if not exist
            utils.create_directory(self.base_dir)

            if (('No' in form_data_json['medical_condition_choice']) and (
                    'No' in form_data_json['symptoms_status_choice'])):
                health = 'good_'
                health_status = 0
            else:
                health = 'bad_'
                health_status = 1

            s3_cough_dir = None
            s3_nose_dir = None
            s3_mouth_dir = None

            if cough_sound is not None:
                cough_sound_dir = "{}/{}_original.wav".format(self.base_dir, "cough")
                cough_save_dir = f"{constant.DATA_DIR}/{constant.COUGH}/{health + cough_sound_name}.wav"
                cough_sound.save(cough_sound_dir)
                s3_util.upload_file(cough_sound_dir, cough_save_dir)
                s3_cough_dir = s3_util.generate_url(cough_save_dir)

            if mouth_sound is not None:
                mouth_sound_dir = "{}/{}_original.wav".format(self.base_dir, "mouth")
                mouth_save_dir = f"{constant.DATA_DIR}/{constant.MOUTH}/{health + mouth_sound_name}.wav"
                mouth_sound.save(mouth_sound_dir)
                s3_util.upload_file(mouth_sound_dir, mouth_save_dir)
                s3_mouth_dir = s3_util.generate_url(mouth_save_dir)

            if nose_sound is not None:
                nose_sound_dir = "{}/{}_original.wav".format(self.base_dir, "nose")
                nose_save_dir = f"{constant.DATA_DIR}/{constant.NOSE}/{health + nose_sound_name}.wav"
                nose_sound.save(nose_sound_dir)
                s3_util.upload_file(nose_sound_dir, nose_save_dir)
                s3_nose_dir = s3_util.generate_url(nose_save_dir)

            label_dir = "{}/{}_original.json".format(self.base_dir, "label")

            sound_name = ''
            if cough_sound is not None:
                sound_name = cough_sound_name
            elif mouth_sound is not None:
                sound_name = mouth_sound_name
            else:
                sound_name = nose_sound_name

            extention = sound_name.split('_')[-1]
            label_name = health + 'label_' + extention
            label_save_dir = f"{constant.LABEL_DIR}/{label_name}.json"
            with open(label_dir, 'w', encoding='utf-8') as outfile:
                json.dump(form_data_json, outfile, ensure_ascii=False)

            s3_util.upload_file(label_dir, label_save_dir, extra_args=constant.S3_JSON_EXTRA_PARAM)

            db = postgres_util.PostgresDB()
            if is_update:
                update_query = "UPDATE collections " \
                               "SET cough=%s, breathe_nose=%s, breathe_mouth=%s, info=%s, health_status=%s, borowed_device=%s " \
                               "WHERE id=%s"
                db.execute_query_with_data(update_query, data=(
                    s3_cough_dir, s3_nose_dir, s3_mouth_dir, str(form_data),
                    health_status, borowedDevice, submit_id))
            else:
                query = "INSERT INTO collections(id,email,cough,breathe_nose,breathe_mouth,info,health_status,borowed_device) " \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                db.execute_query_with_data(query, data=(
                    str(submit_id), str(email), s3_cough_dir, s3_nose_dir, s3_mouth_dir, str(form_data),
                    health_status, borowedDevice))

            db.close_connection()

            return submit_id

        except Exception as e:
            utils.remove_folder(self.base_dir)
            log_service.exception(str(e))
