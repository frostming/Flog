import Mock from 'mockjs'

const List = []
const count = 100

const baseContent = '## Hello World\n我是测试数据我是测试数据\n\n![](https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943)\n'

for (let i = 0; i < count; i++) {
  List.push(Mock.mock({
    id: '@increment',
    title: '@title(5, 10)',
    content: baseContent,
    ptype: Mock.Random.pick(['markdown', 'html']),
    'comment|1': true,
    slug: '@domain',
    'display|1': true
  }))
}

export default [
  {
    url: '/page/\\d+',
    type: 'get',
    response: config => {
      return {
        code: 20000,
        data: List[0]
      }
    }
  },

  {
    url: '/page',
    type: 'get',
    response: config => {
      return {
        code: 20000,
        data: {
          total: List.length,
          items: List
        }
      }
    }
  },

  {
    url: '/page',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/page',
    type: 'put',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/page',
    type: 'delete',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
]
