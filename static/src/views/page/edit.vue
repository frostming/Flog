<template>
  <page-detail :is-edit="true" />
</template>

<script>
import PageDetail from '@/components/PageDetail'

export default {
  name: 'EditPage',
  components: { PageDetail }
}
</script>
