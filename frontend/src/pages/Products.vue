<template>
  <div class="products-page">
    <!-- 顶部标签: 项目 / 产品 / 办卡 -->
    <div class="page-tabs">
      <button
        v-for="tab in pageTabs"
        :key="tab.id"
        :class="['page-tab', { 'page-tab--active': activePageTab === tab.id }]"
        @click="activePageTab = tab.id"
      >{{ tab.label }}</button>
      <!-- 搜索框 -->
      <div class="tab-search">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
        <input v-model="searchText" type="text" placeholder="搜入店名或扫码查询" class="search-input" @input="handleSearch" />
      </div>
    </div>

    <!-- 主内容：左侧分类 + 右侧产品列表 -->
    <div class="content-layout">
      <!-- 左侧分类菜单 -->
      <div class="category-sidebar">
        <button
          v-for="cat in allCategories"
          :key="cat.id"
          :class="['cat-item', { 'cat-item--active': selectedCategory === cat.id }]"
          @click="selectCategory(cat.id)"
        >
          {{ cat.name }}
        </button>
      </div>

      <!-- 右侧产品网格 -->
      <div class="products-area">
        <div class="products-grid" v-if="filteredProducts.length">
          <div class="product-card" v-for="product in filteredProducts" :key="product.id" @click="handleProductClick(product)">
            <!-- 产品图片 -->
            <div class="product-image">
              <div class="product-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="placeholder-icon">
                  <rect x="3" y="3" width="18" height="18" rx="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <path d="m21 15-5-5L5 21" />
                </svg>
              </div>
            </div>
            <!-- 产品信息 -->
            <div class="product-info">
              <h4 class="product-name">{{ product.name }}</h4>
              <div class="product-prices">
                <span class="member-price" v-if="product.member_price">会员价¥{{ product.member_price }}</span>
                <span class="regular-price">¥{{ product.price }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="empty-state" v-else>
          <p>该分类暂无产品</p>
        </div>
      </div>
    </div>

    <!-- 底部结算栏 -->
    <div class="checkout-bar">
      <div class="cart-info">
        <span>本单数量：<strong>{{ cartCount }}</strong></span>
        <span class="cart-total">合计金额：<strong class="total-amount">¥{{ cartTotal.toFixed(2) }}</strong></span>
      </div>
      <div class="cart-actions">
        <button class="btn-outline-action" @click="handleCancel">取单</button>
        <button class="btn-outline-action" @click="handleHold">挂单</button>
        <button class="btn-primary-action" @click="handleCheckout">收银结账</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as productsApi from '@/api/products'

const pageTabs = [
  { id: 'project', label: '项目' },
  { id: 'product', label: '产品' },
  { id: 'card', label: '办卡' },
]

const activePageTab = ref('product')
const searchText = ref('')
const selectedCategory = ref(0)
const categories = ref([])
const products = ref([])
const cartItems = ref([])
const loading = ref(false)

const allCategories = computed(() => {
  return [{ id: 0, name: '全部' }, ...categories.value]
})

const filteredProducts = computed(() => {
  let list = products.value
  if (selectedCategory.value !== 0) {
    list = list.filter(p => p.category_id === selectedCategory.value)
  }
  if (searchText.value) {
    const q = searchText.value.toLowerCase()
    list = list.filter(p => p.name.toLowerCase().includes(q))
  }
  return list
})

const cartCount = computed(() => cartItems.value.reduce((s, i) => s + i.quantity, 0))
const cartTotal = computed(() => cartItems.value.reduce((s, i) => s + (i.price * i.quantity), 0))

const selectCategory = (id) => {
  selectedCategory.value = id
}

const handleSearch = () => {
  // 实时搜索
}

const handleProductClick = (product) => {
  const existing = cartItems.value.find(i => i.id === product.id)
  if (existing) {
    existing.quantity++
  } else {
    cartItems.value.push({ ...product, quantity: 1 })
  }
  ElMessage.success(`已添加 ${product.name}`)
}

const handleCancel = () => {
  cartItems.value = []
  ElMessage.info('已清空购物车')
}

const handleHold = () => {
  ElMessage.success('已挂单')
}

const handleCheckout = () => {
  if (cartItems.value.length === 0) {
    ElMessage.warning('请先选择产品')
    return
  }
  ElMessage.success('收银结账成功')
  cartItems.value = []
}

const loadData = async () => {
  loading.value = true
  try {
    const catRes = await productsApi.getCategories()
    categories.value = catRes?.items || catRes || []
  } catch (e) {
    categories.value = [
      { id: 1, name: '养方' }, { id: 2, name: '枕头' }, { id: 3, name: '养生小食' },
      { id: 4, name: '艾草棒' }, { id: 5, name: '手提袋' }, { id: 6, name: '热敷贴' },
      { id: 7, name: '养生茶' }, { id: 8, name: '三伏养生' }, { id: 9, name: '合液' },
    ]
  }

  try {
    const prodRes = await productsApi.getProducts({ limit: 100 })
    products.value = prodRes?.items || []
  } catch (e) {
    products.value = []
  }
  loading.value = false
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
$primary: #2563eb;
$primary-light: rgba(37, 99, 235, 0.1);
$border: #e5e7eb;
$bg-card: #fff;
$bg-page: #f5f7fa;
$text-main: #111827;
$text-secondary: #6b7280;
$text-muted: #9ca3af;
$red: #ef4444;

.products-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 56px);
  background: $bg-page;
}

// 顶部标签
.page-tabs {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 24px;
  background: white;
  border-bottom: 1px solid $border;
}

.page-tab {
  padding: 8px 24px;
  font-size: 15px;
  font-weight: 500;
  color: $text-secondary;
  background: none;
  border: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;

  &--active {
    color: $text-main;
    border-bottom-color: $primary;
  }

  &:hover:not(.page-tab--active) {
    color: $text-main;
  }
}

.tab-search {
  margin-left: auto;
  position: relative;
  display: flex;
  align-items: center;

  .search-icon {
    position: absolute;
    left: 10px;
    width: 16px;
    height: 16px;
    color: $text-muted;
    pointer-events: none;
  }

  .search-input {
    width: 220px;
    height: 34px;
    padding: 0 12px 0 32px;
    border: 1px solid $border;
    border-radius: 6px;
    font-size: 13px;
    outline: none;
    transition: border-color 0.2s;

    &:focus {
      border-color: $primary;
    }
  }
}

// 主内容
.content-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

// 左侧分类
.category-sidebar {
  width: 110px;
  background: white;
  border-right: 1px solid $border;
  overflow-y: auto;
  flex-shrink: 0;
  padding: 8px 0;
}

.cat-item {
  display: block;
  width: 100%;
  padding: 12px 16px;
  font-size: 14px;
  color: $text-secondary;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 3px solid transparent;

  &:hover {
    background: #f9fafb;
    color: $text-main;
  }

  &--active {
    background: $primary-light;
    color: $primary;
    font-weight: 500;
    border-left-color: $primary;
  }
}

// 右侧产品区域
.products-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.product-card {
  background: white;
  border: 1px solid $border;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-color: rgba(37, 99, 235, 0.3);
    transform: translateY(-2px);
  }
}

.product-image {
  height: 120px;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-placeholder {
  .placeholder-icon {
    width: 40px;
    height: 40px;
    color: #d1d5db;
  }
}

.product-info {
  padding: 12px;
}

.product-name {
  font-size: 13px;
  font-weight: 500;
  color: $text-main;
  margin: 0 0 8px 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-prices {
  display: flex;
  align-items: center;
  gap: 8px;
}

.member-price {
  font-size: 13px;
  font-weight: 600;
  color: $red;
}

.regular-price {
  font-size: 12px;
  color: $text-muted;
  text-decoration: line-through;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: $text-muted;
}

// 底部结算栏
.checkout-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: white;
  border-top: 1px solid $border;
}

.cart-info {
  display: flex;
  gap: 24px;
  font-size: 14px;
  color: $text-secondary;

  strong { color: $text-main; }
}

.total-amount {
  color: $red !important;
  font-size: 18px;
}

.cart-actions {
  display: flex;
  gap: 10px;
}

.btn-outline-action {
  padding: 8px 24px;
  border: 1px solid $border;
  border-radius: 8px;
  background: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: $primary;
    color: $primary;
  }
}

.btn-primary-action {
  padding: 8px 32px;
  background: $primary;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: #1d4ed8;
  }
}

@media (max-width: 768px) {
  .products-grid { grid-template-columns: repeat(2, 1fr); }
  .category-sidebar { width: 80px; .cat-item { padding: 10px 8px; font-size: 12px; } }
}
</style>
