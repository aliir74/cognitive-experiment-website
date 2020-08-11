<template>
  <b-container>
    <b-row style="position:absolute; z-index: 10; right: 50%; top: 50%;" v-show="spinner" >
            <div class="text-center" align-v="center">
              <b-spinner style="margin: auto;" type="grow" label="Loading..."></b-spinner>
            </div>
    </b-row>
    <b-row class="vh-100 text-center" align-v="center">
      <b-col class="col-md-12 col-sm-12" >
        <b-row  class="vh-70" style="min-height: 70vh !important; margin-top: 20px;">
          <b-col>
            <b-modal id="modal-1" title="راهنما" hide-footer hide-header>
              <Explain :god_value="god_value" v-bind:msg="help_msg.replace('{0}', god_value)" dir="rtl"/>
              <b-button class="mt-3 btn-success" block @click="$bvModal.hide('modal-1')">متوجه شدم</b-button>
            </b-modal>
            <PersonalInformation :form.sync="person" v-show="step == 0 && !spinner"/>

            <Explain :god_value="god_value" v-bind:msg="explain_msg.replace('{0}', god_value)" v-show="step == 1 && !spinner"/>

            <Decision v-bind:msg="decision_msg" :value.sync="dictator_value" :god_value="100" v-show="step == 2 && !spinner"/>

            <Decision v-for="(it, index) in god_numbers"
                      v-bind:msg="god_msg.replace('{0}', it).replace('{1}', god_value)"
                      :key="'first-deci'+index.toString()" v-show="step == 3+index && !spinner" :value.sync="value[index]"></Decision>

            <Decision v-for="(it, index) in god_numbers" :key="'second-deci'+index.toString()"
                      v-bind:msg="again_god_msg.replace('{0}', it).replace('{1}', value[index])"
                      v-show="step == 3+god_numbers.length+index && !spinner" :value.sync="after_change_value[index]"
                      v-bind:show_progress="true" v-bind:show_money="true" v-bind:god_value="god_value" :god_number="it"></Decision>

            <Judge v-for="(it, index) in god_numbers" :key="'judge'+index.toString()"
                   v-bind:msg="judge_msg.replace('{0}', it)" v-show="step == 3+2*god_numbers.length+index && !spinner"
                   :value.sync="judge_value[index]"></Judge>
            <Decision v-bind:msg="dictator_again_msg.replace('{0}', dictator_value)" :value.sync="dictator_again"
                      :god_value="100" v-show="step == 3+3*god_numbers.length && !spinner" :show_progress="true"/>
            <IRI v-show="step == 4+3*god_numbers.length && !spinner" v-bind:msg="iri_msg" :value.sync="iri_value"></IRI>
            <Explain :show_image="false" :msg="thankyou_msg" v-show="step === 5+3*god_numbers.length"></Explain>
          </b-col>
        </b-row>
        <b-row style="margin: 20px;">
          <b-col style="margin: auto" v-show="step > 1 && step <= 3+3*god_numbers.length">
             <b-form-checkbox v-model="not_change">مقدار پیش‌فرض را تغییر نمی‌دهم.</b-form-checkbox>
          </b-col>
          <b-col></b-col>
          <b-col></b-col>
        </b-row>
        <b-row class="vh-50" style="margin: 20px;">
          <b-col>
            <b-button variant="success" v-on:click="nextStep()" :disabled="disableNextButton()"
                      v-if="this.step <= 4+3*this.god_numbers.length">{{next_text}}</b-button>
          </b-col>
          <b-col>
            <b-button v-b-modal.modal-1 @click="help += 1" class="btn-info"
                      v-if="step >= 2 && step < 4+3*this.god_numbers.length">راهنما</b-button>
          </b-col>
          <b-col>
            <b-button variant="danger" v-on:click="prevStep()" :disabled="disablePrevButton()"
                      v-if="this.step <= 4+3*this.god_numbers.length">قبلی</b-button>
          </b-col>
        </b-row>
      </b-col>
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
      explain_msg: 'فرض کنید که شما <span class="numbers">100 هزار تومن</span> پول دارید و قراره اون رو با یه نفر دیگه تقسیم کنید. شما هر قدر که دوست داشته باشید می‌تونید پول رو برای خودتون نگه دارید و باقی رو به نفر دیگه بدید.<br>یه نفر دیگه هم تو جمع ما وجود داره که بهش می‌گیم ناظر. ناظر <span class="numbers">{0} هزار تومن</span> پول داره که بعد از تقسیم کردن پول توسط شما، پول خودش رو بین شما و نفر دیگه تقسیم می‌کنه و شما اطلاعاتی در مورد تصمیم‌های قبلیش ندارید. بنابراین همون‌طور که در شکل مشاهده می‌کنید سه نفر در این آزمایش حضور دارن و شما شخص اول هستید و مقداری از پولتون رو به شخص دوم می‌دید.<br>سعی کنید در تمامی مراحل آزمایش، خودتون رو در اون موقعیت تصور کنید و با توجه به این‌که انگار پول واقعی دارید تصمیم‌گیری رو انجام بدید.',
      explain_msg_god: 'فرض کنید که نفر اول <span class="numbers">100 هزار تومن</span> پول دارد و قراره اون رو با نفر دوم تقسیم کند. <br> شما هم به عنوان ناظر در این جمع وجود دارید. ناظر <span class="numbers">{0} هزار تومن</span> پول داره که بعد از تقسیم کردن پول توسط نفر اول پول خودش رو بین نفر اول و نفر دوم تقسیم می‌کنه . بنابراین همون‌طور که در شکل مشاهده می‌کنید سه نفر در این آزمایش حضور دارن و شما ناظر هستید و قراره پولتون رو بین دو نفر تقسیم کنید.<br>سعی کنید در تمامی مراحل آزمایش، خودتون رو در اون موقعیت تصور کنید و با توجه به این‌که انگار پول واقعی دارید تصمیم‌گیری رو انجام بدید.',
      help_msg: 'فرض کنید که شما <span class="numbers">100 هزار تومن</span> پول دارید و قراره اون رو با یه نفر دیگه تقسیم کنید. شما هر قدر که دوست داشته باشید می‌تونید پول رو برای خودتون نگه دارید و باقی رو به نفر دیگه بدید.<br>یه نفر دیگه هم تو جمع ما وجود داره که بهش می‌گیم ناظر. ناظر <span class="numbers">{0} هزار تومن</span> پول داره که بعد از تقسیم کردن پول توسط شما، پول خودش رو بین شما و نفر دیگه تقسیم می‌کنه و شما اطلاعاتی در مورد تصمیم‌های قبلیش ندارید. بنابراین همون‌طور که در شکل مشاهده می‌کنید سه نفر در این آزمایش حضور دارن و شما شخص اول هستید و مقداری از پولتون رو به شخص دوم می‌دید.',
      decision_msg: '        اگر فقط یکبار فرصت داشته باشید که پول رو تقسیم کنید، چه مقدار از پول رو به طرف مقابل می‌دید؟ (از 0 تا  100 هزار تومن)',
      god_msg: 'حالا فرض کنید شما ناظر آزمایش قبل هستید و <span class="numbers">{1} هزار تومن</span> پول در اختیار دارید. اگر نفر اول <span class="numbers">{0} هزار تومن</span> به نفر دوم داده باشه شما به نفر اول چقدر پول میدید؟',
      again_god_msg: 'شما به کسی که <span class="numbers">{0} هزار تومن</span> به نفر دوم داده بود <span class="numbers">{1} هزار تومن</span> داده‌اید. در زیر میزان پول دو نفر را پس از تقسیم پول‌ها می‌بینید. اگر مایلید مقدار پول تقسیم کرده‌ی خود را عوض کنید.',
      judge_msg: 'فرض کنید نفر اول به نفر دوم <span class="numbers">{0} هزار تومن</span> پول داده است. در محور خودخواهی تا دگرخواهی این فرد را در کجا قرار می‌دهید؟ (از -5 تا 5)',
      dictator_again_msg: 'شما وقتی در جایگاه نفر اول بودید <span class="numbers">{0} هزار تومن</span> به نفر دوم دادید. آیا می‌خواهید تصمیم خود را عوض کنید؟',
      iri_msg: ['تقریبا به طور معمول درباره‌ی اتفاقاتی که ممکن است برایم رخ دهد، خیال‌پردازی و خیال‌بافی می‌کنم.',
        'اغلب نسبت به افرادی که کمتر از من خوشبخت هستند احساس دلسوزی و نگرانی می‌کنم.',
        'گاهی دیدن مسائل از نقطه‌نظر فردی دیگر برایم دشوار است.',
        'زمانی که دیگران دچار مشکلاتی هستند احساس تاسف زیادی برایشان نمی‌کنم.',
        'وقتی یک کتاب داستان می‌خوانم به شدت درگیر احساسات شخصیت‌های آن می‌شوم.',
        'در مواقع بحرانی، احساس نگرانی و ناراحتی می‌کنم.',
        'معمولا به هنگام تماشای یک بازی یا فیلم، بی‌طرف هستم و اغلب زیاد درگیر آن نمی‌شوم.',
        'سعی می‌کنم قبل از تصمیم‌گیری دیدگاه‌های مخالف را نیز بررسی می‌کنم.',
        'اگر کسی را در حال سواستفاده شدن ببینم، حالت حمایت از وی پیدا می‌کنم.',
        'گاهی اوقات که در یک موقعیت دشوار عاطفی قرار می‌گیرم، احساس درماندگی می‌کنم.',
        'گاهی برای درک بهتر دوستانم، سعی می‌کنم حدس بزنم که مسائل از دیدگاه آن‌ها چگونه است.',
        'تا حدودی بعید است که خیلی درگیر یک کتاب یا فیلم خوب شوم.',
        'وقتی رنجش کسی را می‌بینم، ترجیح می‌دهم آرامش خودم را حفظ کنم.',
        'مصیبت‌های دیگران معمولا خیلی ناراحتم نمی‌کند.',
        'اگر مطمئن باشم در مورد چیزی حق با من است، زمان زیادی را برای شنیدن دلایل دیگران صرف نمی‌کنم.',
        'پس از دیدن یک فیلم یا بازی، احساس می‌کنم که انگار یکی از شخصیت‌های آن هستم.',
        'از بودن در یک وضعیت عاطفی متشنج می‌ترسم.',
        'گاهی اوقات که می‌بینم با شخصی ناعادلانه رفتار می‌شود، خیلی برایش تاسف نمی‌خورم.',
        'معمولا در موقعیت‌های اضطراری و اورژانسی مسلط و کارآمد هستم.',
        'اغلب با چیزهایی که می‌بینم اتفاق می‌افتد، متاثر می‌شوم.',
        'معتقدم که برای هر مسئله‌ای دو جنبه وجود دارد و من سعی می‌کنم که به هر دو آن‌ها توجه کنم.',
        'من خودم را شخصی بسیار رئوف و خوش‌قلب می‌دانم.',
        'هنگامی که یک فیلم خوب را تماشا می‌کنم، به راحتی می‌توانم خودم را به جای شخصیت اصلی بگذارم.',
        'من مستعد از دست دادن کنترلم در مواقع اضطراری هستم.',
        'وقتی از کسی دلخور می‌شوم، لحظه‌ای "خودم را به جای او می‌گذارم"',
        'زمانی که یک داستان یا رمان جالب را می‌خوانم، فرض می‌کنم در صورتی که وقایع داستان برای من اتفاق می‌افتاد چه احساسی پیدا می‌کردم.',
        'وقتی کسی را در یک موقعیت بحرانی می‌بینم که نیاز به کمک دارد، ناتوان می‌شوم.',
        'قبل از اینکه از کسی انتقاد کنم، سعی می‌کنم تصور کنم که اگر جای او بودم چه احساسی داشتم.'],
      thankyou_msg: 'ممنون از وقتی که برای انجام آزمایش ما گذاشتی :)',
      god_numbers: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      value: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      after_change_value: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      judge_value: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      god_value: 200,
      iri_value: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
      dictator_value: 0,
      dictator_again: 0,
      person: {
        'name': '',
        'email': '',
        'mobile': '',
        'age': 0,
        'sex': ''
      },
      step_presence: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      step_change: [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false,
        false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      step_sequence: [0],
      help: 0,
      step: 1,
      first_after_value_13: false,
      not_change: false,
      step_time: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
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
  watch: {
    step: function (newStep, oldStep) {
      console.log(this.value)
      console.log(this.after_change_value)
      this.step_change[oldStep] = true
      // console.log('step', this.step)
      this.step_time[this.step].push(new Date().getTime())
      this.step_presence[this.step] += 1
      this.step_sequence.push(this.step)
      this.not_change = false
      if (this.step >= 3 && this.step < 3 + 3 * this.god_numbers.length) {
        this.help_msg = this.explain_msg_god
      } else {
        this.help_msg = this.explain_msg
      }
      if (newStep > oldStep) {
        this.step_change[newStep] = false
      }
    },
    dictator_value: function () {
      this.step_change[2] = true
    },
    dictator_again: function () {
      this.step_change[3 + 3 * this.god_numbers.length] = true
    },
    value: {
      deep: true,
      handler: function () {
        // console.log('value')
        if (this.step < 3 + this.god_numbers.length && this.step > 2) {
          this.step_change[this.step] = true
        }
      }
    },
    after_change_value: {
      deep: true,
      immediate: true,
      handler: function () {
        // console.log('after value', this.step)
        if (this.step < 3 + 2 * this.god_numbers.length && this.step > 2 + this.god_numbers.length) {
          if (this.step === 13 && this.first_after_value_13 === false) { // when we become to after_change state,
            // all value copied to after_value_change and this cause detect fake step_change on step 13
            this.first_after_value_13 = true
          } else {
            this.step_change[this.step] = true
          }
        }
      }
    },
    judge_value: {
      deep: true,
      handler: function () {
        // console.log('judge value')
        if (this.step < 3 + 3 * this.god_numbers.length && this.step > 2 + 2 * this.god_numbers.length) {
          this.step_change[this.step] = true
        }
      }
    }
  },
  methods: {
    detectMob: function () {
      const toMatch = [
        /Android/i,
        /webOS/i,
        /iPhone/i,
        /iPad/i,
        /iPod/i,
        /BlackBerry/i,
        /Windows Phone/i
      ]

      return toMatch.some((toMatchItem) => {
        return navigator.userAgent.match(toMatchItem)
      })
    },
    disablePrevButton: function () {
      if (this.step === 0 || this.step === 1 || this.step === 3 || this.step === 3 + this.god_numbers.length ||
              this.step === 3 + 2 * this.god_numbers.length || this.step === 3 + 3 * this.god_numbers.length ||
              this.step === 4 + 3 * this.god_numbers.length) {
        return true
      }
      return false
    },
    disableNextButton: function () {
      if (this.step >= 2 && this.step <= 3 + 3 * this.god_numbers.length) { // Must check `dont want to change`
        console.log('step disable', this.step)
        console.log('step change in disable', this.step_change)
        console.log(this.step_change[this.step])
        console.log(this.not_change)
        if (this.step_change[this.step] !== true && this.not_change === false) {
          return true
        }
      }
      if ((this.dictator_value === '') || (this.value.indexOf('') !== -1) ||
          (this.judge_value.indexOf('') !== -1) || (this.after_change_value.indexOf('') !== -1) ||
          this.dictator_again === '') {
        return true
      }
      if (this.step === 0) {
        return !this.checkFormValidity()
      }
      if (this.step === 2) {
        return !(this.dictator_value >= 0 && this.dictator_value <= 100)
      }
      if (this.step >= 3 && this.step <= 3 + this.god_numbers.length - 1) {
        let valueIndex = this.step - 3
        // if (this.value[valueIndex] === '') {
        //   return true
        // }
        return !(this.value[valueIndex] >= 0 && this.value[valueIndex] <= this.god_value)
      }
      if (this.step === 4 + 3 * this.god_numbers.length) {
        for (let i = 0; i <= this.iri_value.length; i++) {
          if (this.iri_value[i] === '') {
            return true
          }
        }
      }
      return false
    },
    sleep: function (ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    sendData: function () {
      return {'value': this.value,
        'after_change_value': this.after_change_value,
        'iri_value': this.iri_value,
        'judge_value': this.judge_value,
        'dictator_value': this.dictator_value,
        'dictator_again': this.dictator_again,
        'email': this.person.email,
        'mobile': this.person.mobile,
        'name': this.person.name,
        'step_time': this.step_time,
        'help': this.help,
        'complete': true,
        'step_presence': this.step_presence,
        'step_sequence': this.step_sequence,
        'is_mobile': this.detectMob(),
        'send_time': (new Date().getTime()),
        'step_change': this.step_change}
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
      } else if (this.step === 2) {
        this.dictator_again = this.dictator_value
        this.step += 1
      } else if (this.step === 2 + this.god_numbers.length) {
        this.after_change_value = [...this.value]
        this.step += 1
      } else if (this.step === 3 + 3 * this.god_numbers.length) {
        this.next_text = 'ارسال جواب‌ها'
        $backend.submit(this.sendData())
          .then(responseData => {
            this.step += 1
          })
          .catch(error => {
            alert(error.message)
          })
      } else if (this.step === 4 + 3 * this.god_numbers.length) {
        $backend.submit(this.sendData())
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
  .numbers {
    //color: green;
    font-weight: bold;
  }
  .modal-dialog {
    //max-width: 80vw !important;
    margin: auto !important;
  }
</style>
