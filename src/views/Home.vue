<template>
  <b-container class="bv-example-row">
    <b-row class="vh-100 text-center" align-v="center">
      <b-col></b-col>

      <b-col cols="8">
        <b-row class="vh-50" style="min-height: 50vh !important;">
          <b-col cols="2"></b-col>
          <b-col>
            <PersonalInformation msg="Welcome to my cognitive experiment" v-show="step == 0"/>
            <Explain msg="Welcome to my cognitive experiment" v-show="step == 1"/>
            <Decision v-bind:msg="decision_msg" v-show="step == 2"/>
            <Decision v-for="(it, index) in supervisor_numbers" v-bind:msg="supervisor_msg.replace('{0}', it)"
                      :key="index" v-show="step == 3+index" v-bind:supervisor="true"></Decision>
          </b-col>
          <b-col cols="2"></b-col>
        </b-row>
        <b-row class="vh-50">
          <b-col></b-col>
          <b-col>
            <b-button variant="success" v-on:click="step += 1">بعدی</b-button>
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

export default {
  name: 'home',
  data () {
    return {
      decision_msg: '        اگر فقط یکبار فرصت داشته باشین که پول رو تقسیم کنین، چه مقدار از پول رو به طرف مقابل می‌دین؟',
      supervisor_msg: 'حالا فرض کنین شما ناظر آزمایش قبل هستین و 100 هزار تومن پول در اختیار دارین. اگر نفر اول {0} هزار تومن به نفر دوم داده باشه شما به نفر اول چقدر پول میدین؟',
      supervisor_numbers: [30, 60, 100, 5]
    }
  },
  components: {
    PersonalInformation,
    Explain,
    Decision
  },
  props: {
    step: {
      type: Number,
      default: 3
    }
  },
  filters: {
    supervisor_msg_format: function (msg, money) {
      return msg.replace(money)
    }
  }
}
</script>

<style lang="scss">
  .card-body {
    min-height: 40vh !important;
  }
</style>
