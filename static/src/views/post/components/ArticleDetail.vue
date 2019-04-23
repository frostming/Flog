<template>
  <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">
    <el-form-item prop="content">
      <markdown-editor
        ref="editor"
        v-model="postForm.content"
        height="90vh"
        :upload-image="uploadImage"
        :options="{previewStyle: 'tab', hideModeSwitch: true}"
      />
    </el-form-item>

    <right-panel click-not-close>
      <el-form-item prop="title">
        <MDinput v-model="postForm.title" :maxlength="100" name="name" required>
          {{ $t('post.title') }}
        </MDinput>
      </el-form-item>
      <el-form-item prop="image" :label="$t('post.coverImage')">
        <upload v-model="postForm.image" :upload-image="uploadImage" />
      </el-form-item>

      <el-form-item :label="$t('post.author')" class="postInfo-container-item">
        <el-input v-model="postForm.author" :placeholder="$t('post.author')" />
      </el-form-item>
      <el-form-item :label="$t('post.description')">
        <el-input v-model="postForm.description" :rows="1" type="textarea" class="article-textarea" autosize :placeholder="$t('post.description')" />
      </el-form-item>
      <el-form-item :label="$t('post.slug')">
        <el-input v-model="postForm.slug" />
      </el-form-item>
      <el-form-item :label="$t('post.language')">
        <el-radio v-model="postForm.lang" label="zh">中文</el-radio>
        <el-radio v-model="postForm.lang" label="en">English</el-radio>
      </el-form-item>

      <el-form-item :label="$t('post.category')">
        <el-select v-model="postForm.category" style="width:100%" filterable allow-create>
          <el-option v-for="(item,id) in categoryOptions" :key="item+id" :label="item" :value="item" />
        </el-select>
      </el-form-item>

      <el-form-item :label="$t('post.tags')">
        <el-select v-model="postForm.tags" style="width:100%" multiple remote :remote-method="searchRemoteTags" filterable allow-create>
          <el-option v-for="(item,id) in tagOptions" :key="item+id" :label="item" :value="item" />
        </el-select>
      </el-form-item>

      <div style="margin-bottom:30px;">
        <CommentDropdown v-model="postForm.comment" />
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          {{ $t('post.publish' ) }}
        </el-button>
        <el-button v-loading="loading" type="warning" @click="draftForm">
          {{ $t('post.draft' ) }}
        </el-button>
      </div>
    </right-panel>
  </el-form>
</template>

<script>
import MarkdownEditor from '@/components/MarkdownEditor'
import Upload from '@/components/Upload/SingleImage'
import MDinput from '@/components/MDinput'
import { fetchPost, createPost, updatePost } from '@/api/post'
import { CommentDropdown } from './Dropdown'
import { categoryList, tagList } from '@/api/remote-search'
import RightPanel from '@/components/RightPanel'
import uploadData from '@/api/cos'

const defaultForm = {
  is_draft: true,
  title: '', // 文章题目
  content: '', // 文章内容
  description: '', // 文章摘要
  image: '', // 文章图片
  category: '',
  tags: [],
  lang: 'zh',
  comment: true
}

export default {
  name: 'ArticleDetail',
  components: { MarkdownEditor, MDinput, Upload, CommentDropdown, RightPanel },
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
        author: [{ validator: validateRequire }],
        slug: [{ validator: validateRequire }],
        category: [{ validator: validateRequire }]
      },
      categoryOptions: [],
      tagOptions: [],
      tempRoute: {}
    }
  },
  computed: {
    contentShortLength() {
      return this.postForm.description.length
    },
    lang() {
      return this.$store.getters.language
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
    this.fetchCategories()
  },
  methods: {
    fetchData(id) {
      fetchPost(id).then(response => {
        this.postForm = response.data
        // Just for test
        this.postForm.title += `   Article Id:${this.postForm.id}`
        this.postForm.description += `   Article Id:${this.postForm.id}`
        // Set tagsview title
        this.setTagsViewTitle()
      }).catch(err => {
        console.log(err)
      })
    },
    setTagsViewTitle() {
      const title = this.lang === 'zh' ? '编辑文章' : 'Edit Article'
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    fetchCategories() {
      categoryList().then(resp => {
        if (!resp.data.items) return
        this.categoryOptions = resp.data.items.map(v => v.name)
      })
    },
    searchRemoteTags(query) {
      console.log(query)
      tagList(query).then(resp => {
        if (!resp.data.items) return
        this.tagOptions = resp.data.items.map(v => v.name)
      })
    },
    uploadImage(fileObj, callbacks) {
      uploadData(fileObj, callbacks)
    },
    sendPost(data) {
      return (this.isEdit ? updatePost(data) : createPost(data))
    },
    submitForm() {
      this.$refs.postForm.validate(valid => {
        if (!valid) return
        this.sendPost({ type: 'published', ...this.postForm }).then(resp => {
          this.loading = true
          this.$notify({
            title: this.$t('post.success'),
            message: this.$t('post.successMessage'),
            type: 'success',
            duration: 2000
          })
          this.postForm.status = 'published'
          this.loading = false
        })
      })
    },
    draftForm() {
      if (this.postForm.content.length === 0 || this.postForm.title.length === 0) {
        this.$message({
          message: this.$t('post.missingField'),
          type: 'warning'
        })
        return
      }
      this.sendPost({ type: 'draft', ...this.postForm }).then(resp => {
        this.$message({
          message: this.$t('post.saveSuccess'),
          type: 'success',
          showClose: true,
          duration: 1000
        })
        this.postForm.status = 'draft'
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
</style>
