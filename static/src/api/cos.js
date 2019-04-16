import request from '@/utils/request'
import COS from 'cos-js-sdk-v5'

const cos = new COS({
  getAuthorization: (options, callback) => {
    request({
      url: '/token/cos',
      method: 'get'
    }).then(data => {
      callback({
        TmpSecretId: data.credentials.tmpSecretId,
        TmpSecretKey: data.credentials.tmpSecretKey,
        XCosSecurityToken: data.credentials.sessionToken,
        ExpiredTime: data.expiredTime
      })
    })
  }
})
console.log(cos)

export default (request, { success, error, progress }) => {
  let p = 0
  const timer = setInterval(() => {
    p += 0.25
    if (progress) {
      progress(p)
    }
    if (p === 1) {
      clearInterval(timer)
      success('https://frostming.com/images/2018-09-pipenv.jpg')
    }
  }, 1000)
}
