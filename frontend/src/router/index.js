import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LogIn.vue'),
      meta: { 
        layout: 'login',
        metaTitle: 'Log in to TimeFlow'  
       },
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignUp.vue'),
      meta: { 
        layout: 'login',
        metaTitle: 'Sign up to TimeFlow'  
      },
    },
    {
      path: '/planner',
      name: 'planner',
      component: () => import('../views/Planner.vue'),
      meta: { 
        layout: 'default',
        title: 'Planner',
        metaTitle: 'Planner' 
      },
    },
  ]
})

export default router
