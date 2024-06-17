<template>
  <nav class="breadcrumb">
    <ul>
      <li v-for="(crumb, index) in breadcrumbs" :key="index">
        <router-link :to="crumb.link">{{ crumb.text }}</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  computed: {
    breadcrumbs() {
      const route = this.$route;
      const matched = route.matched;

      let breadcrumbs = [];

      // 添加起点（用户仪表盘或商家仪表盘）
      let dashboardBreadcrumb = null;
      if (route.path.startsWith('/users')) {
        dashboardBreadcrumb = { text: '用户仪表盘', link: '/users/dashboard/:id' };
      } else if (route.path.startsWith('/merchants')) {
        dashboardBreadcrumb = { text: '商家仪表盘', link: '/merchants/dashboard/:id' };
      }

      if (dashboardBreadcrumb) {
        breadcrumbs.push(dashboardBreadcrumb);
      }

      // 遍历路由的 matched 数组，生成面包屑导航
      matched.forEach((match) => {
        let breadcrumbText = match.meta.breadcrumb || 'Page'; // 默认为 'Page'，可根据实际情况修改
        let link = this.getFullPath(match);

        // 确保当前面包屑不重复添加
        if (breadcrumbs.length === 0 || breadcrumbs[breadcrumbs.length - 1].text !== breadcrumbText) {
          breadcrumbs.push({ text: breadcrumbText, link });
        }
      });

      return breadcrumbs;
    },
  },
  methods: {
    // 获取完整路径
    getFullPath(match) {
      let path = '';
      match.path.split('/').forEach((pathPart) => {
        if (pathPart) {
          path += `/${pathPart}`;
        }
      });
      return path;
    },
  },
};
</script>

<style scoped>
.breadcrumb {
  margin: 1rem 0;
}

.breadcrumb ul {
  list-style: none;
  display: flex;
  padding: 0;
}

.breadcrumb li {
  margin-right: 0.5rem;
}

.breadcrumb li::after {
  content: '>';
  margin-left: 0.5rem;
}

.breadcrumb li:last-child::after {
  content: '';
  margin-left: 0;
}
</style>
