import axiosProvider from '../common/axios/axios-instance-provider'
import UrlConstant from '../common/constant/url-constant'

const baseInstance = axiosProvider.generateInstanceFromBaseUrl(
  UrlConstant.apis.BASE_API
)

export default {
  checkAudio(data, callback, errorCallback) {
    baseInstance
      .post(UrlConstant.apis.V1.CHECK_AUDIO, data)
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
