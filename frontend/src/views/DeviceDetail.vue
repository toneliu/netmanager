<template>
  <div class="device-detail">
    <el-page-header @back="$router.back()" content="返回">
      <template #title>
        <span style="font-size: 20px; font-weight: bold">{{ device?.name || '设备详情' }}</span>
      </template>
    </el-page-header>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>
          <div class="info-item">
            <span class="label">设备名称:</span>
            <span>{{ device?.name }}</span>
          </div>
          <div class="info-item">
            <span class="label">IP地址:</span>
            <span>{{ device?.ip }}</span>
          </div>
          <div class="info-item">
            <span class="label">厂商:</span>
            <span>{{ device?.vendor }}</span>
          </div>
          <div class="info-item">
            <span class="label">型号:</span>
            <span>{{ device?.model }}</span>
          </div>
          <div class="info-item">
            <span class="label">状态:</span>
            <el-tag :type="getStatusType(device?.status)" size="small">
              {{ getStatusLabel(device?.status) }}
            </el-tag>
          </div>
          <div class="info-item">
            <span class="label">位置:</span>
            <span>{{ device?.location }}</span>
          </div>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>端口列表</span>
            </div>
          </template>
          <el-table :data="ports" style="width: 100%" size="small">
            <el-table-column prop="port_name" label="端口" width="120" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="vlan" label="VLAN" width="80" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.status === 'up' ? 'success' : 'info'" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="speed" label="速率" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>配置备份</span>
              <el-button type="primary" size="small" @click="backupConfig" v-if="authStore.isAdmin">
                <el-icon><Download /></el-icon>
                立即备份
              </el-button>
            </div>
          </template>
          <el-table :data="configs" style="width: 100%" size="small">
            <el-table-column prop="version" label="版本" width="80" />
            <el-table-column prop="backup_time" label="备份时间" width="200">
              <template #default="{ row }">
                {{ formatDate(row.backup_time) }}
              </template>
            </el-table-column>
            <el-table-column prop="config_text" label="配置预览" show-overflow-tooltip />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="showConfig(row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>监控指标 (最近24小时)</span>
            </div>
          </template>
          <div ref="chartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="configDialogVisible" title="配置详情" width="800px">
      <pre style="background: #f5f5f5; padding: 16px; border-radius: 4px; overflow: auto; max-height: 400px">{{ currentConfig?.config_text }}</pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { devicesApi } from '@/api/devices'
import { useAuthStore } from '@/stores/auth'
import { Download } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const route = useRoute()
const authStore = useAuthStore()

const device = ref(null)
const ports = ref([])
const configs = ref([])
const metrics = ref([])
const chartRef = ref(null)
let chart = null
const configDialogVisible = ref(false)
const currentConfig = ref(null)

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

const formatDate = (date) => {
  return new Date(date).toLocaleString('zh-CN')
}

const loadDevice = async () => {
  try {
    const response = await devicesApi.getDevice(route.params.id)
    device.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const loadPorts = async () => {
  try {
    const response = await devicesApi.getDevicePorts(route.params.id)
    ports.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const loadConfigs = async () => {
  try {
    const response = await devicesApi.getDeviceConfigs(route.params.id)
    configs.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const loadMetrics = async () => {
  try {
    const response = await devicesApi.getDeviceMetrics(route.params.id, 24)
    metrics.value = response.data
    renderChart()
  } catch (error) {
    console.error(error)
  }
}

const backupConfig = async () => {
  try {
    await devicesApi.backupConfig(route.params.id)
    ElMessage.success('配置备份成功')
    loadConfigs()
  } catch (error) {
    console.error(error)
  }
}

const showConfig = (config) => {
  currentConfig.value = config
  configDialogVisible.value = true
}

const renderChart = async () => {
  await nextTick()
  if (!chartRef.value) return
  
  if (chart) {
    chart.dispose()
  }
  
  chart = echarts.init(chartRef.value)
  
  const times = metrics.value.map(m => new Date(m.recorded_at).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }))
  const cpuData = metrics.value.map(m => m.cpu_usage)
  const memData = metrics.value.map(m => m.mem_usage)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['CPU使用率', '内存使用率']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: times
    },
    yAxis: {
      type: 'value',
      max: 100,
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: 'CPU使用率',
        type: 'line',
        smooth: true,
        data: cpuData,
        color: '#1e3a8a'
      },
      {
        name: '内存使用率',
        type: 'line',
        smooth: true,
        data: memData,
        color: '#0891b2'
      }
    ]
  }
  
  chart.setOption(option)
}

onMounted(() => {
  loadDevice()
  loadPorts()
  loadConfigs()
  loadMetrics()
})
</script>

<style scoped>
.device-detail {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  color: #666;
}
</style>
