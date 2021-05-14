<template>
  <div>
    <!--导航-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-qrcode"></i>邮箱账号抓取</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主结构-->
    <div class="container">
      <!--工具框-->
      <div class="handle-box" style="width: 100%">
        <div>
          <el-input v-model="keyword" placeholder="请输入邮箱关键字，例如: led"  style="float: left; width: 200px; margin: 0 10px 10px 0"></el-input>
          <el-input v-model="email_suffix" placeholder="请输入邮箱后缀，例如： hotmail.com"  style="float: left; width: 100px; margin: 0 10px 10px 0" :min=0 type="number"></el-input>
          <el-button type="primary" icon="el-icon-search" @click="getEmailGrabbing(true)" style="float:left;">搜索</el-button>
        </div>

      </div>

      <!--列表-->
      <el-table :data="dataList" border class="table" ref="dataList" header-cell-class-name="table-header" v-loading="listLoading">
        <el-table-column prop="keyword" label="抓取关键字" min-width="40" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="grabbingEngine" label="邮箱账号信息抓取来源" min-width="40" sortable></el-table-column>
        <el-table-column prop="emailAddress" label="邮箱账号" min-width="40" sortable :show-overflow-tooltip="true"></el-table-column>
      </el-table>

    </div>
  </div>
</template>

<script>
import { emailGrabbing } from '../../api/index';
export default {
  name: 'PortDetection',
  data() {
    return {
      //列表展示
      dataList:[],
      listLoading: false,
      keyword:"",
      email_suffix: ""
    };
  },
  methods: {
    getEmailGrabbing:function (search) {
      if (search && this.domain === ""){
        this.$message.warning("域名不能为空")
        return false;
      }
      emailGrabbing({
        "keyword": this.keyword,
        "email_suffix": this.email_suffix
      }).then((res) => {
        this.dataList = res;
      });
    }
  },
  mounted() {
  }
};
</script>


<style scoped>
.handle-box {
  margin-bottom: 20px;
}
.handle-input {
  width: 300px;
  display: inline-block;
}
.table {
  width: 100%;
  font-size: 14px;
}
.mr10 {
  margin-right: 10px;
}
.red {
  color: #ff0000;
}
.yellow {
  color: #ebb563;
}
</style>
