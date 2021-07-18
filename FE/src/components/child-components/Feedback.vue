<template>
  <section>
    <b-row>
      <b-col cols="12">
        <div class="p-3">
          <h5 class="feedback-title">{{ $t('confirmation') }}</h5>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <div class="p-3">
          <p>
            {{ $t('confirm_q1') }}
          </p>
        </div>
      </b-col>
      <b-col cols="12">
        <!-- <b-row>
          <b-col cols="6">
            <div class="feedback-container">
              <button @click="feedback(1)">
                <b-icon-check-circle-fill
                  variant="success"
                  class="feedback-icon"
                />
                <div class="text-success">{{ $t('agree') }}</div>
              </button>
            </div>
          </b-col>
          <b-col cols="6">
            <div class="feedback-container">
              <button @click="feedback(0)">
                <b-icon-x-circle-fill variant="danger" class="feedback-icon" />
                <div class="text-danger">{{ $t('disagree') }}</div>
              </button>
            </div></b-col
          >
        </b-row> -->
        <vue-feedback-reaction
          v-model="feedbackData"
          :labels="['1', '2', '3', '4', '5']"
          @input="reactionChange"
        />
      </b-col>
      <b-col cols="12">
        <b-button
          variant="primary"
          class="mt-3 mx-3"
          @click="feedback"
          :disabled="!isChange"
          >{{ $t('submit') }}</b-button
        >
      </b-col>
    </b-row>
    <thankYouModal ref="thank-you-modal" />
  </section>
</template>

<script>
import ThankYouModal from './ThankYouModel';
import { VueFeedbackReaction } from 'vue-feedback-reaction';
import AudioPredictionServices from '../../services/audio-prediction-services';

export default {
  components: {
    thankYouModal: ThankYouModal,
    VueFeedbackReaction,
  },
  data() {
    return {
      isChange: false,
      feedbackData: '',
    };
  },
  methods: {
    reactionChange() {
      this.isChange = true;
    },
    feedback() {
      const url = new URL(window.location.href);
      const id = url.searchParams.get('submit_id');
      const data = new FormData();
      data.append('submit_id', id);
      data.append('type', this.feedbackData);
      AudioPredictionServices.addFeedback(data, () => {
        this.$refs['thank-you-modal'].showModal();
        this.isChange = false;
      });
    },
  },
};
</script>

<style scoped>
.feedback-title {
  margin-top: 20px;
}
.feedback-container {
  text-align: center;
  padding: 1rem 1rem;
}
.feedback-container:hover {
  cursor: pointer;
}
.feedback-container .feedback-icon {
  font-size: 3rem;
}
.feedback-container button {
  border: none;
  background: inherit;
}
.feedback-container button:focus {
  border: none;
  outline: none;
}
</style>
