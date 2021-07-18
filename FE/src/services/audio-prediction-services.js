import axiosProvider from '../common/axios/axios-instance-provider'
import UrlConstant from '../common/constant/url-constant'

const baseInstance = axiosProvider.generateInstanceFromBaseUrl(
  UrlConstant.apis.BASE_API
)

export default {
  audioDetectionSVMV1(data, callback, errorCallback) {
    baseInstance
      .post(UrlConstant.apis.V1.AUDIO_PREDICTION_SVM, data)
      .then((res) => {
        callback(res)
      })
      .catch((err) => {
        if (errorCallback) {
          errorCallback(err)
        }
      })
  },
  audioPredictionVGG16V1(submitId, time, data, callback, errorCallback) {
    baseInstance
      .post(`${UrlConstant.apis.V1.AUDIO_PREDICTION_VGG16}?submit_id=${submitId}&submit_time=${time}`, data)
      .then((res) => {
        callback(res)
      })
      .catch((err) => {
        if (errorCallback) {
          errorCallback(err)
        }
      })
  },
  audioVisualizationSVMV1(data, callback, errorCallback) {
    baseInstance
      .post(UrlConstant.apis.V1.AUDIO_VISUALIZATION_SVM, data)
      .then((res) => {
        callback(res)
      })
      .catch((err) => {
        if (errorCallback) {
          errorCallback(err)
        }
      })
  },
  audioGetVisualizationVGG16V1(id, callback, errorCallback) {
    baseInstance
      .get(`${UrlConstant.apis.V1.AUDIO_VISUALIZATION_VGG16}?submit_id=${id}`)
      .then((res) => {
        callback(res)
      })
      .catch((err) => {
        if (errorCallback) {
          errorCallback(err)
        }
      })
  },
  audioGetResultVGG16V1(id, callback, errorCallback) {
    baseInstance.get(`${UrlConstant.apis.V1.AUDIO_GET_RESULT}?submit_id=${id}`)
      .then((res) => {
        callback(res)
      })
      .catch((err) => {
        if (errorCallback) {
          errorCallback(err)
        }
      })
  },
  addFeedback(data, callback, errorCallback) {
    baseInstance
      .post(UrlConstant.apis.V1.ADD_FEEDBACK, data)
      .then((res) => {
        callback(res)
      })
      .catch((err) => {
        if (errorCallback) {
          errorCallback(err)
        }
      })
  }
}
