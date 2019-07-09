import Vue from 'vue'
import Router from 'vue-router'

import Login from './components/Auth/Login'
import Auth from './components/Auth/Auth'
import MainToppage from './components/Main/MainToppage'
import MainIndex from './components/Main/MainIndex'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/login',
      component: Login,
      meta: { isPublic: true }
    },
    {
      path: '/admin',
      component: Auth,
      children: [
        {
          path: '/',
          component: MainToppage
        },
        {
          path: ':model',
          component: MainIndex
        }
      ]
    },
    {
      path: '',
      redirect: '/admin'
    }
  ]
})

router.beforeEach((to, from, next) => {
  // isPublic でない場合(=認証が必要な場合)、かつ、ログインしていない場合
  // localStorageのトークンの有無でログイン状態を確認。サーバー側でトークンが無効ならログアウト
  if (to.matched.some((record) => !record.meta.isPublic) &&
      !localStorage.getItem('login_id') &&
      !localStorage.getItem('login_token')
  ) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
