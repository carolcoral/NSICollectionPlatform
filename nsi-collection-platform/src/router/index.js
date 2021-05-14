import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/UserManager'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/UserManager',
                    component: () => import(/* webpackChunkName: "dashboard" */ '../components/page/UserManager.vue'),
                    meta: { title: '用户管理' }
                },
                {
                    path: '/DnsResolution',
                    component: () => import(/* webpackChunkName: "tabs" */ '../components/page/DnsResolution.vue'),
                    meta: { title: 'DNS解析' }
                },
                {
                    path: '/SubdomainLookup',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/SubdomainLookup.vue'),
                    meta: { title: '子域名查询' }
                },
                {
                    path: '/EmailInformationCapture',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/EmailInformationCapture.vue'),
                    meta: { title: '邮箱信息抓取' }
                },
                {
                    path: '/PortDetection',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/PortDetection.vue'),
                    meta: { title: '端口检测' }
                },
                {
                    path: '/OperationLog',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/OperationLog.vue'),
                    meta: { title: '操作记录' }
                }
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '/register',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Register.vue'),
            meta: { title: '注册' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
