<script setup lang="ts">
import { computed } from 'vue'
import { useTheme } from 'vuetify'
import { useStravaData } from '@/composables/useStravaData'

const vuetifyTheme = useTheme()
const { weeklySummary } = useStravaData()

const series = [
  {
    name: 'Running (km)',
    data: [8.2, 13.5, 0, 11.0, 0, 22.4, 9.7],
  },
  {
    name: 'Cycling (km / 2.5)',
    data: [0, 0, 19.4, 0, 0, 0, 0], // scaled for comparison
  },
  {
    name: 'Swimming (km x 5)',
    data: [0, 0, 0, 0, 13.0, 0, 0],
  },
]

const chartOptions = computed(() => {
  const currentTheme = vuetifyTheme.current.value.colors

  return {
    chart: {
      type: 'bar',
      stacked: true,
      height: 240,
      toolbar: { show: false },
      parentHeightOffset: 0,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '42%',
        borderRadius: 6,
        borderRadiusApplication: 'end',
      },
    },
    colors: ['#FC4C02', '#03C3EC', '#71DD37'],
    xaxis: {
      categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      labels: {
        style: { colors: currentTheme['grey-500'], fontSize: '12px' },
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    yaxis: {
      labels: {
        style: { colors: currentTheme['grey-500'] },
        formatter: (val: number) => `${Math.round(val)}k`,
      },
    },
    grid: {
      borderColor: 'rgba(128, 128, 128, 0.1)',
      strokeDashArray: 4,
      padding: { top: 0, right: 0, bottom: 0, left: 10 },
    },
    legend: {
      position: 'top',
      horizontalAlign: 'right',
      labels: { colors: currentTheme['grey-600'] },
      markers: { radius: 12 },
    },
    tooltip: {
      theme: vuetifyTheme.current.value.dark ? 'dark' : 'light',
    },
  }
})

const weeklyDays = [
  { day: 'M', sport: 'run', dist: '8.2 km', done: true },
  { day: 'T', sport: 'run', dist: '13.5 km', done: true },
  { day: 'W', sport: 'ride', dist: '48.6 km', done: true },
  { day: 'T', sport: 'run', dist: '11.0 km', done: true },
  { day: 'F', sport: 'swim', dist: '2.6 km', done: true },
  { day: 'S', sport: 'run', dist: '22.4 km', done: true },
  { day: 'S', sport: 'run', dist: '8.0 km', done: false, isToday: true },
]
</script>

<template>
  <VCard class="h-100 d-flex flex-column">
    <VCardItem class="pb-1">
      <template #prepend>
        <VAvatar
          color="primary"
          variant="tonal"
          rounded
          size="40"
          class="me-3"
        >
          <VIcon
            icon="bx-bar-chart-alt-2"
            size="24"
          />
        </VAvatar>
      </template>

      <VCardTitle class="text-h6 font-weight-bold">
        Weekly Volume & Distribution
      </VCardTitle>
      <VCardSubtitle class="text-caption">
        Daily multisport volume tracking towards 75 km goal
      </VCardSubtitle>

      <template #append>
        <VChip
          color="primary"
          size="small"
          variant="flat"
          class="font-weight-bold"
        >
          {{ weeklySummary.currentKm }} km Done
        </VChip>
      </template>
    </VCardItem>

    <VCardText class="flex-grow-1 pt-2">
      <!-- 7-Day Quick Visual Strip -->
      <div class="d-flex justify-space-between gap-1 mb-4 pa-2 rounded-lg bg-var-theme-background">
        <div
          v-for="(item, idx) in weeklyDays"
          :key="idx"
          class="text-center flex-grow-1 pa-1 rounded"
          :class="{
            'bg-primary text-white': item.isToday,
            'text-medium-emphasis': !item.isToday,
          }"
          :style="item.done ? 'border-bottom: 3px solid #FC4C02;' : 'border-bottom: 2px dashed #9E9E9E;'"
        >
          <div class="text-caption font-weight-bold">
            {{ item.day }}
          </div>
          <div style="font-size: 0.65rem;" class="font-weight-semibold">
            {{ item.dist }}
          </div>
          <VIcon
            :icon="item.done ? 'bx-check-circle' : item.isToday ? 'bx-time' : 'bx-circle'"
            :color="item.isToday ? 'white' : item.done ? 'success' : 'disabled'"
            size="14"
            class="mt-1"
          />
        </div>
      </div>

      <!-- ApexChart Bar Chart -->
      <VueApexCharts
        type="bar"
        height="240"
        :options="chartOptions"
        :series="series"
      />

      <!-- Weekly KPI Footer -->
      <VDivider class="my-3" />
      <div class="d-flex flex-wrap justify-space-between align-center gap-2 text-caption">
        <div>
          <span class="text-medium-emphasis">Active Time: </span>
          <span class="font-weight-bold text-body-2">{{ weeklySummary.activeTimeHours }} hrs</span>
        </div>
        <div>
          <span class="text-medium-emphasis">Elevation: </span>
          <span class="font-weight-bold text-body-2">{{ weeklySummary.elevationClimbedM }} m</span>
        </div>
        <div>
          <span class="text-medium-emphasis">Relative Suffer: </span>
          <span class="font-weight-bold text-primary text-body-2">{{ weeklySummary.sufferScore }}</span>
        </div>
      </div>
    </VCardText>
  </VCard>
</template>
