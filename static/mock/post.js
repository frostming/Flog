import Mock from 'mockjs'

const List = []
const count = 100

const baseContent = '## Hello World\n我是测试数据我是测试数据\n\n![](https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943)\n'
const image_uri = 'https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3'

for (let i = 0; i < count; i++) {
  List.push(Mock.mock({
    id: '@increment',
    date: '@datetime',
    author: '@first',
    title: '@title(5, 10)',
    description: '@sentence',
    content: baseContent,
    'lang|1': ['zh', 'en'],
    type: Mock.Random.pick(['published', 'draft']),
    last_modified: '@datetime',
    'comment|1': true,
    image: image_uri,
    slug: '@domain',
    category: Mock.Random.pick(['programming', 'essay']),
    tags: [Mock.Random.pick(['test', 'python', 'algorithm', 'reading'])]
  }))
}

export default [
  {
    url: '/post',
    type: 'get',
    response: config => {
      if (config.query.hasOwnProperty('id')) {
        for (const article of List) {
          if (article.id === +config.query.id) {
            return {
              code: 20000,
              data: article
            }
          }
        }
        return
      }

      const { type, title, page = 1, limit = 20, sort } = config.query

      let mockList = List.filter(item => {
        if (type && type !== item.type) return false
        if (title && item.title.indexOf(title) < 0) return false
        return true
      })

      if (sort === '-id') {
        mockList = mockList.reverse()
      }

      const pageList = mockList.filter((item, index) => index < limit * page && index >= limit * (page - 1))

      return {
        code: 20000,
        data: {
          total: mockList.length,
          items: pageList
        }
      }
    }
  },

  {
    url: '/post',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/post',
    type: 'put',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
]
