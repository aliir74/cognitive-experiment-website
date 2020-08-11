<template>
    <b-card img-right>
        <b-card-text v-html="msg">
        </b-card-text>
        <div>
            <b-input-group dir="ltr" prepend="دگرخواه" append="خودخواه">
                <b-form-input  v-model="value" type="range" min="-5" max="5"
                              @change="$emit('update:value', value);"></b-form-input>
            </b-input-group>
            <b-input-group style="width: 3rem; margin: auto; margin-top: 20px; margin-bottom: 20px;">
                <b-form-input type="number" v-model="value" min="-5" max="5"
                              @change="$emit('update:value', value);"></b-form-input>
            </b-input-group>
<!--            <p>{{value}}</p>-->
        </div>
    </b-card>
</template>

<script>
export default {
  props: {
    msg: String,
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
