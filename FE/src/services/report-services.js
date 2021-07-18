import axiosProvider from '../common/axios/axios-instance-provider'
import UrlConstant from '../common/constant/url-constant'

const baseInstance = axiosProvider.generateInstanceFromBaseUrl(
    UrlConstant.apis.BASE_API
)

export default {
    getReportData(callback, errorCallback) {
        baseInstance
            .get(UrlConstant.apis.REPORT)
            .then((res) => {
                callback(res)
            })
            .catch((err) => {
                if (errorCallback) {
                    errorCallback(err)
                }
            })
    },
}
