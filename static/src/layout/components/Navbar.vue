<template>
  <div class="navbar">
    <hamburger id="hamburger-container" :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar" />

    <breadcrumb id="breadcrumb-container" class="breadcrumb-container" />

    <div class="right-menu">
      <template v-if="device!=='mobile'">
        <search id="header-search" class="right-menu-item" />

        <error-log class="errLog-container right-menu-item hover-effect" />

        <screenfull id="screenfull" class="right-menu-item hover-effect" />

        <el-tooltip :content="$t('navbar.size')" effect="dark" placement="bottom">
          <size-select id="size-select" class="right-menu-item hover-effect" />
        </el-tooltip>

        <lang-select class="right-menu-item hover-effect" />
        <theme-picker class="right-menu-item hover-effect" />

      </template>

      <el-dropdown class="avatar-container right-menu-item hover-effect" trigger="click">
        <div class="avatar-wrapper">
          <img :src="avatar+'?imageView2/1/w/80/h/80'" class="user-avatar">
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu slot="dropdown">
          <router-link to="/">
            <el-dropdown-item>
              {{ $t('navbar.dashboard') }}
            </el-dropdown-item>
          </router-link>
          <a target="_blank" href="https://github.com/frostming/Flog">
            <el-dropdown-item>
              {{ $t('navbar.github') }}
            </el-dropdown-item>
          </a>
          <el-dropdown-item divided>
            <span style="display:block;" @click="passwordDialog = true">{{ $t('navbar.changePassword') }}</span>
          </el-dropdown-item>
          <el-dropdown-item>
            <span style="display:block;" @click="logout">{{ $t('navbar.logOut') }}</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-dialog
        :title="$t('navbar.changePassword')"
        :visible.sync="passwordDialog"
        width="480px"
        :modal-append-to-body="false"
      >
        <el-form ref="passwordForm" :model="passwordForm" :rules="rules">
          <el-form-item>
            <el-input v-model="passwordForm.old" type="password" :placeholder="$t('navbar.oldPassword')" required />
          </el-form-item>
          <el-form-item>
            <el-input v-model="passwordForm.new" type="password" :placeholder="$t('navbar.newPassword')" required />
          </el-form-item>
          <el-form-item>
            <el-input v-model="passwordForm.confirm" type="password" :placeholder="$t('navbar.confirmPassword')" required />
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="passwordDialog = false">{{ $t('el.messagebox.cancel') }}</el-button>
          <el-button type="primary" @click="submitForm">{{ $t('el.messagebox.confirm') }}</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'
import ErrorLog from '@/components/ErrorLog'
import Screenfull from '@/components/Screenfull'
import SizeSelect from '@/components/SizeSelect'
import LangSelect from '@/components/LangSelect'
import Search from '@/components/HeaderSearch'
import ThemePicker from '@/components/ThemePicker'
import { changePassword } from '@/api/user'

export default {
  components: {
    Breadcrumb,
    Hamburger,
    ErrorLog,
    Screenfull,
    SizeSelect,
    LangSelect,
    Search,
    ThemePicker
  },
  data() {
    const validateRequire = (rule, value, callback) => {
      console('im here')
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
    const validateSamePassword = (rule, value, callback) => {
      if (value !== this.confirm) {
        this.$message({
          message: this.$t('navbar.passwordSame'),
          type: 'error'
        })
        callback(new Error(this.$t('navbar.passwordSame')))
      } else {
        callback()
      }
    }
    return {
      passwordDialog: false,
      passwordForm: {
        old: '',
        new: '',
        confirm: ''
      },
      rules: {
        old: [{ validator: validateRequire }],
        new: [{ validator: validateRequire }],
        confirm: [{ validator: validateRequire }, { validator: validateSamePassword }]
      }
    }
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'name',
      'avatar',
      'device'
    ])
  },
  created() {
    this.$store.dispatch('settings/getTheme')
    this.$store.dispatch('app/getLanguage')
  },

  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login?redirect=${this.$route.fullPath}`)
    },
    submitForm() {
      this.$refs.passwordForm.validate(valid => {
        console.log(valid)
        if (!valid) return
        changePassword(this.passwordForm).then(resp => {
          this.passwordDialog = false
          this.$message({
            message: this.$t('post.success'),
            type: 'success'
          })
        }).catch(e => {
          this.$message({
            message: e,
            type: 'error'
          })
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color:transparent;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .errLog-container {
    display: inline-block;
    vertical-align: top;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
