<script setup>
import googleButtonVue from '../components/buttons/google-button.vue'
import logoVue from '../components/icons/logo.vue'
</script>

<template>
  <section class="login-page">
    <div class="login-page__wrapper">
      <logoVue 
        class="login-page__logo"
      />
      <h1 class="login-page__title">Log in to TimeFlow</h1>

      <googleButtonVue class="login-page__button"
        href="#"
        text="Continue with Google"
      />

      <p class="login-page__text">Don't have an account? <RouterLink to="/signup/">Sign Up</RouterLink></p>

      <p class="login-page__privacy-text">By using TimeFlow, you agree to our <a href="javascript:void();">Terms of Service</a> and <a href="javascript:void();">Privacy Policy</a>.</p>
    </div>
  </section>
</template>

<style lang="scss">
  .login-page {
    display: flex;
    width: 100%;
    height: 100%;
    background-color: $violet;
    align-items: center;
    justify-content: center;

    &__wrapper {
      display: flex;
      align-items: center;
      flex-direction: column;
    }

    &__logo {
      display: block;
      width: size(70px);
      height: size(70px);
      margin-bottom: size(20px);
    }

    &__title {
      font-weight: 600;
      font-size: size(50px);
      line-height: 100%;
      text-align: center;
      color: $white;
      margin-top: 0;
      margin-bottom: size(88px);
    }

    &__button {
      margin-bottom: size(44px);
    }

    &__text {
      color: $white;
      font-weight: 400;
      font-size: size(20px);
      line-height: 100%;
      margin-top: 0;
      margin-bottom: size(163px);

      & a {
        color: #4BB6E4
      }
    }


    &__privacy-text {
      font-weight: 300;
      font-size: size(20px);
      color: $dark-lines;
      margin: 0;

      & a {
        text-decoration: underline;
      }
    }
  }
</style>
