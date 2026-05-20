<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card total">
          <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="40"><Monitor /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_devices }}</div>
            <div class="stat-label">设备总数</div>
          </div>
        </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card online">
          <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="40"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.online_devices }}</div>
            <div class="stat-label">在线设备</div>
          </div>
        </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card offline">
          <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="40"><CircleClose /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.offline_devices }}</div>
            <div class="stat-label">离线设备</div>
          </div>
        </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card alert">
          <div class="stat-content">
          <div class="stat-icon">
            <el-icon :size="40"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.active_alerts }}</div>
            <div class="stat-label">活动告警</div>
          </div>
        </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快速操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/devices')">
              <el-icon><Plus /></el-icon>
              查看设备
            </el-button>
            <el-button type="success" @click="$router.push('/alerts')">
              <el-icon><Bell /></el-icon>
              处理告警
            </el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统信息</span>
            </div>
          </template>
          <div class="system-info">
            <p><strong>系统版本:</strong> NetManager v1.0.0</p>
            <p><strong>API服务:</strong> 正常运行</p>
            <p><strong>最后更新:</strong> {{ lastUpdate }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dashboardApi } from '@/api/dashboard'
import { Monitor, CircleCheck, CircleClose, Warning, Plus, Bell } from '@element-plus/icons-vue'

const stats = ref({
  total_devices: 0,
  online_devices: 0,
  offline_devices: 0,
  active_alerts: 0
})
const lastUpdate = ref('')

const loadStats = async () => {
  try {
    const response = await dashboardApi.getStats()
    stats.value = response.data
    lastUpdate.value = new Date().toLocaleString('zh-CN')
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stat-card {
  border: none;
  overflow: hidden;
}

.stat-card :deep(.el-card__body) {
  padding: 24px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
}

.total .stat-icon {
  color: #1e3a8a;
}

.online .stat-icon {
  color: #10b981;
}

.offline .stat-icon {
  color: #ef4444;
}

.alert .stat-icon {
  color: #f59e0b;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #1f2937;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.total {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.online {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}

.offline {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
}

.alert {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.card-header {
  font-weight: 600;
  color: #1f2937;
}

.quick-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.quick-actions .el-button {
  display: flex;
  align-items: center;
  gap: 6px;
}

.system-info p {
  margin: 8px 0;
  color: #374151;
}
</style>
