<template>
  <div>
    <!--导航-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-qrcode"></i>操作记录</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主结构-->
    <div class="container">
      <!--工具框-->
      <div class="handle-box" style="width: 450px">
        <div style="width: 250px; float: left">
          <el-input v-model="params.username" placeholder="请输入用户名"  style="float: none; width: 160%; margin: 0 10px 10px 0">
            <el-button type="primary" icon="el-icon-search" @click="getOperationLog(true)" slot="append">搜索</el-button>
          </el-input>
        </div>

      </div>

      <!--列表-->
      <el-table :data="dataList" border class="table" ref="dataList" header-cell-class-name="table-header" v-loading="listLoading">
        <el-table-column prop="id" label="ID" min-width="40" sortable></el-table-column>
        <el-table-column prop="username" label="用户名" min-width="80" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="operationContent" label="操作内容" min-width="120" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="operationData" label="执行数据" min-width="100" sortable>
          <template scope="scope">
            <el-button type="primary" icon="el-icon-view" circle @click="getExecuteResult(scope.$index, scope.row)"></el-button>
          </template>
        </el-table-column>
        <el-table-column prop="updateTime" label="执行时间" min-width="120" sortable :show-overflow-tooltip="true"></el-table-column>
      </el-table>

    </div>

    <!--  json格式化展示  -->
    <el-dialog title="展示" :visible.sync="jsonDialogVisible" width="50%" center>
      <json-viewer :value="jsonData" :expand-depth=50 copyable boxed sort></json-viewer>
    </el-dialog>

  </div>
</template>

<script>
    import { operationLog } from '../../api/index';
    export default {
        name: 'OperationLog',
        data() {
            return {
                //列表展示
                dataList:[],
                listLoading: false,
                params: {
                    username: ""
                },
                //request response json 格式化展示
                jsonDialogVisible: false,
                jsonData: {}
            };
        },
        methods: {
            getOperationLog:function (search) {
                const role = localStorage.getItem("role");
                if ('admin' !== role){
                    this.$message({
                        type: 'warning',
                        message: '您无访问当前页面的权限!'
                    });
                    return false;
                }
                if (search && this.domain === ""){
                    this.$message.warning("域名不能为空")
                    return false;
                }
                operationLog(this.params).then((res) => {
                    this.dataList = res;
                });
            },
            getExecuteResult: function(index, row) {
                const operationData = row.operationData.toString();
                this.jsonData = JSON.parse(operationData.replace(/'/g, '"'));
                this.jsonDialogVisible = true
            }
        },
        mounted() {
            this.getOperationLog()
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
