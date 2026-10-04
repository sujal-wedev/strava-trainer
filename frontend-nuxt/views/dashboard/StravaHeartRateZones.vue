<script setup lang="ts">
import { computed } from 'vue'
import { useTheme } from 'vuetify'

const vuetifyTheme = useTheme()

const series = [18, 54, 16, 9, 3]

const chartOptions = computed(() => {
  const currentTheme = vuetifyTheme.current.value.colors

  return {
    chart: {
      type: 'donut',
      height: 220,
      parentHeightOffset: 0,
    },
    labels: ['Z1 Recovery', 'Z2 Aerobic Base', 'Z3 Tempo', 'Z4 Threshold', 'Z5 Anaerobic'],
    colors: ['#03C3EC', '#71DD37', '#FFAB00', '#FC4C02', '#FF3E1D'],
    stroke: { width: 2, colors: [vuetifyTheme.current.value.dark ? '#2B2C40' : '#fff'] },
    dataLabels: { enabled: false },
    legend: { show: false },
    plotOptions: {
      pie: {
        donut: {
          size: '72%',
          labels: {
            show: true,
            value: {
              fontSize: '1.25rem',
              fontWeight: 700,
              color: currentTheme['grey-900'],
              formatter: (val: string) => `${val}%`,
            },
            total: {
              show: true,
              label: 'Z2 Aerobic',
              fontSize: '0.8rem',
              color: currentTheme['grey-500'],
              formatter: () => '54%',
            },
          },
        },
      },
    },
    tooltip: {
      theme: vuetifyTheme.current.value.dark ? 'dark' : 'light',
    },
  }
})

const zones = [
  { name: 'Z1 Active Recovery', range: '< 135 bpm', time: '1h 02m', pct: 18, color: '#03C3EC' },
  { name: 'Z2 Aerobic Base', range: '135 - 152 bpm', time: '3h 05m', pct: 54, color: '#71DD37' },
  { name: 'Z3 Tempo & Cruise', range: '153 - 165 bpm', time: '55m', pct: 16, color: '#FFAB00' },
  { name: 'Z4 Lactate Threshold', range: '166 - 178 bpm', time: '31m', pct: 9, color: '#FC4C02' },
  { name: 'Z5 Anaerobic Capacity', range: '> 178 bpm', time: '10m', pct: 3, color: '#FF3E1D' },
]
</script>

<template>
  <VCard class="h-100 d-flex flex-column">
    <VCardItem class="pb-1">
      <template #prepend>
        <VAvatar
          color="error"
          variant="tonal"
          rounded
          size="40"
          class="me-3"
        >
          <VIcon
            icon="bx-heart"
            size="24"
          />
        </VAvatar>
      </template>

      <VCardTitle class="text-h6 font-weight-bold">
        Heart Rate Zones
      </VCardTitle>
      <VCardSubtitle class="text-caption">
        Intensity distribution & polarized 80/20 compliance
      </VCardSubtitle>

      <template #append>
        <VChip
          size="small"
          color="success"
          variant="tonal"
          class="font-weight-bold"
        >
          72% Low Intensity
        </VChip>
      </template>
    </VCardItem>

    <VCardText class="flex-grow-1 pt-2">
      <div class="d-flex align-center justify-center my-1">
        <VueApexCharts
          type="donut"
          height="200"
          :options="chartOptions"
          :series="series"
        />
      </div>

      <!-- Zone Breakdown Rows -->
      <div class="d-flex flex-column gap-2 mt-2">
        <div
          v-for="zone in zones"
          :key="zone.name"
          class="d-flex align-center justify-space-between text-caption py-1 border-b"
        >
          <div class="d-flex align-center gap-2">
            <span
              class="d-inline-block rounded-circle"
              :style="{ width: '10px', height: '10px', backgroundColor: zone.color }"
            />
            <span class="font-weight-medium">{{ zone.name }}</span>
            <span class="text-disabled" style="font-size: 0.7rem;">({{ zone.range }})</span>
          </div>

          <div class="d-flex align-center gap-2">
            <span class="text-medium-emphasis">{{ zone.time }}</span>
            <span class="font-weight-bold text-body-2" :style="{ color: zone.color }">{{ zone.pct }}%</span>
          </div>
        </div>
      </div>
    </VCardText>
  </VCard>
</template>
