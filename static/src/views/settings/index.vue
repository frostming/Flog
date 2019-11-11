<template>
  <el-form ref="settingsForm" :model="settingsForm" :rules="rules" class="settings">
    <el-row :gutter="20">
      <el-col :sm="24" :md="12">
        <el-form-item prop="title">
          <MDinput v-model="settingsForm.name" :maxlength="100" name="name" required>
            {{ $t('settings.siteName') }}
          </MDinput>
        </el-form-item>
        <el-form-item prop="description">
          <MDinput v-model="settingsForm.description" :maxlength="100" name="description" required>
            {{ $t('settings.description') }}
          </MDinput>
        </el-form-item>
        <el-form-item :label="$t('post.coverImage')">
          <upload v-model="settingsForm.cover_url" :upload-image="uploadImage" />
        </el-form-item>
        <el-form-item :label="$t('settings.avatar')">
          <avatar-upload v-model="settingsForm.avatar" :upload-image="uploadImage" />
        </el-form-item>
        <el-form-item :label="$t('settings.icp')">
          <el-input v-model="settingsForm.icp" />
        </el-form-item>
      </el-col>
      <el-col :sm="24" :md="12">
        <el-form-item :label="$t('settings.socialLinks')">
          <el-row v-for="(item,n) in settingsForm.sociallinks" :key="n" :gutter="5" class="link-row">
            <el-col :span="6">
              <el-input v-model="item.name" :placeholder="$t('settings.name')" />
            </el-col>
            <el-col :span="5">
              <el-input v-model="item.icon" :placeholder="$t('settings.icon')" />
            </el-col>
            <el-col :span="10">
              <el-input v-model="item.link" placeholder="URL" />
            </el-col>
            <el-col :span="3">
              <el-button type="danger" icon="el-icon-delete" circle @click="deleteSocialLink(item)" />
            </el-col>
          </el-row>
          <el-button type="primary" class="add-btn" icon="el-icon-plus" circle @click="addSocialLink" />
        </el-form-item>

        <el-form-item :label="$t('settings.friendLinks')">
          <el-row v-for="(item,n) in settingsForm.links" :key="n" :gutter="5" class="link-row">
            <el-col :span="9">
              <el-input v-model="item.text" :placeholder="$t('settings.text')" />
            </el-col>
            <el-col :span="12">
              <el-input v-model="item.url" :placeholder="$t('settings.url')" />
            </el-col>
            <el-col :span="3">
              <el-button type="danger" icon="el-icon-delete" circle @click="deleteFriendLink(item)" />
            </el-col>
          </el-row>
          <el-button type="primary" class="add-btn" icon="el-icon-plus" circle @click="addFriendLink" />
        </el-form-item>

        <el-form-item :label="$t('settings.donate')">
          <avatar-upload v-model="settingsForm.donate" :upload-image="uploadImage" />
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<script>
import MDinput from '@/components/MDinput'
import Upload from '@/components/Upload/SingleImage'
import uploadData from '@/api/cos'
import AvatarUpload from './components/AvatarUpload'
import { getSettings, updateSettings } from '@/api/user'

const defaultSettings = {
  avatar: 'https://frostming.com/static/images/favicon.png',
  cover_url: 'https://frostming.com/images/2019-03-john-westrock-638048-unsplash.jpg',
  sociallinks: [],
  links: []
}

export default {
  name: 'Settings',
  components: { MDinput, Upload, AvatarUpload },
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
      settingsForm: { ...defaultSettings },
      rules: {
        name: [{ validator: validateRequire }],
        description: [{ validator: validateRequire }]
      }
    }
  },
  beforeDestroy() {
    this.submitForm()
  },
  mounted() {
    this.fetchSettings()
  },
  methods: {
    uploadImage(fileObj, callbacks) {
      uploadData(fileObj, callbacks)
    },
    addSocialLink() {
      this.settingsForm.sociallinks.push({
        name: '',
        icon: '',
        url: ''
      })
    },
    addFriendLink() {
      this.settingsForm.links.push({
        text: '',
        url: ''
      })
    },
    deleteSocialLink(item) {
      this.settingsForm.sociallinks.splice(this.settingsForm.sociallinks.indexOf(item), 1)
    },
    deleteFriendLink(item) {
      this.settingsForm.links.splice(this.settingsForm.links.indexOf(item), 1)
    },
    fetchSettings() {
      getSettings().then(resp => {
        this.settingsForm = { ...this.settingsForm, ...(resp.data || {}) }
      })
    },
    submitForm() {
      this.$refs.settingsForm.validate(valid => {
        if (!valid) return
        updateSettings(this.settingsForm)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.settings {
  padding: 10px 5px;

  @media (min-width: 992px){
    padding: 50px;
  };

  .material-input__component {
    margin-top: 12px;
  }
}
.link-row {
  clear: both;
  margin-bottom: 10px;
}

.add-btn {
  clear: both;
  display: block;
}
</style>
