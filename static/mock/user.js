import Mock from 'mockjs'

const tokens = {
  admin: {
    token: 'admin-token'
  },
  editor: {
    token: 'editor-token'
  }
}

const users = {
  'admin-token': {
    roles: ['admin'],
    introduction: 'I am a super administrator',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Super Admin'
  },
  'editor-token': {
    roles: ['editor'],
    introduction: 'I am an editor',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Normal Editor'
  }
}

const settings = {
  name: Mock.Random.word(),
  avatar: 'https://frostming.com/static/images/favicon.png',
  cover_url: 'https://frostming.com/images/2019-03-john-westrock-638048-unsplash.jpg',
  sociallinks: Array(Mock.Random.integer(3, 5)).fill().map(_ => {
    return {
      name: Mock.Random.word(),
      icon: Mock.Random.word(),
      link: Mock.Random.url()
    }
  }),
  links: Array(Mock.Random.integer(3, 5)).fill().map(_ => {
    return {
      text: Mock.Random.word(),
      link: Mock.Random.url()
    }
  })
}

export default [
  // user login
  {
    url: '/user/login',
    type: 'post',
    response: config => {
      const { username } = config.body
      const token = tokens[username]

      // mock error
      if (!token) {
        return {
          code: 60204,
          message: 'Account and password are incorrect.'
        }
      }

      return {
        code: 20000,
        data: token
      }
    }
  },

  // get user info
  {
    url: '/user/info\.*',
    type: 'get',
    response: config => {
      const { token } = config.query
      const info = users[token]

      // mock error
      if (!info) {
        return {
          code: 50008,
          message: 'Login failed, unable to get user details.'
        }
      }

      return {
        code: 20000,
        data: info
      }
    }
  },

  // user logout
  {
    url: '/user/logout',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/settings/theme',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: { value: '#4D619A' }
      }
    }
  },
  {
    url: '/settings/language',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: { value: 'zh' }
      }
    }
  },
  {
    url: '/settings',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: settings
      }
    }
  },
  {
    url: '/settings/\.*',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
]
