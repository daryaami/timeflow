<script setup>
import googleButtonVue from '../components/blocks/buttons/google-button.vue'
import logoVue from '../components/icons/logo.vue'
</script>

<template>
  <section class="sign-up-page">
    <logoVue 
      class="sign-up-page__logo"
    />
    <h1 class="sign-up-page__title">Welcome to TimeFlow</h1>
    <span class="sign-up-page__subtitle">Try out the new planning experience</span>

    <googleButtonVue class="sign-up-page__button"
      href="/google_auth_api/register/"
      text="Connect your Google account "
    />

    <p class="sign-up-page__text">Have an account?&nbsp;<RouterLink to="/login/">Log in</RouterLink></p>

    <p class="sign-up-page__privacy-text">By using TimeFlow, you agree to our <a href="javascript:void();">Terms of Service</a> and <a href="javascript:void();">Privacy Policy</a>.</p>
  </section>
</template>

<style lang="scss">
  .sign-up-page {
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: $white;
    padding-top: size(96px);
    padding-bottom: size(72px);
    width: size(1003px);
    border-radius: size(30px);

    &__logo {
      display: block;
      width: size(70px);
      height: size(70px);
      margin-bottom: size(19px);
    }

    &__title {
      font-weight: 600;
      font-size: size(50px);
      line-height: 100%;
      text-align: center;
      color: $darkest;
      margin-top: 0;
      margin-bottom: size(8px);
    }

    &__subtitle {
      font-weight: 250;
      font-size: size(30px);
      text-align: center;
      color: $darkest;
      margin-top: 0;
      margin-bottom: size(35px);
    }

    &__button {
      margin-bottom: size(23px);
    }

    &__text {
      color: $dark-grey;
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
      color: $light-grey;
      margin: 0;

      & a {
        text-decoration: underline;
      }
    }
  }
</style>
