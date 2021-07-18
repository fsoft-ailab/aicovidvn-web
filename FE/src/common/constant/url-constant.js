export default {
  BASE_URL: `${process.env.BASE_URL}`,
  page: {
    HOME: '/home',
    DEFAULT: '/home'
  },
  apis: {
    BASE_API: `${process.env.BASE_API}/apis`,
    V1: {
      AUDIO_PREDICTION_SVM: '/svm/v1/audio-prediction',
      AUDIO_PREDICTION_VGG16: '/vgg16/v1/audio-prediction',
      AUDIO_VISUALIZATION_SVM: '/svm/v1/audio-visualization',
      AUDIO_VISUALIZATION_VGG16: '/vgg16/v1/audio-visualization',
      AUDIO_GET_RESULT: '/vgg16/v1/results',
      ADD_FEEDBACK: '/v1/feedback',
      CHECK_AUDIO: '/v1/check-audio',
    },
    REPORT: '/report'
  }
}
