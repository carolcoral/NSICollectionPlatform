<template>
  <div>
    <!--导航-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-qrcode"></i>用户管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主结构-->
    <div class="container">
      <!--工具框-->
      <div class="handle-box">
        <el-button type="primary" icon="el-icon-document-add" @click="handleAdd" class="handle-del mr10">新增</el-button>
<!--        <el-input v-model="query.name" placeholder="任意关键词"  style="float: none; width: 20%; margin: 0 10px 10px 0">-->
<!--          <el-button type="primary" icon="el-icon-search" @click="listUserInfo(true)" slot="append">搜索</el-button>-->
<!--        </el-input>-->
      </div>

      <!--列表-->
      <el-table :data="dataList" border class="table" ref="dataList" header-cell-class-name="table-header" v-loading="listLoading">
        <el-table-column prop="id" label="ID" min-width="40" sortable></el-table-column>
        <el-table-column prop="username" label="用户名" min-width="60" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="role" label="角色" min-width="50" sortable :show-overflow-tooltip="true">
          <template scope="scope">
            <el-tag type="success" v-if="scope.row.role === 'admin'">管理员</el-tag>
            <el-tag type="primary" v-else-if="scope.row.role === 'user'">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="updateTime" label="更新时间" min-width="100" sortable></el-table-column>
        <el-table-column label="操作" min-width="150">
          <template scope="scope">
            <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)" plain>编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.$index, scope.row)" plain>删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--新增界面-->
      <el-dialog title="新增用户" :visible.sync="addFormVisible" :close-on-click-modal="false">
        <el-form :model="addForm" label-width="80px" ref="addForm">
          <el-form-item label="用户名" prop="name">
            <el-input v-model="addForm.username" auto-complete="off" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="desc">
            <el-input v-model="addForm.password" auto-complete="off" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item label="重复密码" prop="desc">
            <el-input v-model="addForm.rePassword" auto-complete="off" placeholder="请确认密码" type="password"></el-input>
          </el-form-item>
          <el-form-item label="角色" prop="service">
            <el-select v-model="addForm.role" placeholder="请选择用户角色">
              <el-option v-for="item in roleType"
                         :key="item.value"
                         :label="item.label"
                         :value="item.value"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
        </div>
      </el-dialog>

      <!--编辑界面-->
      <el-dialog title="编辑用户" :visible.sync="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="120px" ref="editForm">
          <el-form-item label="用户名" prop="name">
            <el-input v-model="editForm.username" auto-complete="off" placeholder="请输入用户名" disabled></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="desc">
            <el-input v-model="editForm.password" auto-complete="off" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item label="重复密码" prop="desc">
            <el-input v-model="editForm.rePassword" auto-complete="off" placeholder="请确认密码" type="password"></el-input>
          </el-form-item>
          <el-form-item label="角色" prop="service">
            <el-select v-model="editForm.role" placeholder="请选择用户角色">
              <el-option v-for="item in roleType"
                         :key="item.value"
                         :label="item.label"
                         :value="item.value"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { userList, userGet, userAdd, userDelete, userEdit } from '../../api/index';
export default {
  name: 'UserManager',
  data() {
    return {
      query: {
        // name: ''
      },
      pageTotal: 0,
      username: localStorage.getItem("user_name"),
      //列表展示
      dataList:[],
      listLoading: false,
      //新增
      addFormVisible: false,
      addForm: {},
      addLoading: false,
      //编辑
      editFormVisible: false,
      editForm: {},
      editLoading: false,
      roleType: [
        {
          label:"普通用户",
          value:"user"
        },
        {
          label:"管理员",
          value:"admin"
        }
      ]
    };
  },
  methods: {
    //获取接口详情列表，
    listUserInfo:function (search) {
      const role = localStorage.getItem("role");
      if ('admin' !== role){
        this.$message({
          type: 'warning',
          message: '您无访问当前页面的权限!'
        })
        return false;
      }
      userList(this.query).then((res) => {
        this.dataList = res;
      });
    },
    //显示新增界面
    handleAdd: function() {
      if (this.$refs["addForm"]!==undefined) {
        this.$refs["addForm"].resetFields();
      }
      this.addFormVisible = true;
    },
    //新增
    addSubmit: function () {
      this.addLoading = true;
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          if (this.addForm.password !== this.addForm.rePassword){
            this.$message.error("两次密码不一致")
            return false;
          }
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            let para = Object.assign({}, this.addForm);
            userAdd(para).then((res) => {
              this.$message({
                message: "新增成功",
                type: 'success'
              });
              this.addFormVisible = false;
              this.listUserInfo();
            });
          });
        }
      });
      this.addLoading = false;
    },
    //显示编辑界面
    handleEdit: function (index, row) {
      this.editForm = {};
      let params = {
        id: row.id
      };
      userGet(params).then(res=>{
        this.editForm = res;
      });
      this.editFormVisible = true;
    },
    //编辑页面
    editSubmit: function(){
      this.editLoading = true;
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          if (this.editForm.password !== this.editForm.rePassword){
            this.$message.error("两次密码不一致")
            return false;
          }
          this.$confirm('提示', {}).then(() => {
            let para = Object.assign({}, this.editForm);
            userEdit(para).then((res) => {
              this.editLoading = false;
              this.$message({
                message: "编辑成功",
                type: 'success'
              });
              this.editFormVisible = false;
              this.listUserInfo();
            });
          });
        }
      });
      this.editLoading = false;
    },
    handleDelete: function(index, row){
      this.$confirm('确认删除吗？', '提示', {}).then(() => {
        let para = {
          id: row.id
        };
        userDelete(para).then((res) => {
          this.$message({
            message: "删除成功",
            type: 'success'
          });
          this.listUserInfo();
        });
      });
    }
  },
  mounted() {
    this.query.name = "";
    this.listUserInfo();
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
</style>
