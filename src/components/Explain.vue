<template>
  <b-card img-right>
      <b-card-img :src="require('../assets/image.png')"></b-card-img>
      <b-card-text class="text-right">
          {{msg}}
      </b-card-text>
    </b-card>
</template>

<script>
export default {
  data () {
    return {
      show: true
    }
  },
  props: {
    msg: String
  }
}
</script>
