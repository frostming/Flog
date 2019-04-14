<template>
  <div class="upload-container">
    <div v-if="imageUrl" class="image-cover" :style="{backgroundImage: `url(${imageUrl})`}">
      <i class="el-icon-delete" @click="rmImage" />
    </div>
    <template v-else>
      <el-upload
        v-if="mode==='Upload'"
        :multiple="false"
        :show-file-list="false"
        :http-request="handleUpload"
        class="image-uploader"
        drag
        action="https://httpbin.org/post"
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <div class="switch-mode">
          <a href="#" @click="changeMode('URL')"><i class="el-icon-arrow-right" />Input URL</a>
        </div>
      </el-upload>
      <div v-else class="image-input">
        <el-input placeholder="Image URL" :value="value" @input="emitInput" />
        <div class="switch-mode">
          <a href="#" @click="changeMode('Upload')"><i class="el-icon-arrow-right" />Drag/Upload</a>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
// 预览效果见付费文章
import uploadImage from '@/api/cos'

export default {
  name: 'SingleImageUpload',
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      mode: 'Upload'
    }
  },
  computed: {
    imageUrl() {
      return this.value
    }
  },
  methods: {
    rmImage() {
      this.emitInput('')
    },
    emitInput(val) {
      this.$emit('input', val)
    },
    handleUpload(request) {
      uploadImage(request).then(url => {
        this.emitInput(url)
      })
    },
    changeMode(mode) {
      this.mode = mode
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "~@/styles/mixin.scss";
  .upload-container {
    width: 100%;
    position: relative;
    clear: both;
    @include clearfix;
  }
  .image-cover {
    width: 100%;
    height: 200px;
    background: center center no-repeat;
    background-size: cover;
    text-align: right;
    padding: 0 5px;

    .el-icon-delete {
      font-size: 36px;
      cursor: pointer;
    }
  }

  .image-input {
    width: 100%;
    height: 200px;
    text-align: center;
    padding: 60px 5px 0px;
  }
</style>
