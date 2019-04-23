import request from '@/utils/request'

export function categoryList() {
  return request({
    url: '/categories',
    method: 'get'
  })
}

export function tagList(name) {
  return request({
    url: '/tags',
    method: 'get',
    params: { name }
  })
}

export function transactionList(query) {
  return request({
    url: '/transaction/list',
    method: 'get',
    params: query
  })
}
