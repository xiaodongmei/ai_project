<template>
  <div ref="chartElement" style="width: 100%; height: 300px"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
})

const chartElement = ref(null)
let chart = null

const initChart = () => {
  if (!chartElement.value) return

  chart = echarts.init(chartElement.value)

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(50, 50, 50, 0.7)',
      borderColor: '#777',
      textStyle: {
        color: '#fff',
      },
    },
    grid: {
      left: '50px',
      right: '30px',
      top: '20px',
      bottom: '40px',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: true,
      data: props.data.dates || getDefaultDates(),
      axisTick: {
        show: false,
      },
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          color: '#f0f0f0',
        },
      },
    },
    series: [
      {
        data: props.data.values || getDefaultValues(),
        type: 'line',
        smooth: true,
        itemStyle: {
          color: '#409eff',
        },
        lineStyle: {
          color: '#409eff',
          width: 2,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0)' },
          ]),
        },
      },
    ],
  }

  chart.setOption(option)
}

const getDefaultDates = () => {
  const dates = []
  const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    dates.push(date.toLocaleDateString('zh-CN'))
  }
  return dates
}

const getDefaultValues = () => {
  return [200, 250, 300, 280, 350, 400, 380]
}

onMounted(() => {
  initChart()
})

watch(
  () => props.data,
  () => {
    if (chart) {
      chart.setOption({
        xAxis: {
          data: props.data.dates || getDefaultDates(),
        },
        series: [
          {
            data: props.data.values || getDefaultValues(),
          },
        ],
      })
    }
  },
  { deep: true }
)
</script>
