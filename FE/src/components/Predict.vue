<template>
  <main-layout>
    <template slot="header">
      <main-header />
    </template>
    <template slot="main">
      <main class="main-session">
        <section class="hero text-center pb-0">
          <div class="container-sm">
            <div class="hero-inner">
              <h1
                class="hero-title h2-mobile mt-0 is-revealing"
                style="visibility: visible"
                data-language="formtitle"
              >
                {{ $t('formtitle') }}
              </h1>
            </div>
          </div>
        </section>
        <section class="newsletter section">
          <div class="container-sm">
            <div class="newsletter-inner section-inner has-bottom-divider">
              <div
                class="alert-custom alert-warning-custom"
                id="hidden_alert"
                v-if="formError"
              >
                <h5>{{ $t('errorMessageAlert') }}</h5>
                <ul class="m-0" id="alert_email" v-if="formError.email">
                  <li>{{ $t('errorEmail') }}</li>
                </ul>
                <ul class="m-0" v-if="formError.age">
                  <li>{{ $t('errorAge') }}</li>
                </ul>
                <ul class="m-0" v-if="formError.region">
                  <li>
                    {{ $t('errorRegion') }}
                  </li>
                </ul>
                <ul class="m-0" v-if="formError.medical">
                  <li data-language="errorMedicalCondition">
                    {{ $t('errorMedicalCondition') }}
                  </li>
                </ul>
                <ul class="m-0" v-if="formError.symptom">
                  <li>
                    {{ $t('errorSymptomStatus') }}
                  </li>
                </ul>
              </div>
              <div>
                <label for="email"> {{ $t('email_option') }} </label>
                <br />
                <label for="email">
                  {{ $t('emailLabel') }}
                </label>
                <br />
                <input
                  type="email"
                  id="email"
                  name="email"
                  autocomplete="on"
                  :disabled="isHaveMyFPTData"
                  placeholder="example@fsoft.com.vn"
                />
                <br />
                <br />
                <input
                  type="checkbox"
                  id="borowedDevice"
                  name="borowedDevice"
                  v-model="borowedDeviceCb"
                />
                <label for="borowedDevice">{{
                  $t('borrwedDeviceLabel')
                }}</label>
                <br />
                <br />
                <div class="alert-info alert-info-custom">
                  <h5 data-language="noteRequiredField">
                    {{ $t('noteRequiredField') }}
                  </h5>
                </div>
                <h3>{{ $t('demographics') }}</h3>
                <!-- Biological sex field -->
                <div>
                  <label for="id_sex_choice">
                    <h4>{{ $t('Q1') }}</h4>

                    <select
                      name="sex_choice"
                      id="id_sex_choice"
                      v-model="sexChoices"
                    >
                      <option value="Male" data-language="sexMale">
                        {{ $t('sexMale') }}
                      </option>

                      <option value="Female" data-language="sexFemale">
                        {{ $t('sexFemale') }}
                      </option>

                      <option value="Other" data-language="sexOther">
                        {{ $t('sexOther') }}
                      </option>
                    </select>
                  </label>
                </div>
                <!-- Age field -->
                <div>
                  <label for="id_age_choice">
                    <h4>{{ $t('Q2') }}</h4>
                    <input type="number" id="id_age_choice" name="age_choice" />
                  </label>
                </div>
                <!-- country field -->
                <div>
                  <label for="id_current_country">
                    <h4>
                      {{ $t('current_country_now') }}
                    </h4>
                    <b-form-select
                      v-model="selectedCountry"
                      size="sm"
                      :options="countryData"
                      @change="onSelectedCountry"
                    />
                  </label>
                </div>
                <!-- local field -->
                <div>
                  <label for="id_current_city">
                    <h4>
                      {{ $t('current_city_now') }}
                    </h4>
                    <b-form-select
                      v-model="selectedRegion"
                      size="sm"
                      :options="regionData"
                    />
                  </label>
                </div>
                <!-- Symptoms Survey -->
                <h3>{{ $t('Symptoms') }}</h3>
                <!-- symptoms status choice field -->
                <div class="fieldWrapper">
                  <h4>{{ $t('SymptomsQ1') }}</h4>
                  <!-- render any errors, if they exist -->
                  <label for="id_symptoms_status_choice_2">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="fever"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_2"
                    />
                    <span>
                      {{ $t('symptoms_status_choice_fever') }}
                    </span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_3">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="chills"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_3"
                    />
                    <span data-language="symptoms_status_choice_chills">
                      {{ $t('symptoms_status_choice_chills') }}
                    </span>
                  </label>
                  <br />

                  <label>
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="sorethroat"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_01"
                    />
                    <span data-language="symptoms_status_choice_sore_throat">
                      {{ $t('symptoms_status_choice_sore_throat') }}
                    </span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_4">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="drycough"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_4"
                    />
                    <span data-language="symptoms_status_choice_drycough">
                      {{ $t('symptoms_status_choice_drycough') }}
                    </span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_5">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="wetcough"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_5"
                    />
                    <span data-language="symptoms_status_choice_wetcough">
                      {{ $t('symptoms_status_choice_wetcough') }}
                    </span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_05">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="stuffynose"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_05"
                    />
                    <span data-language="symptoms_status_choice_stuffy_nose">
                      {{ $t('symptoms_status_choice_stuffy_nose') }}
                    </span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_06">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="snivel"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_06"
                    />
                    <span data-language="symptoms_status_choice_snivel">
                      {{ $t('symptoms_status_choice_snivel') }}
                    </span>
                  </label>
                  <br />

                  <label>
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="shortbreath"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_6"
                    />
                    <span data-language="symptoms_status_choice_shortbreath">
                      {{ $t('symptoms_status_choice_shortbreath') }}
                    </span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_7">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="tightness"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_7"
                    />
                    <span data-language="symptoms_status_choice_tightness">
                      {{ $t('symptoms_status_choice_tightness') }}
                    </span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_10">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="headache"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_10"
                    />
                    <span data-language="symptoms_status_choice_headache">{{
                      $t('symptoms_status_choice_headache')
                    }}</span>
                  </label>
                  <br />

                  <label for="id_symptoms_status_choice_9">
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="dizziness"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_9"
                    />
                    <span data-language="symptoms_status_choice_dizziness">{{
                      $t('symptoms_status_choice_dizziness')
                    }}</span>
                  </label>
                  <br />
                  <label>
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="muscleache"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_11"
                    />
                    <span data-language="symptoms_status_choice_muscleache">{{
                      $t('symptoms_status_choice_muscleache')
                    }}</span>
                  </label>
                  <br />

                  <label>
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="smelltasteloss"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_8"
                    />
                    <span
                      data-language="symptoms_status_choice_smelltasteloss"
                      >{{ $t('symptoms_status_choice_smelltasteloss') }}</span
                    >
                  </label>
                  <br />
                  <label>
                    <input
                      type="checkbox"
                      name="symptoms_status_choice"
                      value="No"
                      v-model="symptomsChoices"
                      @change="symptomsChange"
                      id="id_symptoms_status_choice_0"
                    />
                    <span data-language="symptoms_status_choice_none">{{
                      $t('symptoms_status_choice_none')
                    }}</span>
                  </label>
                  <br />
                </div>
                <!-- Medical conditions field, we loop! -->
                <div class="fieldWrapper">
                  <h4 data-language="Q3">
                    {{ $t('Q3') }}
                  </h4>
                  <!-- render any errors, if they exist -->
                  <div>
                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="asthma"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_2"
                      />
                      <span data-language="medicalConditionAsthma">
                        {{ $t('medicalConditionAsthma') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="cystic"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_3"
                      />
                      <span data-language="medicalCondition_cystic">
                        {{ $t('medicalCondition_cystic') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="copd"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_4"
                      />
                      <span data-language="medicalCondition_copd">
                        {{ $t('medicalCondition_copd') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="pulmonary"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_5"
                      />
                      <span data-language="medicalCondition_pulmonary">
                        {{ $t('medicalCondition_pulmonary') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="lung"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_6"
                      />
                      <span data-language="medicalCondition_lung">
                        {{ $t('medicalCondition_lung') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="hbp"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_7"
                      />
                      <span data-language="medicalCondition_hbp">
                        {{ $t('medicalCondition_hbp') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="angina"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_8"
                      />
                      <span data-language="medicalCondition_angina">
                        {{ $t('medicalCondition_angina') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="stroke"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_9"
                      />
                      <span data-language="medicalCondition_stroke">
                        {{ $t('medicalCondition_stroke') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="heart"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_10"
                      />
                      <span data-language="medicalCondition_heart">
                        {{ $t('medicalCondition_heart') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="valvular"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_11"
                      />
                      <span data-language="medicalCondition_valvular">
                        {{ $t('medicalCondition_valvular') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="otherHeart"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_12"
                      />
                      <span data-language="medicalCondition_otherHeart">
                        {{ $t('medicalCondition_otherHeart') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="diabetes"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_13"
                      />
                      <span data-language="medicalCondition_diabetes">
                        {{ $t('medicalCondition_diabetes') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="cancer"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_14"
                      />
                      <span data-language="medicalCondition_cancer">{{
                        $t('medicalCondition_cancer')
                      }}</span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="organ"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_15"
                      />
                      <span data-language="medicalCondition_organ">
                        {{ $t('medicalCondition_organ') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="hiv"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_16"
                      />
                      <span data-language="medicalCondition_hiv">
                        {{ $t('medicalCondition_hiv') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="longterm"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_17"
                        @click="medicalConditionOther"
                      />
                      <span data-language="medicalCondition_longterm">
                        {{ $t('medicalCondition_longterm') }}
                      </span>
                    </label>
                    <br />

                    <label>
                      <input
                        type="checkbox"
                        name="medical_condition_choice"
                        value="No"
                        v-model="medicalsChoices"
                        @change="medicalsChange"
                        id="id_medical_condition_choice_0"
                      />
                      <span data-language="medicalConditionNone">
                        {{ $t('medicalConditionNone') }}
                      </span>
                    </label>
                    <br />
                    <label
                      v-if="isShowOtherInput"
                      id="medical_condition_choice_other"
                    >
                      <span data-language="medicalCondition_other">
                        {{ $t('medicalCondition_other') }}
                      </span>
                      <input
                        type="text"
                        id="id_medical_condition_choice_other"
                        v-model="medicalOtherCondition"
                        name="medical_condition_choice"
                      />
                    </label>
                    <br />
                  </div>
                </div>
                <!--  Insomnia status choice field -->
                <div class="fieldWrapper">
                  <label for="insomnia_status_choice">
                    <h4 data-language="Q4addition">
                      {{ $t('Q4addition') }}
                    </h4>
                    <select
                      name="insomnia_status_choice"
                      v-model="insomniaChoices"
                      id="id_insomnia_status_choice"
                    >
                      <option
                        value="No"
                        data-language="insomnia_status_choice_never"
                      >
                        {{ $t('insomnia_status_choice_never') }}
                      </option>

                      <option
                        value="Onceper2Weeks"
                        data-language="insomnia_status_choice_Onceper2Weeks"
                      >
                        {{ $t('insomnia_status_choice_Onceper2Weeks') }}
                      </option>

                      <option
                        value="1"
                        data-language="insomnia_status_choice_OnceaWeek"
                      >
                        {{ $t('insomnia_status_choice_OnceaWeek') }}
                      </option>

                      <option
                        value="2to3"
                        data-language="insomnia_status_choice_2to3"
                      >
                        {{ $t('insomnia_status_choice_2to3') }}
                      </option>

                      <option
                        value="4+"
                        data-language="insomnia_status_choice_4"
                      >
                        {{ $t('insomnia_status_choice_4') }}
                      </option>
                    </select>
                  </label>
                </div>

                <!-- Smoke status choice field -->
                <div class="fieldWrapper">
                  <label for="id_smoke_status_choice">
                    <h4 data-language="Q4">
                      {{ $t('Q4') }}
                    </h4>

                    <select
                      name="smoke_status_choice"
                      v-model="smokeChoices"
                      id="id_smoke_status_choice"
                    >
                      <option
                        value="never"
                        data-language="smoke_status_choice_never"
                      >
                        {{ $t('smoke_status_choice_never') }}
                      </option>

                      <option value="ex" data-language="smoke_status_choice_ex">
                        {{ $t('smoke_status_choice_ex') }}
                      </option>

                      <option
                        value="ltOnce"
                        data-language="smoke_status_choice_ltOne"
                      >
                        {{ $t('smoke_status_choice_ltOne') }}
                      </option>

                      <option
                        value="1to10"
                        data-language="smoke_status_choice_1to10"
                      >
                        {{ $t('smoke_status_choice_1to10') }}
                      </option>

                      <option
                        value="11to20"
                        data-language="smoke_status_choice_11to20"
                      >
                        {{ $t('smoke_status_choice_11to20') }}
                      </option>

                      <option
                        value="21+"
                        data-language="smoke_status_choice_21"
                      >
                        {{ $t('smoke_status_choice_21') }}
                      </option>

                      <option
                        value="ecig"
                        data-language="smoke_status_choice_ecig"
                      >
                        {{ $t('smoke_status_choice_21') }}
                      </option>
                    </select>
                  </label>
                </div>
                <!-- covid19 status choice field -->
                <div class="fieldWrapper">
                  <label for="id_cov19_status_choice">
                    <h4 data-language="SymptomQ2">
                      {{ $t('SymptomQ2') }}
                    </h4>
                    <select
                      name="cov19_status_choice"
                      v-model="cov19Choices"
                      id="id_cov19_status_choice"
                    >
                      <option
                        value="never"
                        selected="selected"
                        data-language="cov19_status_choice_never"
                      >
                        {{ $t('cov19_status_choice_never') }}
                      </option>

                      <option
                        value="last14"
                        data-language="cov19_status_choice_last14"
                      >
                        {{ $t('cov19_status_choice_last14') }}
                      </option>

                      <option
                        value="over14"
                        data-language="cov19_status_choice_over14"
                      >
                        {{ $t('cov19_status_choice_over14') }}
                      </option>
                    </select>
                  </label>
                </div>

                <!-- Hospital status field -->
                <div class="fieldWrapper">
                  <label for="id_hospital_choice">
                    <h4 data-language="SymptomQ3">
                      {{ $t('SymptomQ3') }}
                    </h4>

                    <select
                      name="hospital_choice"
                      id="id_hospital_choice"
                      v-model="hospitalChoices"
                    >
                      <option value="No" data-language="hospital_choice_no">
                        {{ $t('hospital_choice_no') }}
                      </option>

                      <option value="Yes" data-language="hospital_choice_yes">
                        {{ $t('hospital_choice_yes') }}
                      </option>
                    </select>
                  </label>
                </div>
                <!-- Recordings -->
                <h3>{{ $t('record_sound_data') }}</h3>
                <!-- Record audio for breathing -->
                <div>
                  <br />
                  <p>
                    <i>
                      <span>{{ $t('guidance') }} </span>
                      <span>{{ $t('guidance2') }}</span>
                    </i>
                  </p>

                  <h4>{{ $t('SymptomQ4') }}</h4>
                  <img
                    class="mb-3"
                    src="static/imgs/tutorial1.png"
                    alt="tutorial breathe by nose"
                  />
                  <i
                    >{{ $t('SymptomQ42') }} <b>{{ $t('SymptomQ43') }}</b></i
                  >
                  <div id="breathe3Container">
                    <br />
                    <div>
                      <div id="controls1" class="mb-3">
                        <button
                          id="recordButton1"
                          @click="
                            processStart(
                              recordButton1,
                              stopButton1,
                              'recordingsList1'
                            )
                          "
                        >
                          <span data-language="Recordings">{{
                            $t('Recordings')
                          }}</span>
                        </button>
                        <button
                          id="stopButton1"
                          disabled=""
                          @click="
                            stopRecord(
                              recordButton1,
                              stopButton1,
                              'recordingsList1'
                            )
                          "
                        >
                          <span data-language="Stop">{{ $t('Stop') }}</span>
                        </button>
                        <time-box ref="time-box-1" />
                      </div>
                      <ol id="recordingsList1"></ol>
                      <audio-check-msg :valid="error1" :loading="loading1" />
                    </div>
                  </div>
                  <h5 id="notice_breathe_nose"></h5>
                  <!-- This should be populated by javascript, after the audio recording is done. -->

                  <input
                    type="hidden"
                    name="audio_data_cough"
                    id="id_audio_file_cough"
                  />
                </div>
                <!-- Record audio for cough reading -->
                <div>
                  <h4>{{ $t('SymptomQ5') }}</h4>
                  <img
                    class="mb-3"
                    src="static/imgs/tutorial2.png"
                    alt="tutorial breathe by nose"
                  />
                  <br />
                  <i
                    >{{ $t('SymptomQ52') }} <b>{{ $t('SymptomQ53') }}</b></i
                  >
                  <div id="breathContainer">
                    <br />
                    <div>
                      <div id="controls2" class="mb-3">
                        <button
                          id="recordButton2"
                          @click="
                            processStart(
                              recordButton2,
                              stopButton2,
                              'recordingsList2'
                            )
                          "
                        >
                          <span data-language="Recordings">{{
                            $t('Recordings')
                          }}</span>
                        </button>
                        <button
                          id="stopButton2"
                          disabled=""
                          @click="
                            stopRecord(
                              recordButton2,
                              stopButton2,
                              'recordingsList2'
                            )
                          "
                        >
                          <span data-language="Stop">{{ $t('Stop') }}</span>
                        </button>
                        <time-box ref="time-box-2" />
                      </div>
                      <ol id="recordingsList2"></ol>
                      <audio-check-msg :valid="error2" :loading="loading2" />
                    </div>
                  </div>
                  <h5 id="notice_breathe_mouth"></h5>
                  <!-- This should be populated by javascript, after the audio recording is done. -->

                  <input
                    type="hidden"
                    name="audio_data_breathe"
                    id="id_audio_file_breathe"
                  />
                </div>
                <!-- Record audio for text reading -->
                <div>
                  <h4 data-language="SymptomQ6">{{ $t('SymptomQ6') }}</h4>
                  <img
                    class="mb-3"
                    src="static/imgs/tutorial3.png"
                    alt="tutorial breathe by nose"
                  />
                  <br />
                  <i data-language="SymptomQ62"
                    >{{ $t('SymptomQ62') }} <b>{{ $t('SymptomQ63') }}</b></i
                  >
                  <div id="coughContainer">
                    <br />
                    <div>
                      <div id="controls3" class="mb-3">
                        <button
                          id="recordButton3"
                          @click="
                            processStart(
                              recordButton3,
                              stopButton3,
                              'recordingsList3'
                            )
                          "
                        >
                          <span data-language="Recordings">{{
                            $t('Recordings')
                          }}</span>
                        </button>
                        <button
                          id="stopButton3"
                          disabled=""
                          @click="
                            stopRecord(
                              recordButton3,
                              stopButton3,
                              'recordingsList3'
                            )
                          "
                        >
                          <span data-language="Stop">{{ $t('Stop') }}</span>
                        </button>
                        <time-box ref="time-box-3" />
                      </div>
                      <ol id="recordingsList3"></ol>
                      <audio-check-msg :valid="error3" :loading="loading3" />
                    </div>
                  </div>
                  <h5 id="notice_cough"></h5>
                  <!-- This should be populated by javascript, after the audio recording is done. -->

                  <input
                    type="hidden"
                    name="audio_data_read"
                    id="id_audio_file_read"
                  />
                  <input
                    type="hidden"
                    name="blob_test"
                    id="blob_test"
                    value=""
                  />
                </div>
                <br />
                <!-- Finally submit the form -->
                <button
                  class="mb-3"
                  type="submit"
                  name="button_submit"
                  value="Submit"
                  id="id_form_submit"
                  @click="submitData"
                  :disabled="disableSubmit || loading4"
                >
                  <span>{{ $t('submit') }}</span>
                </button>
                <div v-if="loading4">
                  <b-spinner variant="primary" label="Spinning" />
                  {{ $t('sending') }}
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </template>
  </main-layout>
</template>

<script>
import NavBar from './NavBar';
import MainLayout from './MainLayout';
import Header from './Header';
import UrlConstant from '../common/constant/url-constant';
import AudioCheckMsg from './common/AudioCheckingMessage';
import TimeBox from './child-components/TimeBox';
import AudioPredictionServices from '../services/audio-prediction-services';
import AudioCheckingServices from '../services/audio-checking-services';

export default {
  name: 'Home',
  components: {
    'nav-bar': NavBar,
    'main-layout': MainLayout,
    'main-header': Header,
    'audio-check-msg': AudioCheckMsg,
    'time-box': TimeBox,
  },
  data() {
    return {
      globalData: undefined,
      countryData: [],
      selectedCountry: 'Vietnam',
      selectedRegion: undefined,
      regionData: [],
      recordButton1: undefined,
      recordButton2: undefined,
      recordButton3: undefined,
      stopButton1: undefined,
      stopButton2: undefined,
      stopButton3: undefined,
      audioContext: undefined,
      gumStream: undefined,
      rec: undefined,
      input: undefined,
      sexChoices: 'Male',
      symptomsChoices: ['No'],
      medicalsChoices: ['No'],
      medicalOtherCondition: '', // Using when using select other medical condition
      insomniaChoices: 'No',
      smokeChoices: 'never',
      cov19Choices: 'never',
      hospitalChoices: 'No',
      isHaveMyFPTData: false, // Check user is redirected from MyFPT application
      data1: undefined, // Audio data
      data2: undefined, // Audio data
      data3: undefined, // Audio data
      error1: undefined, // Audio error
      error2: undefined, // Audio error
      error3: undefined, // Audio error
      loading1: false, // Check audio loading
      loading2: false, // Check audio loading
      loading3: false, // Check audio loading
      loading4: false, // Submit loading
      formError: undefined,
      currentRecord: undefined,
      disableSubmit: true,
      recordTime: 0,
      interval: undefined,
      borowedDeviceCb: undefined,
      devicetype: undefined,
      isShowOtherInput: false, // Show other input when user select other reason
    };
  },
  mounted() {
    this.init();
    this.loadParam();
    this.onSelectedCountry();
  },
  methods: {
    init() {
      this.emailTxt = document.getElementById('email');
      this.sexSb = document.getElementById('id_sex_choice');
      this.ageTxt = document.getElementById('id_age_choice');
      this.currentCityTxt = document.getElementById('id_current_city');
      this.recordButton1 = document.getElementById('recordButton1');
      this.recordButton2 = document.getElementById('recordButton2');
      this.recordButton3 = document.getElementById('recordButton3');
      this.stopButton1 = document.getElementById('stopButton1');
      this.stopButton2 = document.getElementById('stopButton2');
      this.stopButton3 = document.getElementById('stopButton3');

      this.globalData = require('../../static/country-data.json');
      this.globalData.forEach((item) => {
        this.countryData.push({
          value: item['countryName'],
          text: item['countryName'],
        });
      });
    },
    // Trigger when user selected new country
    onSelectedCountry() {
      this.globalData.forEach((item) => {
        if (item['countryName'] === this.selectedCountry) {
          this.selectedRegion = undefined;
          this.regionData = [];
          item.regions.forEach((rgItem) => {
            this.regionData.push({
              value: rgItem['name'],
              text: rgItem['name'],
            });
          });
        }
      });
    },
    // Trigger when user select other condition
    medicalConditionOther() {
      this.isShowOtherInput = !this.medicalsChoices.includes('longterm');
    },
    loadParam() {
      const url = new URL(window.location.href);
      const data = url.searchParams.get('data');
      if (data) {
        const jsonData = JSON.parse(atob(data));
        const keyData = Object.keys(jsonData);
        // Check MyFPT data
        if (keyData.includes('email')) {
          this.isHaveMyFPTData = true;
        }
        // Email
        if (keyData.includes('email') && jsonData['email']) {
          this.emailTxt.value = jsonData['email'];
        }
        // Gender
        if (keyData.includes('gender') && jsonData['gender']) {
          const gender = jsonData['gender'];
          switch (gender) {
            case 'M':
              this.sexSb.value = 'Male';
              break;
            case 'F':
              this.sexSb.value = 'Female';
              break;
            default:
              this.sexSb.value = 'Other';
          }
        }
        // Age
        if (keyData.includes('age') && jsonData['age']) {
          this.ageTxt.value = parseInt(jsonData['age']);
        }
        // Device type
        if (keyData.includes('devicetype') && jsonData['devicetype']) {
          this.devicetype = jsonData['devicetype'];
        }
      }
    },
    // Handle record button status
    handleRecord(isDisabled) {
      this.recordButton1.disabled = isDisabled;
      this.recordButton2.disabled = isDisabled;
      this.recordButton3.disabled = isDisabled;
    },
    uuidv4() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        let r = (Math.random() * 16) | 0;
        let v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      });
    },
    makeid(length) {
      var result = '';
      var characters =
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      var charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(
          Math.floor(Math.random() * charactersLength)
        );
      }
      return result;
    },
    submitData() {
      console.log(this.symptomsChoices);
      this.formError = {};
      const reEmail = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      const submitId = this.uuidv4();
      const submitTime = new Date().getTime();
      const sex = this.sexSb.value;
      const age = this.ageTxt.value;
      const borowedDevice = this.borowedDeviceCb;
      const currentCity = this.selectedRegion;
      let email = this.emailTxt.value;
      const redirectUrl = `${
        UrlConstant.BASE_URL
      }/results?submit_id=${submitId}&submit_time=${new Date().getTime()}`;
      let namebytime = new Date().toISOString();
      let filename1 = 'breathe_nose_' + namebytime;
      let filename2 = 'breathe_mouth_' + namebytime;
      let filename3 = 'cough_' + namebytime;

      // Validate age
      if (age === '' || age < 0 || age > 150) {
        this.formError['age'] = true;
      }

      // Validate medical
      if (
        this.medicalsChoices.length === 0 ||
        (this.medicalOtherCondition.length === 0 && this.isShowOtherInput)
      ) {
        this.formError['medical'] = true;
      }

      // Validate symptom
      if (this.symptomsChoices.length === 0) {
        this.formError['symptom'] = true;
      }

      // Validate email
      if (!reEmail.test(email) && !this.isHaveMyFPTData) {
        this.formError['email'] = true;
      }

      // Validate region
      if (currentCity === undefined || currentCity === '') {
        this.formError['region'] = true;
      }

      if (!this.isHaveMyFPTData) {
        email = email.toLowerCase();
      }

      if (Object.keys(this.formError).length > 0) {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
      } else {
        const fd = new FormData();

        if (this.data1) {
          fd.append('audio_data_breathe_nose', this.data1, filename1);
        }
        if (this.data2) {
          fd.append('audio_data_breathe_mouth', this.data2, filename2);
        }
        if (this.data3) {
          fd.append('audio_data_cough', this.data3, filename3);
        }

        fd.append('email', email);
        fd.append(
          'info',
          JSON.stringify({
            devicetype: this.devicetype,
            borowedDevice: borowedDevice,
            email: email,
            sex_choice: sex,
            age_choice: age,
            current_city: currentCity,
            symptoms_status_choice: this.symptomsChoices,
            medical_condition_choice: this.medicalsChoices,
            medical_condition_other_detail: this.medicalOtherCondition,
            insomnia_status_choice: this.insomniaChoices,
            smoke_status_choice: this.smokeChoices,
            cov19_status_choice: this.cov19Choices,
            hospital_choice: this.hospitalChoices,
            breathe_nose_noise: this.error1 ? this.error1.noise : '',
            breathe_mouth_noise: this.error2 ? this.error2.noise : '',
            cough_noise: this.error3 ? this.error3.noise : '',
          })
        );
        this.loading4 = true;
        AudioPredictionServices.audioPredictionVGG16V1(
          submitId,
          submitTime,
          fd,
          (resp) => {
            this.loading4 = false;
            window.location.replace(redirectUrl);
          },
          () => {
            this.loading4 = false;
          }
        );
      }
    },
    // Checking audio when user stop record
    checkingAudio(audio) {
      const fd = new FormData();
      fd.append('audio', audio);

      switch (this.currentRecord) {
        case 'recordingsList1':
          this.loading1 = true;
          break;
        case 'recordingsList2':
          this.loading2 = true;
          break;
        case 'recordingsList3':
          this.loading3 = true;
          break;
      }

      AudioCheckingServices.checkAudio(
        fd,
        (resp) => {
          var result = resp.data;

          switch (this.currentRecord) {
            case 'recordingsList1':
              this.error1 = result;
              this.loading1 = false;
              break;
            case 'recordingsList2':
              this.error2 = result;
              this.loading2 = false;
              break;
            case 'recordingsList3':
              this.error3 = result;
              this.loading3 = false;
              break;
          }
          this.checkSubmitCondition();
        },
        () => {
          this.loading1 = false;
          this.loading2 = false;
          this.loading3 = false;
        }
      );
    },
    processStart(recordButton, stopButton, currentRecord) {
      var constraints = {
        audio: true,
        video: false,
      };

      recordButton.disabled = true;
      stopButton.disabled = true;

      this.handleRecord(true);

      navigator.mediaDevices
        .getUserMedia(constraints)
        .then((stream) => {
          let AudioContext = window.AudioContext || window.webkitAudioContext; // Safari and old versions of Chrome
          this.audioContext = new AudioContext();

          // Update the format

          // Assign to gumStream for later use
          this.gumStream = stream;

          // use the stream
          this.input = this.audioContext.createMediaStreamSource(stream);

          // Create the Recorder object and configure to record mono sound (1 channel)
          // Recording 2 channels  will double the file size
          // eslint-disable-next-line
          this.rec = new Recorder(this.input, {
            numChannels: 1,
          });
          // Start the recording process
          this.rec.record();

          switch (currentRecord) {
            case 'recordingsList1':
              this.$refs['time-box-1'].start();
              break;
            case 'recordingsList2':
              this.$refs['time-box-2'].start();
              break;
            case 'recordingsList3':
              this.$refs['time-box-3'].start();
              break;
          }

          this.interval = setInterval(() => {
            this.recordTime += 1000;
            if (this.recordTime >= 10000) {
              stopButton.disabled = false;
            }

            if (this.recordTime >= 30000) {
              this.stopRecord(recordButton, stopButton, currentRecord);
              clearInterval(this.interval);
              this.recordTime = 0;
            }
          }, 1000);
        })
        .catch(() => {
          this.$notify({
            group: 'noti',
            type: 'error',
            title: 'Error!',
            text: 'Error occured',
          });
          // Enable the record button if getUserMedia() fails
          recordButton.disabled = false;
          stopButton.disabled = true;
          // Disable records process
          this.stopRecord(recordButton, stopButton, currentRecord);
          clearInterval(this.interval);
          this.recordTime = 0;
        });
    },
    stopRecord(recordButton, stopButton, currentRecord) {
      clearInterval(this.interval);
      // Disable the stop button, enable the record too allow for new recordings
      stopButton.disabled = true;
      recordButton.disabled = false;

      // Tell the recorder to stop the recording
      this.rec.stop();

      // Stop microphone access
      this.gumStream.getAudioTracks()[0].stop();
      this.currentRecord = currentRecord;

      // Create the wav blob and pass it on to createDownloadLink
      this.rec.exportWAV(this.createDownloadLink);
      this.recordTime = 0;
      this.handleRecord(false);
    },
    createDownloadLink(blob) {
      var url = URL.createObjectURL(blob);
      var au = document.createElement('audio');
      var li = document.createElement('li');
      var ol = document.getElementById(this.currentRecord);

      ol.innerHTML = '';

      // Add controls to the <audio> element
      au.controls = true;
      au.src = url;

      // Add the new audio element to li
      li.appendChild(au);

      // Add the li element to the ol
      ol.appendChild(li);

      switch (this.currentRecord) {
        case 'recordingsList1':
          this.data1 = blob;
          this.$refs['time-box-1'].stop();
          break;
        case 'recordingsList2':
          this.$refs['time-box-2'].stop();
          this.data2 = blob;
          break;
        case 'recordingsList3':
          this.$refs['time-box-3'].stop();
          this.data3 = blob;
          break;
      }
      this.checkingAudio(blob);
    },
    checkSubmitCondition() {
      if (this.error1 || this.error2 || this.error3) {
        const con1 =
          this.error1 && this.error1.duration && this.error1.count >= 3;
        const con2 =
          this.error2 && this.error2.duration && this.error2.count >= 3;
        const con3 =
          this.error3 && this.error3.duration && this.error3.count >= 3;
        this.disableSubmit = !(con1 || con2 || con3);
      } else {
        this.disableSubmit = true;
      }
    },
    // Handle symptoms change value
    symptomsChange() {
      setTimeout(() => {
        const arrLength = this.symptomsChoices.length;
        if (arrLength >= 1 && this.symptomsChoices[arrLength - 1] === 'No') {
          this.symptomsChoices = ['No'];
        } else {
          this.symptomsChoices = this.symptomsChoices.filter((e) => e !== 'No');
        }
      });
    },
    // Handle medical change value
    medicalsChange() {
      setTimeout(() => {
        const arrLength = this.medicalsChoices.length;
        if (arrLength >= 1 && this.medicalsChoices[arrLength - 1] === 'No') {
          this.medicalsChoices = ['No'];
          this.isShowOtherInput = false;
        } else {
          this.medicalsChoices = this.medicalsChoices.filter((e) => e !== 'No');
        }
      });
    },
  },
};
</script>

<style scoped>
h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: sans-serif;
}
h3 {
  margin-top: 36px;
  margin-bottom: 12px;
}
h4 {
  margin-top: 24px;
  margin-bottom: 4px;
}
.container-sm {
  max-width: 848px;
  overflow-wrap: break-word;
}
.main-session {
  z-index: 1;
}

.hero {
  position: relative;
  padding-top: 40px;
  padding-bottom: 40px;
}

section {
  padding: 60px 0;
  overflow: hidden;
}

img {
  height: auto;
  max-width: 100%;
  vertical-align: middle;
}

.newsletter .section-paragraph {
  margin-bottom: 32px;
  text-align: justify;
  text-justify: inter-word;
}

.newsletter .section-inner {
  padding-bottom: 64px;
}

.section-inner {
  position: relative;
}

.alert-info {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
}

.alert-info-custom {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}

.alert-custom {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
}

.alert-warning-custom {
  color: #856404;
  background-color: #fff3cd;
  border-color: #ffeeba;
}

.custom-select {
  max-width: 231px;
}

ol {
  padding-left: 0;
  list-style-type: none;
}

@media only screen and (min-width: 641px) {
  h1 {
    font-size: 42px;
    line-height: 52px;
    letter-spacing: -0.1px;
  }
  h3 {
    font-size: 30px;
    line-height: 40px;
    letter-spacing: -0.1px;
  }
  h4 {
    font-size: 20px;
    line-height: 30px;
    letter-spacing: -0.1px;
  }
  .site-header::before {
    top: -50%;
    left: 20%;
    width: 80%;
    height: 651px;
    background-size: 1480px 651px;
  }
  .hero {
    padding-top: 80px;
    padding-bottom: 120px;
  }
  .newsletter .section-paragraph {
    margin-bottom: 40px;
  }
  .section-inner {
    padding-bottom: 80px;
  }
}
</style>
