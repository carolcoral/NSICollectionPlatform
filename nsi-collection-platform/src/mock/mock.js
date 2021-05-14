import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import Mock from 'mockjs';

export default {
    /**
     * mock bootstrap
     */
    bootstrap() {
        let mock = new MockAdapter(axios);

        // mock success request
        mock.onGet('/success').reply(200, {
            msg: 'success'
        });

        // mock error request
        mock.onGet('/error').reply(500, {
            msg: 'failure'
        });

        //登录
        mock.onPost('/admin/login').reply(config => {
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve([200, { code: '000000', desc: '请求成功', data: {
                            "token": 'e0c5b8de1d04d1cc412c4a44925a1c3f',
                            "role": "admin"
                        } }]);
                }, 1000);
            });
        });

    }
};
