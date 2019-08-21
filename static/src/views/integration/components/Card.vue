
<template>
  <div class="int-card">
    <el-dialog
      :title="label"
      :visible.sync="dialogVisible"
      width="30%"
    >
      <el-form>
        <el-form-item v-for="key in fields" :key="label+key">
          <el-input v-model="settings[key]">
            <template slot="prepend">{{ key|capitalize }}</template>
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">{{ $t('el.messagebox.cancel') }}</el-button>
        <el-button type="primary" @click="updateSettings">{{ $t('el.messagebox.confirm') }}</el-button>
      </span>
    </el-dialog>
    <el-card :body-style="{ padding: '0px' }">
      <a @click="dialogVisible = true"><img :src="image" class="image" :class="{ gray: !settings.enabled }"></a>
      <div style="padding: 0 14px 14px;">
        <p>{{ label }}</p>
        <div class="bottom clearfix">
          <el-switch v-model="settings.enabled" @input="enableIntegration" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>

export default {
  props: {
    label: {
      type: String,
      default: () => ''
    },
    fields: {
      type: Array,
      default: () => []
    },
    initial: {
      type: Object,
      default: () => { return {} }
    },
    image: {
      type: String,
      default: () => ''
    },
    name: {
      type: String,
      default: () => ''
    }
  },
  data() {
    return {
      dialogVisible: false,
      settings: this.initial || {}
    }
  },
  watch: {
    initial() {
      this.settings = { ...this.initial }
    }
  },
  methods: {
    updateSettings() {
      this.$store.dispatch('integration/updateData', { name: this.name, ...this.settings }).then(_ => {
        this.dialogVisible = false
      })
    },
    enableIntegration() {
      if (Object.entries(this.settings).some(e => !e[1])) {
        this.$message({
          type: 'warning',
          message: this.$t('settings.fieldMissing')
        })
        this.settings.enabled = false
      } else {
        this.$store.dispatch('integration/updateData', { name: this.name, ...this.settings })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.int-card {
  margin: 0 20px 20px 0;
  display: inline-block;
}

.gray {
  -webkit-filter: grayscale(100%);
  -moz-filter: grayscale(100%);
  -ms-filter: grayscale(100%);
  -o-filter: grayscale(100%);

  filter: grayscale(100%);

  filter: gray;
}
</style>
