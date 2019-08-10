<template>
  <div ref="rightPanel" :class="{ show: show }" class="rightPanel-container">
    <!-- <div class="rightPanel-background" /> -->
    <div class="rightPanel" :class="{ show: show }">
      <div
        class="handle-button"
        :style="{ top: buttonTop, 'background-color': theme }"
        @click="show = !show"
      >
        <i :class="show ? 'el-icon-close' : 'el-icon-setting'" />
      </div>
      <div class="rightPanel-items">
        <slot />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RightPanel',
  props: {
    clickNotClose: {
      default: false,
      type: Boolean
    },
    buttonTop: {
      default: '50%',
      type: String
    }
  },
  data() {
    return {
      show: false
    }
  },
  computed: {
    theme() {
      return this.$store.state.settings.theme
    }
  }
}
</script>

<style>
.showRightPanel {
  overflow: hidden;
  position: relative;
  width: calc(100% - 15px);
}
</style>

<style lang="scss" scoped>
.rightPanel {
  background: #fff;
  z-index: 1991;
  position: absolute;
  padding: 0 10px;
  width: 330px;
  top: 50px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.05);
  transition: all 0.25s cubic-bezier(0.7, 0.3, 0.1, 1);
  transform: translate(100%);
  right: 0px;

  @media (min-width: 980px) {
    width: 380px;
    transform: translate(0);
  }
}

.rightPanel-items {
  height: calc(100vh - 50px);
  overflow-y: auto;
}

.show {
  transition: all 0.3s cubic-bezier(0.7, 0.3, 0.1, 1);

  .rightPanel {
    transform: translate(0);
  }
}

.handle-button {
  position: absolute;
  left: -48px;
  border-radius: 6px 0 0 6px !important;
  width: 48px;
  height: 48px;
  pointer-events: auto;
  cursor: pointer;
  pointer-events: auto;
  font-size: 24px;
  text-align: center;
  color: #fff;
  line-height: 48px;

  i {
    font-size: 24px;
    line-height: 48px;
  }

  @media (min-width: 980px) {
    display: none;
  }
}
</style>
