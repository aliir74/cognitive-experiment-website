<template>
    <b-card img-right>
        <b-card-text v-for="(it, index) in msg" :key="index">
            {{ it }}
            <b-input-group dir="ltr" prepend="مخالف" append="موافق">
                <b-form-input v-model="value[index]" type="range" min="1" max="5"
                              @change="$emit('update:value', value);"></b-form-input>
            </b-input-group>
            <p>{{value[index]}}</p>
        </b-card-text>
    </b-card>
</template>

<script>
export default {
  props: {
    msg: Array,
    value: Array
  }
}
</script>

<style>
    .input-group-text {
        border-radius: 0 !important;
    }
</style>
