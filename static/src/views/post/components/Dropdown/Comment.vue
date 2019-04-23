<template>
  <el-dropdown :show-timeout="100" trigger="click">
    <el-button plain>
      {{ enabled?$t('post.commentOn'):$t('post.commentOff') }}
      <i class="el-icon-caret-bottom el-icon--right" />
    </el-button>
    <el-dropdown-menu slot="dropdown" class="no-padding">
      <el-dropdown-item>
        <el-radio-group v-model="enabled" style="padding: 10px;">
          <el-radio :label="false">
            {{ $t('post.turnOff') }}
          </el-radio>
          <el-radio :label="true">
            {{ $t('post.turnOn') }}
          </el-radio>
        </el-radio-group>
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    enabled: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('input', val)
      }
    }
  }
}
</script>
