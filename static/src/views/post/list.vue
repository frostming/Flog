<template>
  <div class="tab-container">
    <router-link slot="label" to="/post/create/">
      <el-button type="primary" size="small" class="create-post-btn" icon="el-icon-edit">
        {{ $t('post.newPost') }}
      </el-button>
    </router-link>
    <el-tabs v-model="activeName" style="margin-top:15px;" type="border-card">
      <el-tab-pane v-for="(name,key) in tabMapOptions" :key="key" :label="name" :name="key">
        <keep-alive>
          <post-tab v-if="activeName===key" :type="key" />
        </keep-alive>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import PostTab from '@/components/PostTab'

export default {
  name: 'PostList',
  components: { PostTab },
  data() {
    return {
      tabMapOptions: {
        published: this.$t('post.published'),
        draft: this.$t('post.draft')
      },
      activeName: 'published'
    }
  }
}
</script>

<style scoped>
  .tab-container {
    margin: 30px;
  }
</style>
