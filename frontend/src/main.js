
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@vuepic/vue-datepicker/dist/main.css';
import VueDraggableResizable from 'vue-draggable-resizable'

const app = createApp(App)

app.use(router)

app.component("vue-draggable-resizable", VueDraggableResizable)

router.afterEach((to) => {
  document.title = to.meta.metaTitle || 'TimeFlow';
});

app.mount('#app')
