<template>
  <b-container class="bv-example-row">
    <b-row class="vh-100 text-center" align-v="center">
      <b-col></b-col>
      <b-col>
        <PersonalInformation msg="Welcome to my cognitive experiment"/>
      </b-col>
      <b-col></b-col>
    </b-row>
  </b-container>
</template>

<script>
// @ is an alias to /src
import PersonalInformation from '@/components/PersonalInformation'

export default {
  name: 'home',
  components: {
    PersonalInformation
  }
}
</script>

<style lang="scss">

</style>
