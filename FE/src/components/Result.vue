<template>
  <main-layout>
    <template slot="header">
      <main-header />
    </template>
    <template slot="main">
      <main id="detected-section">
        <div class="container-sm">
          <!-- loading -->
          <loading v-if="isLoading" />
          <!-- instruction user -->
          <instruction v-if="isInit" />
          <!-- nodata -->
          <nodata v-if="!isHaveData && !isInit && !isLoading" />
          <template v-if="isHaveData">
            <div v-if="!isLoading || file != undefined">
              <b-card class="card-custom">
                <b-row class="p-2">
                  <b-col cols="12">
                    <div class="sound-detection-container">
                      <template v-if="detect !== '' && isHaveData">
                        <div>
                          <b-row class="mb-3">
                            <b-col cols="12" lg="4">
                              <h5 class="text-left">{{ $t('analyzing') }}</h5>
                            </b-col>
                            <b-col cols="12" lg="8">
                              <div class="legend-content">
                                <div class="legend-bg bg-danger" />
                                <span class="legend-text">{{
                                  $t('positive')
                                }}</span>
                                <div class="legend-bg bg-success" />
                                <span class="legend-text">{{
                                  $t('negative')
                                }}</span>
                              </div>
                            </b-col>
                          </b-row>
                        </div>
                      </template>
                    </div>
                  </b-col>
                </b-row>
                <sound-prediction-item
                  @explain="explainMoreAction('cough')"
                  ref="cough-item"
                  :exData="{
                    detect: detect['cough'],
                    file: file['cough'],
                    fileName: fileName['cough'],
                    isGoodCondition: isGoodCondition['cough'],
                  }"
                >
                  <template v-slot:sound-title> {{ $t('cough') }} </template>
                </sound-prediction-item>
                <sound-prediction-item
                  ref="mouth-item"
                  @explain="explainMoreAction('mouth')"
                  :exData="{
                    detect: detect['mouth'],
                    file: file['mouth'],
                    fileName: fileName['mouth'],
                    isGoodCondition: isGoodCondition['mouth'],
                  }"
                >
                  <template v-slot:sound-title
                    >{{ $t('breath_mouth') }}
                  </template>
                </sound-prediction-item>
                <sound-prediction-item
                  ref="nose-item"
                  @explain="explainMoreAction('nose')"
                  :exData="{
                    detect: detect['nose'],
                    file: file['nose'],
                    fileName: fileName['nose'],
                    isGoodCondition: isGoodCondition['nose'],
                  }"
                >
                  <template v-slot:sound-title>
                    {{ $t('breath_nose') }}
                  </template>
                </sound-prediction-item>
              </b-card>
              <b-card class="card-custom">
                <combine-result :data="{ isGoodCondition: isGoodCondition }" />
              </b-card>
              <b-card class="card-custom">
                <feedback />
              </b-card>
            </div>
            <explain-model ref="explain-more-model" />
          </template>
        </div>
      </main>
    </template>
  </main-layout>
</template>

<script>
import MainLayout from './MainLayout';
import Header from './Header';
import Nodata from './common/Nodata';
import Instruction from './common/Instruction';
import Loading from './common/Loading';
import SoundPredictionItem from './child-components/SoundPredictionItem';
import ExplainModel from './child-components/ExplainMoreModel';
import Feedback from './child-components/Feedback';
import CombineResult from './child-components/CombineResult';

import AudioPredictionServices from '../services/audio-prediction-services';

export default {
  name: 'Result',
  components: {
    loading: Loading,
    nodata: Nodata,
    instruction: Instruction,
    soundPredictionItem: SoundPredictionItem,
    explainModel: ExplainModel,
    feedback: Feedback,
    combineResult: CombineResult,
    'main-layout': MainLayout,
    'main-header': Header,
  },
  data() {
    return {
      isInit: false,
      isHaveData: false,
      isLoading: false,
      isFeatureLoading: false,
      isGoodCondition: {},
      searchText: '',
      file: {},
      fileName: {},
      featureImage: {},
      detect: '',
      retry: 0,
      // If good result > goodScoreCondition
      // => Good case else Bad case
      goodScoreCondition: 0.6,
      testData: [
        {
          id: '8amV2pq0',
          cough:
            'https://tmp-sounddr-data.s3-ap-southeast-1.amazonaws.com/tmp/8amV2pq0/cough_original.wav',
          results: { cough_result: 0.33741843700408936 },
          cough_feature_url:
            'https://tmp-sounddr-data.s3-ap-southeast-1.amazonaws.com/tmp/8amV2pq0/cough.jpg',
        },
      ],
    };
  },
  mounted() {
    this.isInit = true;
    this.handleMode();
  },
  methods: {
    handleMode() {
      const url = new URL(window.location.href);
      const mode = url.searchParams.get('mode');
      if (mode === 'test') {
        this.getTestResult();
      } else {
        this.getResult();
      }
    },
    explainMoreAction(key) {
      const data = {
        audioName: this.fileName[key],
        status: this.isGoodCondition[key],
        detect: this.detect[key],
        featureImage: this.featureImage[key],
      };
      this.$refs['explain-more-model'].initData(data);
      this.$refs['explain-more-model'].showModel();
    },
    // Check when audio result is good case
    checkIsGoodCondition(data) {
      // In case data is empty
      if (data && data.length > 0) {
        const goodMatch = data[0];
        if (goodMatch >= this.goodScoreCondition) {
          return true;
        } else {
          return false;
        }
      }
    },
    visualize(id) {
      setTimeout(() => {
        this.$refs['cough-item'].process();
        this.$refs['mouth-item'].process();
        this.$refs['nose-item'].process();
      });
      // Viualize data when it is not good condition
      // if (!this.isGoodCondition) {
      AudioPredictionServices.audioGetVisualizationVGG16V1(id, (resp) => {
        if (resp.data.server_busy) {
          this.$refs['cough-item'].busy();
          this.$refs['mouth-item'].busy();
          this.$refs['nose-item'].busy();
          this.retry += 1;

          if (this.retry < 5) {
            setTimeout(() => {
              this.getResult();
            }, 30000);
          }
        } else {
          this.$refs['cough-item'].done();
          this.$refs['mouth-item'].done();
          this.$refs['nose-item'].done();
          this.featureImage['cough'] = resp.data.cough_feature_url;
          this.featureImage['mouth'] = resp.data.mouth_feature_url;
          this.featureImage['nose'] = resp.data.nose_feature_url;
        }
      });
      // }
    },
    getTestResult() {
      this.isLoading = true;
      this.isInit = false;
      this.detect = [];
      const url = new URL(window.location.href);
      const id = url.searchParams.get('submit_id');
      setTimeout(() => {
        this.isLoading = false;
        this.isHaveData = true;
        const data = this.testData.find((e) => e.id === id);
        const result = parseFloat(data.results.cough_result);
        this.file = `${data.cough}`;
        this.fileName = data.cough;
        this.detect.push(1 - result);
        this.detect.push(result);
        this.featureImage = data.cough_feature_url;
      }, 2000);
    },
    getResult() {
      this.isLoading = true;
      this.isInit = false;
      this.detect = {};
      this.detect['cough'] = [];
      this.detect['mouth'] = [];
      this.detect['nose'] = [];

      const url = new URL(window.location.href);
      const id = url.searchParams.get('submit_id');

      const calResult = (result) => {
        result = parseFloat(result);
        const tmp = [];
        tmp.push(1 - result);
        tmp.push(result);
        return tmp;
      };

      AudioPredictionServices.audioGetResultVGG16V1(
        id,
        (resp) => {
          this.isLoading = false;
          this.isHaveData = true;
          const data = resp.data;
          ['cough', 'mouth', 'nose'].forEach((key) => {
            this.file[key] = data[key];
            this.detect[key] = calResult(resp.data.results[`${key}_result`]);
            this.featureImage[key] = resp.data[`${key}_feature_url`];
            this.isGoodCondition[key] = this.checkIsGoodCondition(
              this.detect[key]
            );
          });
          if (
            !this.featureImage['cough'] ||
            !this.featureImage['mouth'] ||
            !this.featureImage['nose']
          ) {
            this.visualize(id);
          } else {
            this.$refs['cough-item'].done();
            this.$refs['mouth-item'].done();
            this.$refs['nose-item'].done();
          }
        },
        () => {
          this.isLoading = false;
        }
      );
    },
  },
};
</script>

<style scoped>
#content-container {
  min-height: calc(100vh - 215px);
}

#detected-section {
  margin-top: 40px;
}

#detected-section audio:focus {
  outline: none;
}

#detected-section .img-container {
  width: 100%;
}
#detected-section .legend-content {
  float: right;
  position: relative;
  top: 3px;
  display: block;
  margin-right: 1rem;
  font-size: 1rem;
}
#detected-section .legend-bg {
  display: inline-block;
  width: 30px;
  height: 15px;
  margin-right: 0.5rem;
}

#detected-section .legend-text {
  font-size: 0.8rem;
  margin-right: 0.5rem;
}
.main-session {
  margin-top: 80px;
}
.card-custom {
  border-radius: 10px;
  margin-bottom: 1.5rem;
}
</style>
