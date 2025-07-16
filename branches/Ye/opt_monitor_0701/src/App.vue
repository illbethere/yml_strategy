<template>
  <nav class="navbar-center">
    <router-link to="/" class="nav-link">首页</router-link>
    <router-link to="/Signal" class="nav-link">信号</router-link>
    <router-link to="/Order" class="nav-link">下单</router-link>
  </nav>
</template>

<style>
/* 顶部导航栏：始终100%拉满 */
.navbar-center {
  width: 100vw;
  min-width: 360px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0 16px 0;
  background: #f6faff;
  box-sizing: border-box;
  gap: 36px;
  border-bottom: 1px solid #e0e0e0;
  z-index: 10;
}

/* 导航按钮样式同前略 */

.nav-link {
  color: #222;
  font-size: 1.15rem;
  text-decoration: none;
  padding: 6px 18px;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
}
.nav-link:hover {
  background: #409EFF22;
  color: #409EFF;
}
.router-link-exact-active.nav-link {
  background: #409EFF;
  color: #fff !important;
  font-weight: bold;
}

/* 中间内容区域自适应居中，最大宽度 */
.main-content {
  margin: 0 auto;              /* 水平居中 */
  padding: 32px 18px 40px 18px;/* 内边距，左右适配窄屏 */
  max-width: 1200px;           /* 最大宽度 */
  min-height: 80vh;            /* 保证内容撑满页面 */
  box-sizing: border-box;
}
</style>