import Mock from 'mockjs'

const NameList = []
const count = 100

for (let i = 0; i < count; i++) {
  NameList.push(Mock.mock({
    name: '@first'
  }))
}
NameList.push({ name: 'mock-Pan' })
const TagList = ['test', 'python', 'algorithm', 'reading']

export default [
  // username search
  {
    url: '/categories',
    type: 'get',
    response: config => {
      return {
        code: 20000,
        data: {
          total: 2,
          items: [
            { id: 0, name: 'programming' },
            { id: 1, name: 'essay' }
          ]
        }
      }
    }
  },

  {
    url: '/tags',
    type: 'get',
    response: config => {
      const { name } = config.query
      const filteredList = TagList.filter(item => {
        return (item.toLowerCase().indexOf(name.toLowerCase()) > -1)
      })
      return {
        code: 20000,
        data: {
          total: filteredList.length,
          items: filteredList.map(v => {
            return { name: v }
          })
        }
      }
    }
  },

  // transaction list
  {
    url: '/transaction/list',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          total: 20,
          'items|20': [{
            order_no: '@guid()',
            timestamp: +Mock.Random.date('T'),
            username: '@name()',
            price: '@float(1000, 15000, 0, 2)',
            'status|1': ['success', 'pending']
          }]
        }
      }
    }
  }
]
