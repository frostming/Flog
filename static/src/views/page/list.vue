<template>
  <div class="tab-container">
    <el-tabs style="margin-top:15px;" type="border-card">
      <el-tab-pane :label="$t('post.pages')">
        <keep-alive>
          <div class="app-container">
            <el-table v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%">
              <el-table-column align="center" label="ID" width="80">
                <template slot-scope="scope">
                  <span>{{ scope.row.id }}</span>
                </template>
              </el-table-column>

              <el-table-column width="120px" align="center" :label="$t('post.url')">
                <template slot-scope="scope">
                  <span>/{{ scope.row.slug }}</span>
                </template>
              </el-table-column>

              <el-table-column min-width="300px" :label="$t('post.title')">
                <template slot-scope="{row}">
                  <router-link :to="'/page/edit/'+row.id" class="link-type">
                    <span>{{ row.title }}</span>
                  </router-link>
                </template>
              </el-table-column>

              <el-table-column align="center" :label="$t('post.actions')" width="220">
                <template slot-scope="scope">
                  <router-link :to="'/page/edit/'+scope.row.id">
                    <el-button type="primary" size="small" icon="el-icon-edit">
                      {{ $t('post.edit') }}
                    </el-button>
                  </router-link>
                  <el-button type="danger" size="small" icon="el-icon-delete" @click="handleDelete(scope.row)">
                    {{ $t('post.delete') }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </keep-alive>
      </el-tab-pane>
      <el-tab-pane>
        <router-link slot="label" to="/page/create/">
          <el-button type="primary" size="small" class="create-post-btn" icon="el-icon-edit">
            {{ $t('post.newPage') }}
          </el-button>
        </router-link>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { fetchList, deletePage } from '@/api/page'

export default {
  name: 'PageList',
  data() {
    return {
      list: null,
      total: 0,
      listLoading: true
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList().then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.listLoading = false
      })
    },
    handleDelete(row) {
      this.$confirm(this.$t('post.confirmDelete'), this.$t('el.messagebox.title'), {
        type: 'warining'
      }).then(val => {
        if (val) {
          deletePage(row.id).then(() => {
            this.list.splice(this.list.indexOf(row), 1)
            this.$message(this.$t('post.delSuccess'))
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.tab-container {
  margin: 30px;
}
.edit-input {
  padding-right: 100px;
}
.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
</style>
