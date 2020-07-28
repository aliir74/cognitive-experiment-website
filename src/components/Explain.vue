<template>
  <b-card img-right>
      <b-card-img v-show="show_image" :src="require('../assets/image.png')"></b-card-img>
      <b-card-text class="text-right">
          {{msg}}
      </b-card-text>
    </b-card>
</template>

<script>
export default {
  data () {
    return {
      show: true,
      show_image: true
    }
  },
  props: {
    msg: String
  }
}
</script>
