import axios from 'axios';
import { errorLog, errorCreate } from './tools'
import router from '../router'
import { Message } from 'element-ui'

const service = axios.create({
    // process.env.NODE_ENV === 'development' 来判断是否开发环境
    // easy-mock服务挂了，暂时不使用了
    // baseURL: 'https://www.easy-mock.com/mock/592501a391470c0ac1fab128',
    timeout: 5000
});

service.interceptors.request.use(
    config => {
        return config;
    },
    error => {
        return Promise.reject();
    }
);

service.interceptors.response.use(
    response => {
        const dataAxios = response.data
        const { code } = dataAxios
        if (code === undefined) {
            // 如果没有 code 代表这不是项目后端开发的接口 比如可能是 D2Admin 请求最新版本
            return dataAxios
        } else{
            // 有 code 代表这是一个后端接口 可以进行进一步的判断
            switch (code) {
                case '000000':
                    return dataAxios.data;
                case '999999':
                    //登录注销
                    Message({
                        message: '登录过期，注销登录，自动跳转登录页面.',
                        type: 'error'
                    })
                    localStorage.removeItem('user_name');
                    localStorage.removeItem('token');
                    router.push({path:'/login'})
                    break;
                default:
                    // 不是正确的 code
                    errorCreate(`${dataAxios.desc}`);
                    break
            }
        }
    },
    error => {
        if (error && error.response) {
            switch (error.response.code) {
                case 400: error.message = '请求错误'; break;
                case 401: error.message = '未授权，请登录'; window.location.href = '/#/login';break;
                case 403: error.message = '拒绝访问'; break;
                case 404: error.message = `请求地址出错: ${error.response.config.url}`; break;
                case 408: error.message = '请求超时'; break;
                case 500: error.message = '服务器内部错误'; break;
                case 501: error.message = '服务未实现'; break;
                case 502: error.message = '网关错误'; break;
                case 503: error.message = '服务不可用'; break;
                case 504: error.message = '网关超时'; break;
                case 505: error.message = 'HTTP版本不受支持'; break;
                default: break
            }
        }
        errorLog(error);
        return Promise.reject(error)
    }
);

export default service;
