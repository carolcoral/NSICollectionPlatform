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
          <el-input type="password" placeholder="password" v-model="param.password">
            <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item prop="rePassword">
          <el-input type="password" placeholder="password" v-model="param.rePassword">
            <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="returnLogin()" style="float:left;width: 45%;">返回登录</el-button>
          <el-button type="primary" @click="register()" style="float: none;width: 45%;">注册</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { register } from '../../api/index';
export default {
  data() {
    return {
      param: {
        username: '',
        password: '',
        rePassword: ''
      },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        rePassword: [{ required: true, message: '请再次输入密码', trigger: 'blur' }],
      },
    };
  },
  methods: {
    returnLogin: function(){
      this.$router.push({
        path: '/login'
      })
    },
    register: function(){
      if (this.param.password !== this.param.rePassword){
        this.$message.error("两次密码不一致")
        return false;
      }
      this.$confirm('确认提交吗？', '提示', {}).then(() => {
        register(this.param).then((res) => {
          this.$message({
            message: "注册成功",
            type: 'success'
          });
          this.returnLogin()
        });
      });
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
