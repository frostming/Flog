import request from '@/utils/request'

export function fetchList() {
  return request({
    url: '/page',
    method: 'get'
  })
}

export function fetchPage(id) {
  return request({
    url: `/page/${id}`,
    method: 'get'
  })
}

export function createPage(data) {
  return request({
    url: '/page',
    method: 'post',
    data
  })
}

export function updatePage(data) {
  return request({
    url: `/page/${data.id}`,
    method: 'put',
    data
  })
}

export function deletePage(id) {
  return request({
    url: `/page/${id}`,
    method: 'delete'
  })
}
