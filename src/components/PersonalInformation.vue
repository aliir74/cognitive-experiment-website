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
          :state="emailState"
          aria-describedby="input1-live-feedback"
          placeholder="ایمیل خود را وارد کنید"
          @change="$emit('update:form', form);"
        ></b-form-input>
        <b-form-invalid-feedback id="input1-live-feedback">
          ایمیل خود را درست وارد کنید.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group id="input-group-2" label="نام و نام خانوادگی:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.name"
          required
          aria-describedby="input2-live-feedback"
          :state="nameState"
          placeholder="نام و نام خانوادگی"
          @change="$emit('update:form', form);"
        ></b-form-input>
        <b-form-invalid-feedback id="input2-live-feedback">
          نام و نام خانوادگی خود را وارد کنید.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group id="input-group-3" label="شماره موبایل:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="form.mobile"
          required
          :state="mobileState"
          aria-describedby="input3-live-feedback"
          placeholder="شماره موبایل"
          @change="$emit('update:form', form);"
        ></b-form-input>
        <b-form-invalid-feedback id="input3-live-feedback">
          شماره موبایل خود را وارد کنید.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group id="input-group-4" label="سن:" label-for="input-4">
        <b-form-input
          id="input-4"
          v-model="form.age"
          required
          :state="ageState"
          aria-describedby="input4-live-feedback"
          type="number"
          @change="$emit('update:form', form);"
        ></b-form-input>
        <b-form-invalid-feedback id="input4-live-feedback">
          سن خود را وارد کنید.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group id="input-group-5" label="جنسیت:" label-for="input-5">
        <b-form-select v-model="form.sex" :options="['زن', 'مرد']" id="input-5"
                       aria-describedby="input5-live-feedback" :state="sexState"
          @change="$emit('update:form', form);"></b-form-select>
        <b-form-invalid-feedback id="input5-live-feedback">
          جنسیت خود را مشخص کنید.
        </b-form-invalid-feedback>
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
        mobile: '',
        sex: '',
        age: ''
      },
      show: true,
      email_reg: /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
    }
  },
  computed: {
    emailState () {
      return this.email_reg.test(this.form.email)
    },
    nameState () {
      return this.form.name !== ''
    },
    ageState () {
      return this.form.age !== '' && this.form.age > 0
    },
    sexState () {
      return this.form.sex !== ''
    },
    mobileState () {
      return (this.form.mobile !== '' && isNaN(this.form.mobile) === false)
    }
  }
}
</script>
