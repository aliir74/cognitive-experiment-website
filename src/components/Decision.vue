<template>
  <b-card img-right>
      <b-card-text>
        اگر فقط یکبار فرصت داشته باشین که پول رو تقسیم کنین، چه مقدار از پول رو به طرف مقابل می‌دین؟
      </b-card-text>
      <div>
      <b-input-group prepend="0" append="100">
        <b-form-input v-model="value" type="range" min="0" max="100"></b-form-input>
      </b-input-group>
      <p style="padding-left: 20px">{{value}}</p>

  </div>
    </b-card>
</template>

<script>
export default {
  data () {
    return {
      value: 50
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      alert(JSON.stringify(this.form))
    },
    onReset (evt) {
      evt.preventDefault()
      // Reset our form values
      this.form.email = ''
      this.form.name = ''
      this.form.food = null
      this.form.checked = []
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    }
  }
}
</script>

<style>
    .input-group-text {
        border-radius: 0 !important;
    }
</style>
