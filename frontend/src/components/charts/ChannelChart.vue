<template>
  <div class="channel-chart">
    <div ref="chartElement" style="width: 100%; height: 300px"></div>
    <div class="channel-legend">
      <div v-for="(item, index) in data" :key="index" class="legend-item">
        <span class="legend-dot" :style="{ backgroundColor: colors[index] }"></span>
        <span class="legend-label">{{ item.name }}</span>
        <span class="legend-value">{{ item.percentage }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
})

const chartElement = ref(null)
const colors = ['#FF9500', '#409EFF', '#67C23A', '#F56C6C']
let chart = null

const initChart = () => {
  if (!chartElement.value) return

  chart = echarts.init(chartElement.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(50, 50, 50, 0.7)',
      borderColor: '#777',
      textStyle: {
        color: '#fff',
      },
      formatter: '{b}: ¥{c} ({d}%)',
    },
    legend: {
      show: false,
    },
    series: [
      {
        type: 'pie',
        radius: '60%',
        center: ['50%', '50%'],
        data: props.data.map((item, index) => ({
          value: item.value,
          name: item.name,
          itemStyle: {
            color: colors[index],
          },
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  }

  chart.setOption(option)
}

onMounted(() => {
  initChart()
})

watch(
  () => props.data,
  () => {
    if (chart) {
      chart.setOption({
        series: [
          {
            data: props.data.map((item, index) => ({
              value: item.value,
              name: item.name,
              itemStyle: {
                color: colors[index],
              },
            })),
          },
        ],
      })
    }
  },
  { deep: true }
)
</script>

<style scoped lang="scss">
.channel-chart {
  display: flex;
  flex-direction: column;
}

.channel-legend {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;

  .legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .legend-label {
    flex: 1;
    color: #606266;
  }

  .legend-value {
    color: #909399;
    font-weight: 600;
  }
}
</style>
