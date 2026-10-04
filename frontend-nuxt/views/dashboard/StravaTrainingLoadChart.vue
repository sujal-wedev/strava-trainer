<script setup lang="ts">
import { computed } from 'vue'
import { useTheme } from 'vuetify'
import { useStravaData } from '@/composables/useStravaData'

const vuetifyTheme = useTheme()
const { ctlAtlForm } = useStravaData()

const series = computed(() => [
  {
    name: 'Fitness (CTL)',
    type: 'area',
    data: ctlAtlForm.value.history30Days.map(item => item.ctl),
  },
  {
    name: 'Fatigue (ATL)',
    type: 'line',
    data: ctlAtlForm.value.history30Days.map(item => item.atl),
  },
  {
    name: 'Form (TSB)',
    type: 'column',
    data: ctlAtlForm.value.history30Days.map(item => item.tsb),
  },
])

const chartOptions = computed(() => {
  const currentTheme = vuetifyTheme.current.value.colors

  return {
    chart: {
      height: 320,
      type: 'line',
      stacked: false,
      toolbar: { show: false },
      parentHeightOffset: 0,
    },
    stroke: {
      width: [3, 2.5, 0],
      curve: 'smooth',
      dashArray: [0, 4, 0],
    },
    colors: [
      '#FC4C02', // Strava Orange for Fitness CTL
      '#FFAB00', // Amber for Fatigue ATL
      '#71DD37', // Green for Form TSB
    ],
    fill: {
      type: ['gradient', 'solid', 'solid'],
      gradient: {
        shade: 'light',
        type: 'vertical',
        shadeIntensity: 0.25,
        opacityFrom: 0.35,
        opacityTo: 0.05,
        stops: [0, 90, 100],
      },
    },
    markers: {
      size: [4, 4, 0],
      strokeWidth: 2,
      hover: { size: 6 },
    },
    xaxis: {
      categories: ctlAtlForm.value.history30Days.map(item => item.date),
      labels: {
        style: {
          colors: currentTheme['grey-500'],
          fontSize: '12px',
        },
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    yaxis: [
      {
        title: {
          text: 'Load (CTL / ATL)',
          style: { color: currentTheme['grey-500'], fontSize: '11px', fontWeight: 600 },
        },
        labels: {
          style: { colors: currentTheme['grey-500'] },
          formatter: (val: number) => Math.round(val),
        },
        min: 40,
        max: 95,
      },
      {
        opposite: true,
        title: {
          text: 'Form (TSB)',
          style: { color: currentTheme['grey-500'], fontSize: '11px', fontWeight: 600 },
        },
        labels: {
          style: { colors: currentTheme['grey-500'] },
          formatter: (val: number) => (val > 0 ? `+${val}` : `${val}`),
        },
        min: -20,
        max: 25,
      },
    ],
    legend: {
      position: 'top',
      horizontalAlign: 'right',
      labels: { colors: currentTheme['grey-600'] },
      markers: { radius: 12 },
    },
    grid: {
      borderColor: 'rgba(128, 128, 128, 0.1)',
      strokeDashArray: 4,
      padding: { top: 0, right: 10, bottom: 0, left: 10 },
    },
    tooltip: {
      shared: true,
      intersect: false,
      theme: vuetifyTheme.current.value.dark ? 'dark' : 'light',
    },
  }
})
</script>

<template>
  <VCard>
    <VCardItem class="pb-2">
      <template #prepend>
        <VAvatar
          color="primary"
          variant="tonal"
          rounded
          size="40"
          class="me-3"
        >
          <VIcon
            icon="bx-trending-up"
            size="24"
          />
        </VAvatar>
      </template>

      <VCardTitle class="text-h6 font-weight-bold">
        Training Load & Form (CTL / ATL / TSB)
      </VCardTitle>
      <VCardSubtitle class="text-caption">
        Continuous Chronic Fitness vs Acute Fatigue & Performance Form curve
      </VCardSubtitle>

      <template #append>
        <VChip
          color="success"
          size="small"
          variant="tonal"
          class="font-weight-bold"
        >
          ACWR: {{ ctlAtlForm.acwrRatio }} (Optimal)
        </VChip>
      </template>
    </VCardItem>

    <VCardText class="pt-2">
      <!-- 4 Core Metric Indicators -->
      <VRow class="mb-4">
        <VCol
          cols="6"
          sm="3"
        >
          <div class="pa-3 rounded-lg metric-pill" style="border-left: 3px solid #FC4C02;">
            <div class="text-caption text-medium-emphasis">
              Fitness (CTL)
            </div>
            <div class="text-h5 font-weight-black text-primary">
              {{ ctlAtlForm.ctlFitness }}
            </div>
            <div class="text-caption text-success font-weight-semibold">
              <VIcon
                icon="bx-up-arrow-alt"
                size="14"
              /> +16 pts (30d)
            </div>
          </div>
        </VCol>

        <VCol
          cols="6"
          sm="3"
        >
          <div class="pa-3 rounded-lg metric-pill" style="border-left: 3px solid #FFAB00;">
            <div class="text-caption text-medium-emphasis">
              Fatigue (ATL)
            </div>
            <div class="text-h5 font-weight-black text-warning">
              {{ ctlAtlForm.atlFatigue }}
            </div>
            <div class="text-caption text-medium-emphasis font-weight-semibold">
              <VIcon
                icon="bx-down-arrow-alt"
                size="14"
              /> -6 vs peak
            </div>
          </div>
        </VCol>

        <VCol
          cols="6"
          sm="3"
        >
          <div class="pa-3 rounded-lg metric-pill" style="border-left: 3px solid #71DD37;">
            <div class="text-caption text-medium-emphasis">
              Form (TSB)
            </div>
            <div class="text-h5 font-weight-black text-success">
              +{{ ctlAtlForm.tsbForm }}
            </div>
            <div class="text-caption text-success font-weight-semibold">
              Fresh & Primed
            </div>
          </div>
        </VCol>

        <VCol
          cols="6"
          sm="3"
        >
          <div class="pa-3 rounded-lg metric-pill" style="border-left: 3px solid #03C3EC;">
            <div class="text-caption text-medium-emphasis">
              Workload Ratio
            </div>
            <div class="text-h5 font-weight-black text-info">
              {{ ctlAtlForm.acwrRatio }}
            </div>
            <div class="text-caption text-info font-weight-semibold">
              Sweet Spot
            </div>
          </div>
        </VCol>
      </VRow>

      <!-- ApexChart -->
      <VueApexCharts
        type="line"
        height="320"
        :options="chartOptions"
        :series="series"
      />
    </VCardText>
  </VCard>
</template>

<style scoped>
.metric-pill {
  background: rgba(var(--v-theme-surface), 0.6);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
</style>
