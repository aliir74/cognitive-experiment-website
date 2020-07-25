<template>
  <b-container class="bv-example-row">
    <b-row class="vh-100 text-center" align-v="center">
      <b-col></b-col>

      <b-col cols="8">
        <b-row class="vh-50">
          <PersonalInformation msg="Welcome to my cognitive experiment" v-show="step == 0"/>
          <HelloWorld msg="Welcome to my cognitive experiment" v-show="step == 1"/>
        </b-row>
        <b-row>
          <b-col>
            <b-button variant="success" v-on:click="step += 1">بعدی</b-button>
          </b-col>
          <b-col>
            <b-button variant="danger" v-show="step == 0">پاک کردن اطلاعات</b-button>
          </b-col>
        </b-row>
      </b-col>

      <b-col></b-col>
    </b-row>

  </b-container>
</template>

<script>
// @ is an alias to /src
import PersonalInformation from '@/components/PersonalInformation'
import HelloWorld from '@/components/HelloWorld'

export default {
  name: 'home',
  components: {
    PersonalInformation,
    HelloWorld
  },
  props: {
    step: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style lang="scss">

</style>
