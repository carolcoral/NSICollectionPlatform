<template>
  <div>
    <!--导航-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-qrcode"></i>DNS解析</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主结构-->
    <div class="container">
      <!--工具框-->
      <div class="handle-box" style="width: 450px">
        <div style="width: 60px; float: left;">
          <el-select v-model="domainType" slot="prepend">
            <el-option label="A" value="A"></el-option>
            <el-option label="MX" value="MX"></el-option>
            <el-option label="NS" value="NS"></el-option>
            <el-option label="CNAME" value="CNAME"></el-option>
          </el-select>
        </div>
        <div style="width: 250px; float: left">
          <el-input v-model="domain" placeholder="请输入域名 www.baidu.com"  style="float: none; width: 160%; margin: 0 10px 10px 0">
            <el-button type="primary" icon="el-icon-search" @click="getDnsResolve(true)" slot="append">搜索</el-button>
          </el-input>
        </div>

      </div>

      <!--列表-->
      <el-table :data="dataList" border class="table" ref="dataList" header-cell-class-name="table-header" v-loading="listLoading">
        <el-table-column prop="domain" label="域名" min-width="80" sortable></el-table-column>
        <el-table-column prop="ip" label="IP" min-width="60" sortable></el-table-column>
        <el-table-column prop="country" label="国家" min-width="60" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="area" label="地区" min-width="60" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="province" label="省份" min-width="60" sortable></el-table-column>
        <el-table-column prop="city" label="城市" min-width="60" sortable></el-table-column>
        <el-table-column prop="isp" label="运营商" min-width="60" sortable></el-table-column>
      </el-table>

    </div>
  </div>
</template>

<script>
import { dnsResolve } from '../../api/index';
export default {
  name: 'DnsResolution',
  data() {
    return {
      //列表展示
      dataList:[],
      listLoading: false,
      domain:"",
      domainType: "A"
    };
  },
  methods: {
    getDnsResolve:function (search) {
      if (search && this.domain === ""){
        this.$message.warning("域名不能为空")
        return false;
      }
      dnsResolve({
        "domain": this.domain,
        "domainType": this.domainType
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
