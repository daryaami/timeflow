
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

router.afterEach((to) => {
  document.title = to.meta.metaTitle || 'TimeFlow';
});

app.mount('#app')
