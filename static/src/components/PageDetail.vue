<template>
  <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">
    <el-form-item prop="content">
      <markdown-editor
        ref="editor"
        v-model="postForm.content"
        height="90vh"
        :options="{previewStyle: 'tab', hideModeSwitch: true}"
      />
    </el-form-item>

    <right-panel click-not-close>
      <el-form-item prop="title">
        <MDinput v-model="postForm.title" :maxlength="100" name="name" required>
          {{ $t('post.title') }}
        </MDinput>
      </el-form-item>

      <el-form-item :label="$t('post.slug')">
        <el-input v-model="postForm.slug" />
      </el-form-item>

      <el-form-item :label="$t('post.ptype')">
        <el-select v-model="postForm.ptype">
          <el-option :label="$t('post.markdown')" value="markdown" />
          <el-option :label="$t('post.html')" value="html" />
        </el-select>
      </el-form-item>

      <el-form-item :label="$t('post.display')">
        <el-select v-model="postForm.display">
          <el-option :label="$t('post.yes')" :value="true" />
          <el-option :label="$t('post.no')" :value="false" />
        </el-select>
      </el-form-item>

      <div style="margin-bottom:30px;">
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          {{ $t('post.save' ) }}
        </el-button>
      </div>

    </right-panel>
  </el-form>
</template>

<script>
import MarkdownEditor from '@/components/MarkdownEditor'
import MDinput from '@/components/MDinput'
import { fetchPage, createPage, updatePage } from '@/api/page'
import RightPanel from '@/components/RightPanel'

const defaultForm = {
  title: '', // 文章题目
  content: '', // 文章内容
  display: false,
  ptype: 'markdown'
}

export default {
  name: 'ArticleDetail',
  components: { MarkdownEditor, MDinput, RightPanel },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    const validateRequire = (rule, value, callback) => {
      if (value === '') {
        this.$message({
          message: rule.field + this.$t('post.missing'),
          type: 'error'
        })
        callback(new Error(rule.field + this.$t('post.missing')))
      } else {
        callback()
      }
    }
    return {
      postForm: Object.assign({}, defaultForm),
      loading: false,
      rules: {
        title: [{ validator: validateRequire }],
        content: [{ validator: validateRequire }],
        slug: [{ validator: validateRequire }]
      },
      tempRoute: {}
    }
  },
  created() {
    if (this.isEdit) {
      const id = this.$route.params && this.$route.params.id
      this.fetchData(id)
    } else {
      this.postForm = Object.assign({}, defaultForm)
    }

    // Why need to make a copy of this.$route here?
    // Because if you enter this page and quickly switch tag, may be in the execution of the setTagsViewTitle function, this.$route is no longer pointing to the current page
    // https://github.com/PanJiaChen/vue-element-admin/issues/1221
    this.tempRoute = Object.assign({}, this.$route)
  },
  methods: {
    fetchData(id) {
      fetchPage(id).then(response => {
        this.postForm = response.data
        // Set tagsview title
        this.setTagsViewTitle()
      }).catch(err => {
        console.log(err)
      })
    },
    setTagsViewTitle() {
      const title = this.lang === 'zh' ? '编辑页面' : 'Edit Page'
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    sendPage(data) {
      return (this.isEdit ? updatePage(data) : createPage(data))
    },
    submitForm() {
      this.$refs.postForm.validate(valid => {
        if (!valid) return
        this.sendPage(this.postForm).then(resp => {
          this.loading = true
          this.$notify({
            title: this.$t('post.success'),
            message: this.$t('post.successMessage'),
            type: 'success',
            duration: 2000
          })
          this.loading = false
        })
      })
    }
  }
}
</script>

<style lang="scss">
.sub-navbar {
  background: none;
}

.te-editor .CodeMirror {
  font-size: 16px;
}

.tui-editor-defaultUI {
  border-bottom: none;
}

@media (min-width: 980px) {
  .form-container {
    padding-right: 380px;
  }
}
</style>
