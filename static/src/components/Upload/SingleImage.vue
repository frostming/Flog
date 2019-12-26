<template>
  <div class="upload-container">
    <div v-if="show" class="image-cover" :style="{backgroundImage: `url(${value})`}">
      <i class="el-icon-close" @click="rmImage" />
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
        <el-progress
          v-if="loading"
          type="circle"
          :percentage="progress"
          :color="theme"
          style="margin-top: 37px"
        />
        <template v-else>
          <i class="el-icon-upload" />
          <div class="el-upload__text">
            {{ $t('post.dragImage') }}<em>{{ $t('post.clickToUpload') }}</em>
          </div>
          <div class="switch-mode">
            <a href="#" @click.stop="changeMode('URL')"><i class="el-icon-arrow-right" />{{ $t('post.inputURL') }}</a>
          </div>
        </template>
      </el-upload>
      <div v-else class="image-input">
        <el-input :placeholder="$t('post.imageURL')" :value="value" @input="emitInput" />
        <div class="switch-mode">
          <a href="#" @click.stop="changeMode('Upload')"><i class="el-icon-arrow-right" />{{ $t('post.dragUpload') }}</a>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
// 预览效果见付费文章
export default {
  name: 'SingleImageUpload',
  props: {
    value: {
      type: String,
      default: ''
    },
    uploadImage: {
      type: Function,
      required: false,
      default: null
    }
  },
  data() {
    return {
      mode: 'Upload',
      loading: false,
      progress: 0
    }
  },
  computed: {
    theme() {
      return this.$store.state.settings.theme
    },
    show() {
      return (this.value && this.mode === 'Upload')
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
      if (!this.uploadImage) return
      const _self = this
      this.loading = true
      this.progress = 0
      this.uploadImage(request.file, {
        success(val) {
          _self.emitInput(val)
          _self.loading = false
        },
        progress(val) {
          _self.progress = parseFloat(val) * 100
        },
        error(val) {
          _self.$message({
            message: 'Upload failed: ' + val,
            type: 'danger'
          })
        }
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

    .el-icon-close {
      font-size: 24px;
      cursor: pointer;
      display: none;
      border-radius: 50%;
      color: white;
      background-color: black;
    }

    &:hover .el-icon-close {
      display: inline;
    }
  }

  .image-input {
    width: 100%;
    height: 200px;
    text-align: center;
    padding: 60px 5px 0px;
  }
</style>
