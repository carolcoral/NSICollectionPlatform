<template>
  <div>
    <!--导航-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-qrcode"></i>端口检测</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主结构-->
    <div class="container">
      <!--工具框-->
      <div class="handle-box" style="width: 100%">
        <div>
          <el-input v-model="domain" placeholder="请输入域名或IP"  style="float: left; width: 200px; margin: 0 10px 10px 0"></el-input>
          <el-input v-model="port" placeholder="请输入端口"  style="float: left; width: 100px; margin: 0 10px 10px 0" :min=0 type="number"></el-input>
          <el-button type="primary" icon="el-icon-search" @click="getPortDetection(true)" style="float:left;">搜索</el-button>
        </div>

      </div>

      <!--列表-->
      <el-table :data="dataList" border class="table" ref="dataList" header-cell-class-name="table-header" v-loading="listLoading">
        <el-table-column prop="domain" label="域名/IP" min-width="40" sortable></el-table-column>
        <el-table-column prop="port" label="端口" min-width="40" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="status" label="状态" width="80" sortable :show-overflow-tooltip="true">
          <template scope="scope">
            <el-tag type="success" v-if="scope.row.status === true">启用</el-tag>
            <el-tag type="danger" v-else-if="scope.row.status === false">禁用</el-tag>
          </template>
        </el-table-column>
      </el-table>

    </div>
  </div>
</template>

<script>
import { portDetection } from '../../api/index';
export default {
  name: 'PortDetection',
  data() {
    return {
      //列表展示
      dataList:[],
      listLoading: false,
      domain:"",
      port: 0
    };
  },
  methods: {
    getPortDetection:function (search) {
      if (search && this.domain === ""){
        this.$message.warning("域名不能为空")
        return false;
      }
      portDetection({
        "domain": this.domain,
        "port": this.port
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
