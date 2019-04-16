import request from '@/utils/request'

export function fetchList(query) {
  return request({
    url: '/post',
    method: 'get',
    params: query
  })
}

export function fetchPost(id) {
  return request({
    url: '/post',
    method: 'get',
    params: { id }
  })
}

export function createPost(data) {
  return request({
    url: '/post',
    method: 'post',
    data
  })
}

export function updatePost(data) {
  return request({
    url: '/post',
    method: 'put',
    data
  })
}
