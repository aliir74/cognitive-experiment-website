<template>
  <b-card>
    <b-form v-if="show">
      <b-form-group
        id="input-group-1"
        label="آدرس ایمیل:"
        label-for="input-1"
        description=""
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          required
          placeholder="ایمیل خود را وارد کنید"
          @change="$emit('update:form', form);"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="نام و نام خانوادگی:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.name"
          required
          placeholder="نام و نام خانوادگی"
          @change="$emit('update:form', form);"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="شماره موبایل:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="form.mobile"
          required
          placeholder="شماره موبایل"
          @change="$emit('update:form', form);"
        ></b-form-input>
      </b-form-group>
    </b-form>
  </b-card>
</template>

<script>
export default {
  data () {
    return {
      form: {
        email: '',
        name: '',
        mobile: ''
      },
      show: true
    }
  }
}
</script>
