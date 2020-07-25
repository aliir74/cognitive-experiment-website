<template>
  <b-container class="bv-example-row">
    <b-row class="vh-100 text-center" align-v="center">
      <b-col></b-col>

      <b-col cols="8">
        <b-row class="vh-50">
          <b-col cols="2"></b-col>
          <b-col>
            <PersonalInformation msg="Welcome to my cognitive experiment" v-show="step == 0"/>
            <Explain msg="Welcome to my cognitive experiment" v-show="step == 1"/>
            <Decision msg="Welcome to my cognitive experiment" v-show="step == 2"/>
          </b-col>
          <b-col cols="2"></b-col>
        </b-row>
        <b-row class="vh-50">
          <b-col></b-col>
          <b-col>
            <b-button variant="success" v-on:click="step += 1">بعدی</b-button>
          </b-col>
          <b-col>
            <b-button variant="danger" v-on:click="step -= 1" :disabled="!(step <= 2 && step >= 1)">قبلی</b-button>
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
  components: {
    PersonalInformation,
    Explain,
    Decision
  },
  props: {
    step: {
      type: Number,
      default: 2
    }
  }
}
</script>

<style lang="scss">

</style>
