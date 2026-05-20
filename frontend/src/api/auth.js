import api from './index'

export const authApi = {
  login(data) {
    return api.post('/login', data)
  },
  getCurrentUser() {
    return api.get('/users/me')
  }
}
