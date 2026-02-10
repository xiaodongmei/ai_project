<template>
  <div ref="chartElement" style="width: 100%; height: 300px"></div>
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
      axisPointer: {
        type: 'shadow',
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
      data: props.data.map((item) => item.name),
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
        data: props.data.map((item) => item.value),
        type: 'bar',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#fccb05' },
            { offset: 0.5, color: '#f78103' },
            { offset: 1, color: '#ff6b00' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#ffb808' },
              { offset: 0.7, color: '#ff8c00' },
              { offset: 1, color: '#cc5500' },
            ]),
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
        xAxis: {
          data: props.data.map((item) => item.name),
        },
        series: [
          {
            data: props.data.map((item) => item.value),
          },
        ],
      })
    }
  },
  { deep: true }
)
</script>
