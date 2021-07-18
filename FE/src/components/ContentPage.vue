<template>
  <div id="content-container">
    <!-- Profile card section -->
    <section id="detected-section">
      <!-- loading -->
      <loading v-if="isLoading" />
      <!-- instruction user -->
      <instruction v-if="isInit" />
      <!-- nodata -->
      <nodata v-if="!isHaveData && !isInit && !isLoading" />
      <b-card v-if="isHaveData">
        <div v-if="!isLoading || file != undefined">
          <b-row class="p-2">
            <b-col cols="4">
              <h3>Sound list</h3>
            </b-col>
            <b-col cols="8">
              <div class="sound-detection-container">
                <template v-if="detect !== '' && isHaveData">
                  <div>
                    <b-row class="mb-3">
                      <b-col cols="6">
                        <h3>Predict result</h3>
                      </b-col>
                      <b-col cols="6">
                        <div class="legend-content">
                          <div class="legend-bg bg-danger" />
                          <span class="legend-text">Positive</span>
                          <div class="legend-bg bg-success" />
                          <span class="legend-text">Negative</span>
                        </div>
                      </b-col>
                    </b-row>
                  </div>
                </template>
              </div>
            </b-col>
          </b-row>
          <sound-prediction-item
            @explain="explainMoreAction"
            ref="cough-item"
            :exData="{
              detect: detect,
              file: file,
              fileName: fileName,
              isGoodCondition: isGoodCondition,
            }"
          >
            <template v-slot:sound-title> Cough </template>
          </sound-prediction-item>
          <sound-prediction-item
            ref="mouth-item"
            @explain="explainMoreAction"
            :exData="{
              detect: detect,
              file: file,
              fileName: fileName,
              isGoodCondition: isGoodCondition,
            }"
          >
            <template v-slot:sound-title> Breath (mouth) </template>
          </sound-prediction-item>
          <sound-prediction-item
            ref="nose-item"
            @explain="explainMoreAction"
            :exData="{
              detect: detect,
              file: file,
              fileName: fileName,
              isGoodCondition: isGoodCondition,
            }"
          >
            <template v-slot:sound-title> Breath (nose) </template>
          </sound-prediction-item>
        </div>
        <explain-model ref="explain-more-model" />
      </b-card>
    </section>
  </div>
</template>

<script>
import AudioPredictionServices from '../services/audio-prediction-services';
import SoundPredictionItem from './child-components/SoundPredictionItem';
import Nodata from './common/Nodata';
import Instruction from './common/Instruction';
import Loading from './common/Loading';
import ExplainModel from './child-components/ExplainMoreModel';
import { mapActions } from 'vuex';

export default {
  name: 'ContentPage',
  components: {
    loading: Loading,
    nodata: Nodata,
    explainModel: ExplainModel,
    instruction: Instruction,
    soundPredictionItem: SoundPredictionItem,
  },
  data() {
    return {
      test: undefined,
      isInit: false,
      isHaveData: false,
      isLoading: false,
      isFeatureLoading: false,
      isGoodCondition: true,
      searchText: '',
      file: undefined,
      fileName: undefined,
      featureImage: undefined,
      detect: '',
      // If good result > goodScoreCondition
      // => Good case else Bad case
      goodScoreCondition: 0.6,
    };
  },
  mounted() {
    this.isInit = true;
    this.getResult();
  },
  methods: {
    ...mapActions({
      isChangeNav: 'isChangeNav',
    }),
    explainMoreAction() {
      const data = {
        audioName: this.fileName,
        status: this.isGoodCondition,
        detect: this.detect,
        featureImage: this.featureImage,
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
          this.isGoodCondition = true;
          // this.isGoodCondition = false;
        } else {
          this.isGoodCondition = false;
        }
      }
    },
    // Audio detion API to detect good or bad audio condition
    audioDetection(event) {
      const tmpFile = event.target.files[0];
      if (!tmpFile || tmpFile === undefined) {
        return;
      }
      this.detect = [];
      this.isInit = false;
      this.isHaveData = false;
      this.isLoading = true;
      this.isFeatureLoading = false;
      this.fileName = tmpFile.name;
      this.file = URL.createObjectURL(tmpFile);
      const data = new FormData();
      data.append('audio_data_cough', tmpFile);
      AudioPredictionServices.audioDetectionVGG16V1(
        data,
        (resp) => {
          this.isLoading = false;
          if (!resp.data || resp.data.result.length === 0) {
            this.isHaveData = false;
          } else {
            this.isHaveData = true;
            const result = parseFloat(resp.data.result);
            this.detect.push(1 - result);
            this.detect.push(result);
            // this.detect = resp.data.result;
            this.checkIsGoodCondition(this.detect);
            this.visualize(data);
          }
        },
        () => {
          this.isLoading = false;
        }
      );
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
        this.$refs['cough-item'].done();
        this.$refs['mouth-item'].done();
        this.$refs['nose-item'].done();
        this.featureImage = resp.data.cough_feature_url;
      });
      // }
    },
    getResult() {
      this.isInit = false;
      this.detect = [];
      const url = new URL(window.location.href);
      const id = url.searchParams.get('submit_id');
      AudioPredictionServices.audioGetResultVGG16V1(
        id,
        (resp) => {
          this.isLoading = false;
          this.isHaveData = true;
          const data = resp.data;
          const result = parseFloat(resp.data.results.cough_result);
          this.file = `${data.cough}`;
          this.detect.push(1 - result);
          this.detect.push(result);
          this.featureImage = resp.data.cough_feature_url;
          if (!this.featureImage) {
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
</style>
