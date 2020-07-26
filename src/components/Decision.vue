<template>
    <b-card img-right>
        <b-card-text>
            {{ msg }}
        </b-card-text>
        <div>
            <b-input-group prepend="0" append="100" v-if="show_progress">
                <b-form-input v-model="value" type="range" min="0" max="100"
                              @keyup="$emit('update:value', value);"></b-form-input>
            </b-input-group>
            <p style="padding-left: 20px" v-if="show_progress">{{value}}</p>
            <b-input-group style="width: 70px; margin: auto" v-if="!show_progress">
                <b-form-input type="number" v-model="value"
                              @keyup="$emit('update:value', value);"></b-form-input>
            </b-input-group>
        </div>
        <b-card-text v-if="show_money">
            پول نفر اول: {{value}}
        </b-card-text>
        <b-card-text v-if="show_money">
            پول نفر دوم: {{god_value-value}}
        </b-card-text>
    </b-card>
</template>

<script>
export default {
  props: {
    msg: String,
    god: {
      type: Boolean,
      default: false
    },
    god_value: Number,
    show_money: {
      type: Boolean,
      default: false
    },
    show_progress: {
      type: Boolean,
      default: false
    },
    value: {
      type: Number,
      default: 0
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
