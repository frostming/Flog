import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

export function getSettings() {
  return request({
    url: '/settings',
    method: 'get'
  })
}

export function changeTheme(value) {
  return request({
    url: '/settings/theme',
    method: 'post',
    data: { value }
  })
}

export function changeLanguage(value) {
  return request({
    url: '/settings/language',
    method: 'post',
    data: { value }
  })
}

export function getTheme() {
  return request({
    url: '/settings/theme',
    method: 'get'
  }).then(resp => resp.data.value)
}

export function getLanguage() {
  return request({
    url: '/settings/language',
    method: 'get'
  }).then(resp => resp.data.value)
}
