<template>
  <b-card img-right>
      <b-card-text class="text-right" v-html="msg">
      </b-card-text>
      <b-card-img v-show="show_image" :src="require('../assets/image.png')"></b-card-img>
    </b-card>
</template>

<script>
export default {
  props: {
    msg: String,
    show_image: {
      type: Boolean,
      default: true
    }
  }
}
</script>
