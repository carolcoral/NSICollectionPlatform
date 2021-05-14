<template>
  <div>
    <!--导航-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-qrcode"></i>接口列表</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主结构-->
    <div class="container">
      <!--工具框-->
      <div class="handle-box">
        <el-button type="primary" icon="el-icon-document-add" @click="handleAdd" class="handle-del mr10">新增</el-button>
        <el-input v-model="query.name" placeholder="任意关键词"  style="float: none; width: 20%; margin: 0 10px 10px 0">
          <el-button type="primary" icon="el-icon-search" @click="getInterfaceList(true)" slot="append">搜索</el-button>
        </el-input>
      </div>

      <!--列表-->
      <el-table :data="interfaceListData" border class="table" ref="scheduledTasksData" header-cell-class-name="table-header" v-loading="listLoading" :default-sort = "{prop: 'update_time', order: 'descending'}">
        <el-table-column prop="id" label="ID" min-width="40" sortable></el-table-column>
        <el-table-column prop="name" label="接口名" min-width="140" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="desc" label="描述" width="200" sortable :show-overflow-tooltip="true"></el-table-column>
        <el-table-column prop="service" label="提供方" min-width="120" sortable></el-table-column>
        <el-table-column prop="type" label="接口类型" min-width="80" sortable></el-table-column>
        <el-table-column prop="enable" label="使用状态" min-width="80" sortable>
          <template scope="scope">
            <el-tag type="success" v-if="scope.row.enable === '启用'">启用</el-tag>
            <el-tag type="danger" v-else-if="scope.row.enable === '废弃'">废弃</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="生效时间" min-width="100" sortable></el-table-column>
        <el-table-column prop="user_name" label="更新人" min-width="60" sortable></el-table-column>
        <el-table-column prop="update_time" label="更新时间" min-width="100" sortable></el-table-column>
        <el-table-column label="操作" min-width="150">
          <template scope="scope">
            <el-button type="success" size="small" @click="handlerDetails(scope.$index, scope.row)" plain>详情</el-button>
            <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)"  v-if="username === 'jianghao' || username === 'liuxuewen' || username === 'admin'">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--新增界面-->
      <el-dialog title="新增接口详情" :visible.sync="addFormVisible" :close-on-click-modal="false">
        <el-form :model="addForm" label-width="120px" :rules="formRules" ref="addForm">
          <el-form-item label="接口名" prop="name">
            <el-input v-model="addForm.name" auto-complete="off" placeholder="请输入接口名"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="desc">
            <el-input v-model="addForm.desc" auto-complete="off" placeholder="请输入接口描述"></el-input>
          </el-form-item>
          <el-form-item label="提供方" prop="service">
            <el-select v-model="addForm.service" placeholder="请选择接口服务供应方">
              <el-option v-for="item in interfacesServices"
                         :key="item.value"
                         :label="item.label"
                         :value="item.label"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="接口类型" prop="type">
            <el-select v-model="addForm.type" placeholder="请选择接口归属类型">
              <el-option v-for="item in interfacesType"
                         :key="item.value"
                         :label="item.label"
                         :value="item.label"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="使用状态" prop="enable">
            <el-select v-model="addForm.enable" placeholder="请选择接口当前启用状态">
              <el-option v-for="item in interfacesEnable"
                         :key="item.value"
                         :label="item.label"
                         :value="item.label"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="接口请求命令" prop="request">
            <el-input v-model="addForm.request" auto-complete="off" placeholder="请输入接口请求命令"></el-input>
          </el-form-item>
          <el-form-item label="接口返回结果" prop="response">
            <el-input v-model="addForm.response" auto-complete="off" placeholder="请输入接口返回结果"></el-input>
          </el-form-item>
          <el-form-item label="接口生效时间" prop="create_time">
            <el-date-picker
                v-model="addForm.create_time"
                type="datetime"
                placeholder="请输入接口生效时间">
            </el-date-picker>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
        </div>
      </el-dialog>

      <!--编辑界面-->
      <el-dialog title="编辑接口详情" :visible.sync="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="120px" :rules="formRules" ref="editForm">
          <el-form-item label="接口名" prop="name">
            <el-input v-model="editForm.name" auto-complete="off" placeholder="请输入接口名" disabled></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="desc">
            <el-input v-model="editForm.desc" auto-complete="off" placeholder="请输入接口描述"></el-input>
          </el-form-item>
          <el-form-item label="提供方" prop="service">
            <el-select v-model="editForm.service" placeholder="请选择接口服务供应方" disabled>
              <el-option v-for="item in interfacesServices"
                         :key="item.value"
                         :label="item.label"
                         :value="item.label"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="接口类型" prop="type">
            <el-select v-model="editForm.type" placeholder="请选择接口归属类型">
              <el-option v-for="item in interfacesType"
                         :key="item.value"
                         :label="item.label"
                         :value="item.label"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="使用状态" prop="enable">
            <el-select v-model="editForm.enable" placeholder="请选择接口当前启用状态">
              <el-option v-for="item in interfacesEnable"
                         :key="item.value"
                         :label="item.label"
                         :value="item.label"
                         :disabled="item.disabled">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="接口请求命令" prop="request">
            <el-input v-model="editForm.request" auto-complete="off" placeholder="请输入接口请求命令"></el-input>
          </el-form-item>
          <el-form-item label="接口返回结果" prop="response">
            <el-input v-model="editForm.response" auto-complete="off" placeholder="请输入接口返回结果"></el-input>
          </el-form-item>
          <el-form-item label="接口生效时间" prop="create_time">
            <el-date-picker
                v-model="editForm.create_time"
                type="datetime"
                placeholder="请输入接口生效时间"
                disabled>
            </el-date-picker>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
        </div>
      </el-dialog>

      <!--详情界面-->
      <el-dialog title="详情" :visible.sync="detailsFormVisible" :close-on-click-modal="false">
        <el-form :model="detailsForm" label-width="120px" ref="detailsForm">
          <el-form-item label="接口名:" prop="name">
            {{detailsForm.name}}
          </el-form-item>
          <el-form-item label="描述:" prop="desc">
            {{detailsForm.desc}}
          </el-form-item>
          <el-form-item label="提供方:" prop="service">
            {{detailsForm.service}}
          </el-form-item>
          <el-form-item label="接口类型:" prop="type">
            {{detailsForm.type}}
          </el-form-item>
          <el-form-item label="使用状态:" prop="enable">
            <span style="color: green" v-if="detailsForm.enable === '启用'">启用</span>
            <span style="color: red" v-else-if="detailsForm.enable === '废弃'">废弃</span>
          </el-form-item>
          <el-form-item label="接口请求命令:">
            <span style="display:block; width: 500px; height: 30px;overflow: hidden;float: left" :show-overflow-tooltip="true">{{detailsForm.request}}</span>
            <el-button size="small" type="primary" ref="copy" icon="el-icon-copy-document" circle v-clipboard:success="requestCopy" v-clipboard:copy="detailsForm.request"></el-button>
          </el-form-item>
          <el-form-item label="接口返回结果:">
            <template scope="scope">
              <el-button type="primary" icon="el-icon-view" circle @click="getDetailsFormInfo(scope.$index, scope.row)"></el-button>
            </template>
          </el-form-item>
          <el-form-item label="接口生效时间:" prop="create_time">
            {{detailsForm.create_time}}
          </el-form-item>
          <el-form-item label="更新人:" prop="user_name">
            {{detailsForm.user_name}}
          </el-form-item>
          <el-form-item label="更新时间:" prop="update_time">
            {{detailsForm.update_time}}
          </el-form-item>
        </el-form>
      </el-dialog>

      <!--  json格式化展示  -->
      <el-dialog title="展示" :visible.sync="jsonDialogVisible" width="60%" center>
        <json-viewer :value="jsonData" :expand-depth=50 copyable boxed sort></json-viewer>
      </el-dialog>

      <!--分页-->
      <div class="pagination">
        <el-pagination
            background
            layout="total, prev, pager, next"
            :current-page="query.pageIndex"
            :page-size="query.pageSize"
            :total="pageTotal"
            @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
    import { getInterfaces, addInterface, editInterface, getSystemInfo, getInterfaceById } from '../../api/index';
    export default {
        name: 'interfaces',
        data() {
            return {
                query: {
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                pageTotal: 0,
                username: localStorage.getItem("user_name"),
                //列表展示
                interfaceListData:[],//接口详情列表
                listLoading: false,//列表展示
                //新增
                addFormVisible: false,
                addForm: {},
                addLoading: false,
                //编辑
                editFormVisible: false,
                editForm: {},
                editLoading: false,
                //新增、编辑通用信息
                formRules: {
                    name: [
                        { required: true, message: '请输入接口名', trigger: 'blur' }
                    ],
                    service:[
                        { required: true, message: '请选择接口服务供应方', trigger: 'blur'}
                    ],
                    type:[
                        { required: true, message: '请选择接口归属类型', trigger: 'blur'}
                    ],
                    enable:[
                        { required: true, message: '请选择接口当前启用状态', trigger: 'blur'}
                    ],
                    createTime: [
                        { required: true, message: '请选择接口生效时间', trigger: 'blur'}
                    ]
                },
                interfacesServices: [],
                interfacesType: [
                    {
                        label:"业务",
                        value:"业务"
                    },
                    {
                        label:"非业务",
                        value:"非业务"
                    },
                    {
                        label:"其他",
                        value:"其他"
                    }
                ],
                interfacesEnable: [
                    {
                        label:"启用",
                        value:"启用"
                    },
                    {
                        label:"废弃",
                        value:"废弃"
                    }
                ],
                //详情
                detailsFormVisible: false,
                detailsForm: [],
                //request response json 格式化展示
                jsonDialogVisible: false,
                jsonData: {}
            };
        },
        methods: {
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getInterfaceList();
            },
            //获取接口详情列表，
            getInterfaceList:function (search) {
                this.listLoading = true;
                if(search){
                    this.query.pageIndex = 1;
                }
                getInterfaces(this.query).then((res) => {
                    this.pageTotal = res.pageTotal;
                    this.interfaceListData = res.data;
                    this.listLoading = false;
                });
                this.handleServiceChange()
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
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            let para = Object.assign({}, this.addForm);
                            addInterface(para).then((res) => {

                                this.$message({
                                    message: "新增成功",
                                    type: 'success'
                                });
                                this.addFormVisible = false;
                                this.getInterfaceList();
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
                getInterfaceById(params).then(res=>{
                    this.editForm = res;
                });
                this.editFormVisible = true;
            },
            //编辑页面
            editSubmit: function(){
                this.editLoading = true;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('提示', {}).then(() => {
                            let para = Object.assign({}, this.editForm);
                            editInterface(para).then((res) => {
                                this.editLoading = false;
                                this.$message({
                                    message: "编辑成功",
                                    type: 'success'
                                });
                                this.editFormVisible = false;
                                this.getInterfaceList();
                            });
                        });
                    }
                });
                this.editLoading = false;
            },
            //归属服务切换
            handleServiceChange: function(){
                getSystemInfo().then(res=>{
                    let server_list = res.data;
                    let services = new Set();
                    for (let i = 0; i < server_list.length; i++) {
                        services.add(server_list[i].service_name)
                    }
                    services.add("crbt_admin");
                    let index = 0;
                    services.forEach(key=>{
                        this.interfacesServices[index] = {
                            label: key,
                            value: key
                        };
                        index = index + 1;
                    })
                });
            },
            //详情页面
            handlerDetails:function(index, row){
                this.detailsFormVisible = true;
                this.detailsForm = Object.assign({}, row);
            },
            //获取request、response信息并展示
            getDetailsFormInfo: function (index, row) {
                try{
                    this.jsonData = JSON.parse(this.detailsForm.response)
                }catch (e) {
                    this.jsonData = this.detailsForm.response
                }
                this.jsonDialogVisible = true
            },
            //复制request内容
            requestCopy: function () {
                this.$message({
                    message:"复制成功",
                    type: 'success'
                })
            }
        },
        mounted() {
            this.query.name = "";
            this.getInterfaceList();
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
