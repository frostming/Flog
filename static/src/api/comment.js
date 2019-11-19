import request from '@/utils/request'

export function fetchList() {
  return request({
    url: '/comment',
    method: 'get'
  })
}

export function deleteComment(id) {
  return request({
    url: `/comment/${id}`,
    method: 'delete'
  })
}
