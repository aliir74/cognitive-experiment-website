<template>
    <b-card img-right>
        <b-card-text v-html="msg">
        </b-card-text>
        <div>
            <b-input-group dir="ltr" prepend="0" :append="god_value.toString()" v-if="show_progress">
                <b-form-input v-model.number="value" type="range" min="0" :max="god_value"
                              @input="$emit('update:value', value);"></b-form-input>
            </b-input-group>

            <b-input-group style="width: 3.2rem; margin: auto; margin-top: 20px; margin-bottom: 20px;">
                <b-form-input type="number" v-model.number="value" min="0" :max="god_value"
                              @input="$emit('update:value', value);"></b-form-input>
            </b-input-group>
          <p style="padding-left: 0;" v-if="!show_progress">{{value}} هزار تومن</p>
        </div>
        <b-row>
          <b-col>
            <b-card-text v-if="show_money">
                پول نفر دوم: {{god_value-value+god_number}} هزار تومن
            </b-card-text>
          </b-col>
          <b-col>
            <b-card-text v-if="show_money">
                پول نفر اول: {{value-god_number+100}} هزار تومن
            </b-card-text>
          </b-col>
        </b-row>
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
    god_number: Number,
    show_progress: {
      type: Boolean,
      default: false
    },
    value: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style>
    .input-group-text {
        border-radius: 0 !important;
    }
</style>
