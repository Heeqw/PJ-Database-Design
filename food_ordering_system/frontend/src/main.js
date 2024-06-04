import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

// 路由配置
app.use(router)

// Axios 配置
axios.defaults.baseURL = 'http://localhost:8000/api' // 后端 API 地址
axios.defaults.timeout = 30000 // 请求超时时间（单位：毫秒）

axios.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
})

// 在接收到响应之后，可以做一些拦截处理，例如处理错误信息等
axios.interceptors.response.use(
    response => {
        // 处理响应数据
        return response
    },
    error => {
        // 处理错误信息
        if (error.response && error.response.status === 401) {
            // 这里可以处理认证失败的情况，例如跳转到登录页面
        }
        return Promise.reject(error)
    }
)

// 将 Axios 实例挂载到 Vue 实例的原型上，使所有组件都可以通过 this.$axios 访问
app.config.globalProperties.$axios = axios

// 挂载 Vue 应用实例到 #app 标签下
app.mount('#app')
