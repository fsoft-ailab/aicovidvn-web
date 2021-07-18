import Axios from 'axios'

const baseAxios = Axios.create({
  baseURL: process.env.VUE_APP_BASE_HOST_URL
})

export default {
  getBaseInstance () {
    return baseAxios
  },
  generateInstanceFromBaseUrl (baseURL) {
    return Axios.create({
      baseURL
    })
  },
  generateInstanceFromConfig (config) {
    return Axios.create(config)
  }
}
