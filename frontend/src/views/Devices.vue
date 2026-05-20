<template>
  <div class="devices">
    <el-card>
      <div class="toolbar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索设备名称或IP"
          prefix-icon="Search"
          style="width: 300px"
          clearable
          @input="loadDevices"
        />
        <el-select v-model="statusFilter" placeholder="状态筛选" clearable style="width: 150px" @change="loadDevices">
          <el-option label="全部" value="" />
          <el-option label="在线" value="online" />
          <el-option label="离线" value="offline" />
          <el-option label="维护中" value="maintenance" />
        </el-select>
        <el-button type="primary" @click="showCreateDialog" v-if="authStore.isAdmin">
          <el-icon><Plus /></el-icon>
          添加设备
        </el-button>
        <el-button @click="loadDevices">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <el-table :data="devices" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="设备名称" />
        <el-table-column prop="ip" label="IP地址" />
        <el-table-column prop="vendor" label="厂商" />
        <el-table-column prop="model" label="型号" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="位置" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDevice(row.id)">查看</el-button>
            <el-button type="primary" link @click="showEditDialog(row)" v-if="authStore.isAdmin">编辑</el-button>
            <el-button type="danger" link @click="deleteDevice(row)" v-if="authStore.isAdmin">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑设备' : '添加设备'" width="600px">
      <el-form :model="deviceForm" :rules="deviceRules" ref="deviceFormRef" label-width="100px">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="deviceForm.name" />
        </el-form-item>
        <el-form-item label="IP地址" prop="ip">
          <el-input v-model="deviceForm.ip" />
        </el-form-item>
        <el-form-item label="厂商" prop="vendor">
          <el-select v-model="deviceForm.vendor" style="width: 100%">
            <el-option label="Cisco" value="Cisco" />
            <el-option label="Juniper" value="Juniper" />
            <el-option label="Huawei" value="Huawei" />
            <el-option label="Arista" value="Arista" />
            <el-option label="其他" value="Other" />
          </el-select>
        </el-form-item>
        <el-form-item label="型号" prop="model">
          <el-input v-model="deviceForm.model" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="deviceForm.status" style="width: 100%">
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
            <el-option label="维护中" value="maintenance" />
          </el-select>
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="deviceForm.location" />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="deviceForm.notes" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDevice" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { devicesApi } from '@/api/devices'
import { useAuthStore } from '@/stores/auth'
import { Plus, Refresh, Search } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const devices = ref([])
const loading = ref(false)
const saving = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const deviceFormRef = ref(null)
const editId = ref(null)

const deviceForm = ref({
  name: '',
  ip: '',
  vendor: '',
  model: '',
  status: 'online',
  location: '',
  notes: ''
})

const deviceRules = {
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  ip: [{ required: true, message: '请输入IP地址', trigger: 'blur' }]
}

const getStatusType = (status) => {
  const types = {
    online: 'success',
    offline: 'danger',
    maintenance: 'warning'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status) => {
  const labels = {
    online: '在线',
    offline: '离线',
    maintenance: '维护中'
  }
  return labels[status] || status
}

const loadDevices = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchQuery.value) params.search = searchQuery.value
    if (statusFilter.value) params.status = statusFilter.value
    const response = await devicesApi.getDevices(params)
    devices.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const viewDevice = (id) => {
  router.push(`/devices/${id}`)
}

const showCreateDialog = () => {
  isEdit.value = false
  editId.value = null
  deviceForm.value = {
    name: '',
    ip: '',
    vendor: '',
    model: '',
    status: 'online',
    location: '',
    notes: ''
  }
  dialogVisible.value = true
}

const showEditDialog = (device) => {
  isEdit.value = true
  editId.value = device.id
  deviceForm.value = { ...device }
  dialogVisible.value = true
}

const saveDevice = async () => {
  await deviceFormRef.value?.validate()
  saving.value = true
  try {
    if (isEdit.value) {
      await devicesApi.updateDevice(editId.value, deviceForm.value)
      ElMessage.success('设备更新成功')
    } else {
      await devicesApi.createDevice(deviceForm.value)
      ElMessage.success('设备添加成功')
    }
    dialogVisible.value = false
    loadDevices()
  } catch (error) {
    console.error(error)
  } finally {
    saving.value = false
  }
}

const deleteDevice = async (device) => {
  try {
    await ElMessageBox.confirm(`确定要删除设备 "${device.name}" 吗?`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await devicesApi.deleteDevice(device.id)
    ElMessage.success('设备删除成功')
    loadDevices()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  }
}

onMounted(() => {
  loadDevices()
})
</script>

<style scoped>
.devices {
  padding: 0;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
</style>
