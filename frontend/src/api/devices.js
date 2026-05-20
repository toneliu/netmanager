import api from './index'

export const devicesApi = {
  getDevices(params) {
    return api.get('/devices', { params })
  },
  getDevice(id) {
    return api.get(`/devices/${id}`)
  },
  createDevice(data) {
    return api.post('/devices', data)
  },
  updateDevice(id, data) {
    return api.put(`/devices/${id}`, data)
  },
  deleteDevice(id) {
    return api.delete(`/devices/${id}`)
  },
  getDeviceConfigs(id) {
    return api.get(`/devices/${id}/configs`)
  },
  backupConfig(id) {
    return api.post(`/devices/${id}/backup_config`)
  },
  getDevicePorts(id) {
    return api.get(`/devices/${id}/ports`)
  },
  getDeviceMetrics(id, hours = 24) {
    return api.get(`/devices/${id}/metrics`, { params: { hours } })
  }
}
