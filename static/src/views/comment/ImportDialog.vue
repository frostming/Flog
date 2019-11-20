<template>
  <el-dialog
    :title="$t('post.import')"
    :visible.sync="dialogVisible"
  >
    <el-upload
      ref="upload"
      action="/api/comment/import"
      :data="{type}"
      :headers="headers"
      :on-success="showSuccess"
      :on-error="showError"
      :multiple="false"
      :limit="1"
      :auto-upload="false"
    >
      <el-button slot="trigger" type="primary">{{ $t('post.pickFile') }}</el-button>
      <el-button style="margin-left: 10px;" type="success" @click="submitUpload">{{ $t('post.upload') }}</el-button>
    </el-upload>
    <p>{{ $t('post.format') }}</p>
    <el-radio v-model="type" label="disqus">Disqus</el-radio>
  </el-dialog>
</template>

<script>
import { getToken } from '@/utils/auth'

export default {
  name: 'ImportDialog',
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      type: 'disqus'
    }
  },
  computed: {
    dialogVisible: {
      get() {
        return this.visible
      },
      set(val) {
        this.$emit('update:visible', val)
      }
    },
    headers() {
      return { 'X-Token': getToken() }
    }
  },
  methods: {
    submitUpload() {
      this.$refs.upload.submit()
    },
    showSuccess() {
      this.dialogVisible = false
      this.$message({
        type: 'success',
        message: this.$t('post.uploadSuccess')
      })
      this.$emit('success')
    },
    showError(e) {
      this.$message({
        type: 'danger',
        message: this.$t('post.uploadError') + ': ' + e
      })
    }
  }
}
</script>

<style lang="css" scoped>
</style>
