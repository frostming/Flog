<template>
  <div class="app-container">
    <el-button slot="label" type="primary" style="margin-bottom: 20px;" icon="el-icon-edit" @click="importVisible = true">
      {{ $t('post.import') }}
    </el-button>
    <import-dialog :visible.sync="importVisible" @success="getList" />
    <el-table v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%">
      <el-table-column align="center" label="ID" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column min-width="120px" align="center" :label="$t('route.posts')">
        <template slot-scope="scope">
          <a :href="scope.row.post.url">{{ scope.row.post.title }}</a>
        </template>
      </el-table-column>

      <el-table-column :label="$t('post.author')" width="100px">
        <template slot-scope="{row}">
          <span>{{ row.author.username }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('post.date')" width="150px">
        <template slot-scope="{row}">
          <span>{{ row.create_at | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('post.content')">
        <template slot-scope="{row}">
          <span>{{ row.content }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" :label="$t('post.actions')" width="220">
        <template slot-scope="scope">
          <el-button type="danger" size="small" icon="el-icon-delete" @click="handleDelete(scope.row)">
            {{ $t('post.delete') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total>listQuery.page" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
  </div>

</template>

<script>
import Pagination from '@/components/Pagination'
import ImportDialog from './ImportDialog'
import { fetchList, deleteComment } from '@/api/comment'

export default {
  name: 'CommentList',
  components: { Pagination, ImportDialog },
  data() {
    return {
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20
      },
      importVisible: false
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
          deleteComment(row.id).then(() => {
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
