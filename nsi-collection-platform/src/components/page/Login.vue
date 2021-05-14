<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">后台管理系统</div>
      <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="username">
            <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
              type="password"
              placeholder="password"
              v-model="param.password"
              @keyup.enter.native="submitForm()"
          >
            <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm()" style="float:left;width: 45%;">登录</el-button>
          <el-button type="primary" @click="toRegister()" style="float: none;width: 45%;">注册</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { login } from '../../api/index';
export default {
  data() {
    return {
      param: {
        username: '',
        password: '',
      },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      },
    };
  },
  // beforeRouteEnter(to,from,next){
  //     login(this.param).then(res=>{
  //         this.$message.success('登录成功');
  //         // localStorage.setItem('ms_username', this.param.username);
  //         // localStorage.setItem('username', this.param.username);
  //         localStorage.setItem('token', res);
  //     }).next('/')
  // },
  methods: {
    // async submitForm() {
    //   await this.$refs.login.validate(valid => {
    //     if (valid) {
    //       login(this.param).then(res => {
    //         this.$message.success('登录成功');
    //         localStorage.setItem('user_name', this.param.username);
    //         localStorage.setItem('token', res['token'].toString());
    //         localStorage.setItem('role', res['role'].toString());
    //         this.$router.push({ path: '/UserManager' });
    //       })
    //     } else {
    //       this.$message.error('请输入账号和密码');
    //       return false;
    //     }
    //   });
    // },
     submitForm() {
       this.$refs.login.validate(valid => {
        if (valid) {
          login(this.param).then(res => {
            this.$message.success('登录成功');
            localStorage.setItem('user_name', this.param.username);
            localStorage.setItem('token', res['token'].toString());
            localStorage.setItem('role', res['role'].toString());
            this.$router.push({ path: '/UserManager' });
          })
        } else {
          this.$message.error('请输入账号和密码');
          return false;
        }
      });
    },
    toRegister: function(){
      this.$router.push({ path: '/register'})
    }
  },
};
</script>

<style scoped>
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../../assets/img/login-bg.jpg);
  background-size: 100%;
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: #fff;
  border-bottom: 1px solid #ddd;
}
.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}
.ms-content {
  padding: 30px 30px;
}
.login-btn {
  text-align: center;
}
.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
</style>
