import api from './index'

export const dashboardApi = {
  getStats() {
    return api.get('/dashboard/stats')
  }
}
