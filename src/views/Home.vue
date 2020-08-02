<template>
  <b-container class="bv-example-row">

    <b-row class="vh-100 text-center" align-v="center">
      <b-col>

      </b-col>

      <b-col cols="12">
        <b-row  class="vh-70" style="min-height: 70vh !important; margin-top: 20px;">
          <b-col cols="1"></b-col>
          <b-col style="position:absolute; z-index: 10; min-height: 70vh;" v-show="spinner" >
            <div style="min-height: 100vh;" class="text-center" align-v="center">
              <b-spinner style="margin: 50vh !important;" type="grow" label="Loading..."></b-spinner>
            </div>
          </b-col>
          <b-col>
            <b-modal id="modal-1" title="راهنما" hide-footer hide-header>
              <Explain v-bind:msg="explain_msg.replace('{0}', god_value)"/>
              <b-button class="mt-3 btn-success" block @click="$bvModal.hide('modal-1')">متوجه شدم</b-button>
            </b-modal>
            <PersonalInformation :form.sync="person" v-show="step == 0"/>

            <Explain v-bind:msg="explain_msg.replace('{0}', god_value)" v-show="step == 1"/>

            <Decision v-bind:msg="decision_msg" :value.sync="dictator_value" v-show="step == 2"/>

            <Decision v-for="(it, index) in god_numbers"
                      v-bind:msg="god_msg.replace('{0}', it).replace('{1}', god_value)"
                      :key="'first-deci'+index.toString()" v-show="step == 3+index" :value.sync="value[index]"></Decision>

            <Decision v-for="(it, index) in god_numbers" :key="'second-deci'+index.toString()"
                      v-bind:msg="again_god_msg.replace('{0}', it).replace('{1}', value[index])"
                      v-show="step == 3+god_numbers.length+index" :value.sync="after_change_value[index]"
                      v-bind:show_progress="true" v-bind:show_money="true" v-bind:god_value="god_value" :god_number="it"></Decision>

            <Judge v-for="(it, index) in god_numbers" :key="'judge'+index.toString()"
                   v-bind:msg="judge_msg.replace('{0}', it)" v-show="step == 3+2*god_numbers.length+index"
                   :value.sync="judge_value[index]"></Judge>

            <IRI v-show="step == 3+3*god_numbers.length" v-bind:msg="iri_msg" :value.sync="iri_value"></IRI>
            <Explain :show_image="false" :msg="thankyou_msg" v-show="step === 4+3*god_numbers.length"></Explain>
          </b-col>
          <b-col cols="1"></b-col>
        </b-row>
        <b-row class="vh-50" style="margin: 20px;">
          <b-col></b-col>
          <b-col>
            <b-button variant="success" v-on:click="nextStep()" :disabled="disableNextButton()"
                      v-if="this.step <= 3+3*this.god_numbers.length">{{next_text}}</b-button>
          </b-col>
          <b-col>
            <b-button v-b-modal.modal-1 @click="help += 1" class="btn-info" v-if="step >= 0">راهنما</b-button>
          </b-col>
          <b-col>
            <b-button variant="danger" v-on:click="step -= 1" :disabled="disablePrevButton()"
                      v-if="this.step <= 3+3*this.god_numbers.length">قبلی</b-button>
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
      spinner: false,
      explain_msg: 'فرض کنید که شما 100 هزار تومن پول دارین و قراره اون رو با یه نفر دیگه تقسیم کنین. شما هر قدر که دوست داشته باشین می‌تونین پول رو برای خودتون نگه دارین و باقی رو به نفر دیگه بدین.\nیه نفر دیگه هم تو جمع ما وجود داره که بهش می‌گیم ناظر. ناظر {0} هزار تومن پول داره که بعد از تقسیم کردن پول توسط شما، پول خودش رو بین شما و نفر دیگه تقسیم می‌کنه و شما اطلاعاتی در مورد تصمیم‌های قبلیش ندارین. بنابراین همون‌طور که در شکل مشاهده می‌کنید سه نفر در این آزمایش حضور دارن و شما شخص اول هستین و مقداری از پولتون رو به شخص دوم می‌دین.',
      decision_msg: '        اگر فقط یکبار فرصت داشته باشین که پول رو تقسیم کنین، چه مقدار از پول رو به طرف مقابل می‌دین؟ (از 0 تا  100 هزار تومن)',
      god_msg: 'حالا فرض کنین شما ناظر آزمایش قبل هستین و {1} هزار تومن پول در اختیار دارین. اگر نفر اول {0} هزار تومن به نفر دوم داده باشه شما به نفر اول چقدر پول میدین؟',
      again_god_msg: 'شما به کسی که {0} هزار تومن به نفر دوم داده بود {1} هزار تومن داده‌اید. در زیر میزان پول دو نفر را پس از تقسیم پول‌ها می‌بینید. اگر مایلید مقدار پول تقسیم کرده‌ی خود را عوض کنید.',
      judge_msg: 'فرض کنید نفر اول به نفر دوم {0} هزار تومن پول داده است. به میزان خودخواهی نفر اول از -5 تا 5 نمره دهید.',
      iri_msg: ['وقتی من داستان جالب، یا رمانی را می خوانم ، تصور می کنم که اگر حوادث داستان برای من اتفاق می افتاد چه احساسی داشتم.',
        'من واقعا با احساسات شخصیت های رمان درگیر شدم.',
        'من معمولا در موقع تماشای یک فیلم یا بازی بی طرف هستم',
        'بعد از دیدن یک بازی یا فیلم، من احساس می کنم مثل این که ، من یکی از شخصیت ها بودم.',
        'من با نظم خاصی درباره چیزهایی که ممکن است برایم اتفاق افتذ، خیال پردازی می کنم.',
        'برای من به ندرت پیش می آید که به شدت درگیر یک فیلم یا کتاب خوب شوم.',
        'وقتی من یک فیلم خوب می بینم ، به راحتی می توانم خود را به جای نقش اول فیلم بگذارم.',
        'قبل از انتقاد کردن از کسی ، سعی می کنم تصور کنم اگر جای آن ها بودم چه احساسی داشتم.',
        'اگر مطمئن باشم که حق با من است، وقتم را تلف نمی کنم که به جرّ و بحث های دیگران گوش کنم.',
        'من بعضی وقت ها سعی می کنم از دید دوستانم به امور نگاه کنم، تا آن ها را بهتر بفهمم.',
        'من معتقدم که برای هر سوال دو جنبه وجود دارد و سعی می کنم به هر دو جنبه نگاه کنم.',
        'من بعضی وقت ها پی می برم که دیدن چیزها از نقطه نظر دیگران مشکل است.',
        'قبل از آین که تصمیم بگیرم ، سعی می کنم به جنبه ناسازگاری هر کس نگاه کنم.',
        'وقتی من از کسی ناراحتمف معمولا سعی می کنم خود را چند لحظه جای او بگذارم.',
        'وقتی می بینم کسی مورد سوء استفاده قرار می گیرد، احساس می کنم باید از او حمایت کنم.',
        'گاهی اوقات می بینم کسی نادرست رفتار می کند، نسبت به او احساس همدردی و تاسف ندارم.',
        'من اغلب برای افرادی که کمتر از من خوشبخت هستند، احساس محبت و نگرانی دارم.',
        'من خودم را یک شخص نازک دل می دانم.',
        'گاهی برای افرادی که مشکل دارند، احساس تاسف نمی کنم.',
        'مردم بیچاره و بدبخت معمولا مرا خیلی آشفته و مضطرب نمی کنند.',
        'من اغلب از چیزهایی که می بینم اتفاق می افتذ کاملا متاثر می شوم.'],
      thankyou_msg: 'ممنون از وقتی که برای انجام آزمایش ما گذاشتی :)',
      god_numbers: [0],
      value: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      after_change_value: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      judge_value: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      god_value: 95,
      iri_value: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
      dictator_value: 0,
      person: {
        'name': '',
        'email': '',
        'mobile': '',
        'age': 0,
        'sex': ''
      },
      help: 0,
      step: 0,
      step_time: [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
      next_text: 'بعدی',
      email_reg: /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
    }
  },
  components: {
    IRI,
    Judge,
    PersonalInformation,
    Explain,
    Decision
  },
  methods: {
    disablePrevButton: function () {
      if (this.step === 0 || this.step === 1 || this.step === 3 || this.step === 3 + this.god_numbers.length ||
              this.step === 3 + 2 * this.god_numbers.length || this.step === 3 + 3 * this.god_numbers.length) {
        return true
      }
      return false
    },
    disableNextButton: function () {
      if (this.step === 0) {
        return !this.checkFormValidity()
      }
      if (this.step === 2) {
        // if (this.dictator_value === '') {
        //   return true
        // }
        return !(this.dictator_value >= 0 && this.dictator_value <= 100)
      }
      if (this.step >= 3 && this.step <= 3 + this.god_numbers.length - 1) {
        let valueIndex = this.step - 3
        // if (this.value[valueIndex] === '') {
        //   return true
        // }
        return !(this.value[valueIndex] >= 0 && this.value[valueIndex] <= this.god_value)
      }
      // if (this.step === 3 + 3 * this.god_numbers.length) {
      //   for (let i; i <= this.iri_value.length; i++) {
      //     if (this.iri_value[i] === undefined) {
      //       return true
      //     }
      //   }
      // }
      return false
    },
    sleep: function (ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    prevStep: async function () {
      this.spinner = true
      await this.sleep(1000)
      this.spinner = false
      this.step -= 1
    },
    nextStep: async function () {
      this.spinner = true
      await this.sleep(1000)
      if (this.step_time[this.step] === -1) {
        this.step_time[this.step] = new Date().getTime()
      }

      if (this.step === 0) {
        $backend.register({'person': this.person}).then(responseData => {
          this.god_numbers = responseData.result.god_numbers
          this.god_value = responseData.result.god_value
          this.step += 1
        }).catch(error => {
          if (error.response.status === 409) {
            alert('شما قبلا در این آزمایش شرکت کرده‌اید!')
          } else {
            alert(error.message)
          }
        })
      } else if (this.step === 2 + this.god_numbers.length) {
        this.after_change_value = [...this.value]
        this.step += 1
      } else if (this.step === 2 + 3 * this.god_numbers.length) {
        this.next_text = 'ارسال جواب‌ها'
        this.step += 1
      } else if (this.step === 3 + 3 * this.god_numbers.length) {
        $backend.submit({'value': this.value,
          'after_change_value': this.after_change_value,
          'iri_value': this.iri_value,
          'judge_value': this.judge_value,
          'dictator_value': this.dictator_value,
          'email': this.person.email,
          'mobile': this.person.mobile,
          'name': this.person.name,
          'step_time': this.step_time,
          'help': this.help})
          .then(responseData => {
            this.step += 1
          })
          .catch(error => {
            alert(error.message)
          })
      } else {
        this.step += 1
      }
      this.spinner = false
    },
    checkFormValidity: function () {
      if (!this.email_reg.test(this.person.email)) {
        return false
      }
      return ((this.person.name !== '') && (this.person.email !== '') && (this.person.mobile !== '') &&
          (!isNaN(this.person.mobile)) && (this.person.age !== '') && (this.person.age > 0) && (this.person.sex !== ''))
    }
  }
}
</script>

<style lang="scss">
  .card-body {
    min-height: 45vh !important;
    box-shadow: 1px 1px 2px white, 0 0 10px black, 0 0 3px white;
  }
  .modal-dialog {
    max-width: 50vw !important;
  }
</style>
