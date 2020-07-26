<template>
  <b-container class="bv-example-row">
    <b-row class="vh-100 text-center" align-v="center">
      <b-col></b-col>

      <b-col cols="8">
        <b-row class="vh-50" style="min-height: 50vh !important;">
          <b-col cols="2"></b-col>
          <b-col>
            <PersonalInformation :form.sync="person" v-show="step == 0"/>
            <Explain msg="Welcome to my cognitive experiment" v-show="step == 1"/>
            <Decision v-bind:msg="decision_msg" :value.sync="dictator_value" v-show="step == 2"/>
            <Decision v-for="(it, index) in god_numbers"
                      v-bind:msg="god_msg.replace('{0}', it).replace('{1}', god_value)"
                      :key="index" v-show="step == 3+index" :value.sync="value[index]"></Decision>
            <Decision v-for="(it, index) in god_numbers" :key="index"
                      v-bind:msg="again_god_msg.replace('{0}', it).replace('{1}', value[index])"
                      v-show="step == 3+god_numbers.length+index" v-bind:value="value[index]"
                      v-bind:show_progress="true" v-bind:show_money="true" v-bind:god_value="god_value"></Decision>
            <Judge v-for="(it, index) in god_numbers" :key="index"
                   v-bind:msg="judge_msg.replace('{0}', it)" v-show="step == 3+2*god_numbers.length+index"
                   v-bind:value="judge_value[index]"></Judge>
            <IRI v-show="step == 3+3*god_numbers.length" v-bind:msg="iri_msg" :value.sync="iri_value"></IRI>
          </b-col>
          <b-col cols="2"></b-col>
        </b-row>
        <b-row class="vh-50">
          <b-col></b-col>
          <b-col>
            <b-button variant="success" v-on:click="nextStep()" :disabled="nextButton()">بعدی</b-button>
          </b-col>
          <b-col>
            <b-button variant="danger" v-on:click="step -= 1" :disabled="false && !(step <= 2 && step >= 1)">قبلی</b-button>
          </b-col>
          <b-col></b-col>
        </b-row>
      </b-col>

      <b-col></b-col>
    </b-row>

  </b-container>
</template>

<script>
// @ is an alias to /src
import PersonalInformation from '@/components/PersonalInformation'
import Explain from '@/components/Explain'
import Decision from '@/components/Decision'
import Judge from '../components/Judge'
import IRI from '../components/IRI'
import $backend from '../backend'

export default {
  name: 'home',
  data () {
    return {
      decision_msg: '        اگر فقط یکبار فرصت داشته باشین که پول رو تقسیم کنین، چه مقدار از پول رو به طرف مقابل می‌دین؟',
      god_msg: 'حالا فرض کنین شما ناظر آزمایش قبل هستین و {1} هزار تومن پول در اختیار دارین. اگر نفر اول {0} هزار تومن به نفر دوم داده باشه شما به نفر اول چقدر پول میدین؟',
      again_god_msg: 'شما به کسی که {0} هزار تومن به نفر دوم داده بود {1} هزار تومن داده‌اید. در زیر میزان پول دو نفر را پس از تقسیم پول‌ها می‌بینید. اگر مایلید مقدار پول تقسیم کرده‌ی خود را عوض کنید.',
      judge_msg: 'فرض کنید نفر اول به نفر دوم {0} هزار تومن پول داده است. به میزان خودخواهی نفر اول از 0 تا 10 نمره دهید.',
      iri_msg: [' وقتی من داستان جالب، یا رمانی را می خوانم ، تصور می کنم که اگر حوادث داستان برای من اتفاق می افتاد چه احساسی داشتم .', '  من واقعا با احساسات شخصیت های رمان درگیر شدم.', ' وقتی من داستان جالب، یا رمانی را می خوانم ، تصور می کنم که اگر حوادث داستان برای من اتفاق می افتاد چه احساسی داشتم .', '  من واقعا با احساسات شخصیت های رمان درگیر شدم.', ' وقتی من داستان جالب، یا رمانی را می خوانم ، تصور می کنم که اگر حوادث داستان برای من اتفاق می افتاد چه احساسی داشتم .', '  من واقعا با احساسات شخصیت های رمان درگیر شدم.', ' وقتی من داستان جالب، یا رمانی را می خوانم ، تصور می کنم که اگر حوادث داستان برای من اتفاق می افتاد چه احساسی داشتم .', '  من واقعا با احساسات شخصیت های رمان درگیر شدم.'],
      god_numbers: [0, 10, 20, 30],
      value: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      judge_value: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
      god_value: 100,
      iri_value: new Array(8),
      dictator_value: 0,
      person: {
        'name': '',
        'email': '',
        'mobile': ''
      }
    }
  },
  components: {
    IRI,
    Judge,
    PersonalInformation,
    Explain,
    Decision
  },
  props: {
    step: {
      type: Number,
      default: 0
    }
  },
  methods: {
    nextButton: function () {
      if (this.step === 0) {
        return !((this.person.name.length !== 0) && (this.person.email.length !== 0) && (this.person.mobile.length !== 0))
      }
      return false
    },
    nextStep: function () {
      if (this.step === 0) {
        $backend.register({'person': this.person}).then(responseData => {
          this.god_numbers = responseData.result.god_numbers
          this.god_value = responseData.result.god_value
          this.step += 1
        }).catch(error => {
          alert(error.message)
        })
      } else {
        this.step += 1
      }
    }
  }
}
</script>

<style lang="scss">
  .card-body {
    min-height: 45vh !important;
    box-shadow: 1px 1px 2px white, 0 0 10px black, 0 0 3px white;
  }
</style>
