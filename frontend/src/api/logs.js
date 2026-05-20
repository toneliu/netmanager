import api from './index'

export const logsApi = {
  getLogs(params) {
    return api.get('/logs', { params })
  }
}
