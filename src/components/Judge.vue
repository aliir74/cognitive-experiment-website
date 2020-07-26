<template>
    <b-card img-right>
        <b-card-text>
            {{ msg }}
        </b-card-text>
        <div>
            <b-input-group prepend="دگرخواه" append="خودخواه">
                <b-form-input v-model="value" type="range" min="0" max="10"
                              @keyup="$emit('update:value', value);"></b-form-input>
            </b-input-group>
            <p>{{value}}</p>
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
