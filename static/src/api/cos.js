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

export default (request) => {
  return new Promise((resolve) => {
    resolve('https://frostming.com/images/2019-03-john-westrock-638048-unsplash.jpg')
  })
}
