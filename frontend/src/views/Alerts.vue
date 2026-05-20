<template>
  <div class="alerts">
    <el-card>
      <div class="toolbar">
        <el-select v-model="onlyActive" placeholder="筛选" style="width: 200px" @change="loadAlerts">
          <el-option label="只显示活动告警" :value="true" />
          <el-option label="显示全部" :value="false" />
        </el-select>
        <el-button @click="loadAlerts">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <el-table :data="alerts" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="alert_type" label="类型" width="120" />
        <el-table-column prop="message" label="消息" />
        <el-table-column prop="severity" label="严重程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getSeverityType(row.severity)" size="small">
              {{ getSeverityLabel(row.severity) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_resolved" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_resolved ? 'info' : 'danger'" size="small">
              {{ row.is_resolved ? '已解决' : '活动' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" v-if="authStore.isAdmin">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="resolveAlert(row)" v-if="!row.is_resolved">
              解决
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { alertsApi } from '@/api/alerts'
import { useAuthStore } from '@/stores/auth'
import { Refresh } from '@element-plus/icons-vue'

const authStore = useAuthStore()

const alerts = ref([])
const loading = ref(false)
const onlyActive = ref(true)

const getSeverityType = (severity) => {
  const types = {
    critical: 'danger',
    warning: 'warning',
    info: 'info'
  }
  return types[severity] || 'info'
}

const getSeverityLabel = (severity) => {
  const labels = {
    critical: '严重',
    warning: '警告',
    info: '信息'
  }
  return labels[severity] || severity
}

const formatDate = (date) => {
  return new Date(date).toLocaleString('zh-CN')
}

const loadAlerts = async () => {
  loading.value = true
  try {
    const response = await alertsApi.getAlerts(onlyActive.value)
    alerts.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const resolveAlert = async (alert) => {
  try {
    await alertsApi.resolveAlert(alert.id)
    ElMessage.success('告警已标记为已解决')
    loadAlerts()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadAlerts()
})
</script>

<style scoped>
.alerts {
  padding: 0;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
</style>
