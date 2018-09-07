(function(){
  var imgButton = document.querySelector("a[title^='Insert Image']")
  imgButton.onclick = null
  imgButton.style.position = "relative"
  var inputEle = document.createElement('input')
  inputEle.setAttribute('type', 'file')
  inputEle.setAttribute('accept', 'image/*')
  inputEle.style.position = "absolute"
  inputEle.style.opacity = "0"
  inputEle.style.left = "0"
  inputEle.style.cursor = "pointer"
  inputEle.style.width = "100%"
  inputEle.style.height = "100%"
  imgButton.appendChild(inputEle)

  var cos = new COS({
    getAuthorization: function(options, callback) {
      $.get('/upload-token', {
        method: (options.Method || 'get').toLowerCase(),
        path: '/' + (options.Key || '')
      }, function(authorization) {
        callback(authorization);
      }, 'text')
    }
  })

  inputEle.onchange = function() {
    var file = this.files[0]
    if(!file) return
    var date = new Date().toISOString().slice(0, 7)
    cos.sliceUploadFile({
      Bucket: window.cosConfig.bucket,
      Region: window.cosConfig.region,
      Key: date + '-' + file.name,
      Body: file,
    }, function(error) {
      if(!error) {
        simplemde.codemirror.replaceSelection(`![](/images/${date}-${file.name})`)
      }
    })
  }
})()
