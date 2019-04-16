<template>
  <el-upload
    class="avatar-uploader"
    action="https://jsonplaceholder.typicode.com/posts/"
    :multiple="false"
    :show-file-list="false"
    :before-upload="beforeAvatarUpload"
    :http-request="handleUpload"
  >
    <img v-if="value" :src="value" class="avatar">
    <i v-else class="el-icon-plus avatar-uploader-icon" />
  </el-upload>
</template>

<style lang="scss">
  @import "~@/styles/mixin.scss";
  .avatar-uploader {
    @include clearfix;

    .el-upload {
      border: 1px dashed #d9d9d9;
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;

      &:hover {
        border-color: #409EFF;
      }
    }
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>

<script>
export default {
  props: {
    value: {
      type: String,
      default: ''
    },
    uploadImage: {
      type: Function,
      default: null
    }
  },
  methods: {
    beforeAvatarUpload(file) {
      const isJPGPNG = ['image/jpeg', 'image/png'].indexOf(file.type) >= 0
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPGPNG) {
        this.$message.error('Only JPG and PNG format are allowed!')
      }
      if (!isLt2M) {
        this.$message.error('The file size should be less than 2M!')
      }
      return isJPGPNG && isLt2M
    },
    handleUpload(request) {
      if (!this.uploadImage) return
      const _self = this

      this.uploadImage(request.file, {
        success(val) {
          _self.$emit('input', val)
        },
        error(val) {
          _self.$message({
            message: 'Upload failed: ' + val,
            type: 'danger'
          })
        }
      })
    }
  }
}
</script>
