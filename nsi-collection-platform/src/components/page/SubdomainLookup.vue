<template>
  <div>
    <!--导航-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-qrcode"></i>子域名解析</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主结构-->
    <div class="container">
      <!--工具框-->
      <div class="handle-box" style="width: 450px">
        <div style="width: 250px; float: left">
          <el-input v-model="domain" placeholder="请输入域名 baidu.com"  style="float: none; width: 160%; margin: 0 10px 10px 0">
            <el-button type="primary" icon="el-icon-search" @click="getSubDnsResolve(true)" slot="append">搜索</el-button>
          </el-input>
        </div>

      </div>

      <!--列表-->
      <el-table :data="dataList" border class="table" ref="dataList" header-cell-class-name="table-header" v-loading="listLoading">
        <el-table-column prop="href" label="地址" min-width="120" sortable></el-table-column>
        <el-table-column prop="title" label="描述" min-width="200" sortable :show-overflow-tooltip="true"></el-table-column>
      </el-table>

    </div>
  </div>
</template>

<script>
import { subdomainLookup } from '../../api/index';
export default {
  name: 'SubdomainLookup',
  data() {
    return {
      //列表展示
      dataList:[],
      listLoading: false,
      domain:""
    };
  },
  methods: {
    getSubDnsResolve:function (search) {
      if (search && this.domain === ""){
        this.$message.warning("域名不能为空")
        return false;
      }
      subdomainLookup({
        "domain": this.domain
      }).then((res) => {
        this.dataList = res;
      });
    }
  },
  mounted() {
    this.getSubDnsResolve();
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
