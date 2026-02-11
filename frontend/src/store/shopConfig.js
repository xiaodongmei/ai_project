/**
 * 店铺配置全局状态
 *
 * 存储当前店铺的行业类型、术语标签、选项列表等配置。
 * 所有需要显示行业相关术语的组件都从这里读取。
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as configApi from '@/api/config'

export const useShopConfigStore = defineStore('shopConfig', () => {
  // 完整配置
  const config = ref({
    shop_name: '我的店铺',
    industry_type: 'general_service',
    description: '',
    address: '',
    phone: '',
    business_hours: '',
    logo_url: '',
    // 术语
    space_label: '服务区',
    space_label_plural: '服务区管理',
    station_label: '工位',
    provider_label: '服务师',
    provider_label_plural: '服务师管理',
    // 选项列表
    space_types: [],
    station_types: [],
    staff_roles: [],
    service_categories: [],
    product_categories: [],
    skill_tags: [],
    // 默认服务项目（含价格、时长）
    default_services: [],
  })

  const loaded = ref(false)

  // 快捷访问计算属性
  const shopName = computed(() => config.value.shop_name)
  const industryType = computed(() => config.value.industry_type)
  const spaceLabel = computed(() => config.value.space_label)
  const spaceLabelPlural = computed(() => config.value.space_label_plural)
  const stationLabel = computed(() => config.value.station_label)
  const providerLabel = computed(() => config.value.provider_label)
  const providerLabelPlural = computed(() => config.value.provider_label_plural)
  const staffRoles = computed(() => config.value.staff_roles)
  const serviceCategories = computed(() => config.value.service_categories)
  const productCategories = computed(() => config.value.product_categories)
  const skillTags = computed(() => config.value.skill_tags)
  const defaultServices = computed(() => config.value.default_services || [])
  const spaceTypes = computed(() => config.value.space_types)
  const stationTypes = computed(() => config.value.station_types)

  // 侧边栏菜单动态标签
  const menuLabels = computed(() => ({
    dashboard: '收银',
    spaces: config.value.space_label || '服务区',
    customers: '顾客',
    appointments: '预约',
    orders: '订单',
    products: '产品',
    employees: config.value.provider_label || '员工',
    statistics: '统计',
  }))

  // 面包屑动态标签
  const breadcrumbLabels = computed(() => ({
    '/dashboard': '收银台',
    '/rooms': config.value.space_label_plural || '服务区管理',
    '/customers': '顾客管理',
    '/appointments': '预约管理',
    '/orders': '订单管理',
    '/products': '产品管理',
    '/employees': (config.value.provider_label || '员工') + '管理',
    '/statistics': '数据统计',
    '/profile': '个人资料',
    '/settings': '系统设置',
  }))

  /** 从后端加载配置 */
  async function loadConfig() {
    try {
      const res = await configApi.getShopConfig()
      if (res) {
        config.value = { ...config.value, ...res }
      }
      loaded.value = true
    } catch (e) {
      // 后端不可用时使用默认配置，不阻塞页面
      loaded.value = true
    }
  }

  /** 更新配置 */
  async function saveConfig(data) {
    const res = await configApi.updateShopConfig(data)
    if (res) {
      config.value = { ...config.value, ...res }
    }
    return res
  }

  /** 切换行业模板 */
  async function switchIndustry(industryType) {
    const res = await configApi.updateShopConfig({ industry_type: industryType })
    if (res) {
      config.value = { ...config.value, ...res }
    }
    return res
  }

  return {
    config,
    loaded,
    shopName,
    industryType,
    spaceLabel,
    spaceLabelPlural,
    stationLabel,
    providerLabel,
    providerLabelPlural,
    staffRoles,
    serviceCategories,
    productCategories,
    skillTags,
    defaultServices,
    spaceTypes,
    stationTypes,
    menuLabels,
    breadcrumbLabels,
    loadConfig,
    saveConfig,
    switchIndustry,
  }
})
