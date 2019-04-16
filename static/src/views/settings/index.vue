<template>
  <el-form ref="settingsForm" :model="settingsForm" :rules="rules" class="settings">
    <el-row :gutter="20">
      <el-col :sm="24" :md="12">
        <el-form-item prop="title">
          <MDinput v-model="settingsForm.name" :maxlength="100" name="name" required>
            Site Name
          </MDinput>
        </el-form-item>
        <el-form-item prop="description">
          <MDinput v-model="settingsForm.description" :maxlength="100" name="description" required>
            Site Description
          </MDinput>
        </el-form-item>
        <el-form-item label="Cover Image">
          <upload v-model="settingsForm.cover_url" :upload-image="uploadImage" />
        </el-form-item>
        <el-form-item label="Avatar">
          <avatar-upload v-model="settingsForm.avatar" :upload-image="uploadImage" />
        </el-form-item>
        <el-form-item label="Google Site Verification">
          <el-input v-model="settingsForm.google_site_verification" />
        </el-form-item>
        <el-form-item label="Google Analytics ID">
          <el-input v-model="settingsForm.google_analytics_id" />
        </el-form-item>
        <el-form-item label="Disqus Shortname">
          <el-input v-model="settingsForm.disqus_shortname" />
        </el-form-item>
        <el-form-item label="ICP Number">
          <el-input v-model="settingsForm.icp" />
        </el-form-item>
      </el-col>
      <el-col :sm="24" :md="12">
        <el-form-item label="Social Links">
          <el-row v-for="(item,n) in settingsForm.sociallinks" :key="n" :gutter="5" class="link-row">
            <el-col :span="6">
              <el-input v-model="item.name" placeholder="Name" />
            </el-col>
            <el-col :span="5">
              <el-input v-model="item.icon" placeholder="Icon" />
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

        <el-form-item label="Friend Links">
          <el-row v-for="(item,n) in settingsForm.links" :key="n" :gutter="5" class="link-row">
            <el-col :span="9">
              <el-input v-model="item.text" placeholder="Link Text" />
            </el-col>
            <el-col :span="12">
              <el-input v-model="item.link" placeholder="Link URL" />
            </el-col>
            <el-col :span="3">
              <el-button type="danger" icon="el-icon-delete" circle @click="deleteFriendLink(item)" />
            </el-col>
          </el-row>
          <el-button type="primary" class="add-btn" icon="el-icon-plus" circle @click="addFriendLink" />
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
import { getSettings } from '@/api/user'

const validateRequire = (rule, value, callback) => {
  if (value === '') {
    this.$message({
      message: rule.field + '为必填项',
      type: 'error'
    })
    callback(new Error(rule.field + '为必填项'))
  } else {
    callback()
  }
}

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
    return {
      settingsForm: { ...defaultSettings },
      rules: {
        name: [{ validator: validateRequire }],
        description: [{ validator: validateRequire }]
      }
    }
  },
  beforeDestroy() {
    console.log(this.settingsForm)
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
        this.settingsForm = resp.data
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
