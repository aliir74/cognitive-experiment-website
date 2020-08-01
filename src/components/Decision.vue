<template>
    <b-card img-right>
        <b-card-text>
            {{ msg }}
        </b-card-text>
        <div>
            <b-input-group prepend="0" :append="god_value" v-if="show_progress">
                <b-form-input v-model="value" type="range" min="0" :max="god_value"
                              @change="$emit('update:value', value);"></b-form-input>
            </b-input-group>
            <p style="padding-left: 20px" v-if="show_progress">{{value}}</p>

            <b-input-group style="width: 70px; margin: auto" v-if="!show_progress">
                <b-form-input type="number" v-model="value"
                              @change="$emit('update:value', value);"></b-form-input>
            </b-input-group>
        </div>
        <b-card-text v-if="show_money">
            پول نفر اول: {{value-god_number+100}}
        </b-card-text>
        <b-card-text v-if="show_money">
            پول نفر دوم: {{god_value-value+god_number}}
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
