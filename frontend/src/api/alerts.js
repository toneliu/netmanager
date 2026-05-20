import api from './index'

export const alertsApi = {
  getAlerts(onlyActive = true) {
    return api.get('/alerts', { params: { only_active: onlyActive } })
  },
  resolveAlert(id) {
    return api.put(`/alerts/${id}/resolve`)
  }
}
