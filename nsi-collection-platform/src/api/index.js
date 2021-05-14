import request from '../utils/request';

let base = '/admin';
// let base = 'http://127.0.0.1:8080/admin';

//过滤请求内容
request.interceptors.request.use(
    config => {
        config.headers["token"] = localStorage.getItem('token');
        // if (config.method === "post") {
        //     config.data = qs.stringify(config.data);
        //     config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
        //     config.headers["user_name"] = "";
        // }
        return config;
    }
);

//登录
export const login = (params, headers) => { return request.post(`${base}/login`, params, {headers: headers }); };
//注册
export const register = (params, headers) => { return request.post(`${base}/register`, params, {headers: headers }); };
//用户操作
export const userList = (params, headers) => { return request.get(`${base}/user/list`, { params: params, headers: headers }); };
export const userGet = (params, headers) => { return request.get(`${base}/user/get`, { params: params, headers: headers }); };
export const userAdd = (params, headers) => { return request.post(`${base}/user/add`, params, {headers: headers }); };
export const userDelete = (params, headers) => { return request.post(`${base}/user/delete`, params, {headers: headers }); };
export const userEdit = (params, headers) => { return request.post(`${base}/user/edit`, params, {headers: headers }); };
//DNS解析
export const dnsResolve = (params, headers) => { return request.get(`${base}/dns/resolution`, { params: params, headers: headers }); };
//子域名解析
export const subdomainLookup = (params, headers) => { return request.get(`${base}/subdomain/lookup`, { params: params, headers: headers }); };
//邮箱内容抓取
export const emailGrabbing = (params, headers) => { return request.get(`${base}/email/grabbing`, { params: params, headers: headers }); };
//端口检测
export const portDetection = (params, headers) => { return request.get(`${base}/port/detection`, { params: params, headers: headers }); };
