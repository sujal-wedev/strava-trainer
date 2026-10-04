<script setup lang="ts">
import { useStravaData } from '@/composables/useStravaData'

const { gearList } = useStravaData()

const getProgressColor = (current: number, max: number) => {
  const pct = (current / max) * 100
  if (pct >= 85) return 'error'
  if (pct >= 65) return 'warning'
  return 'primary'
}
</script>

<template>
  <VCard class="h-100 d-flex flex-column">
    <VCardItem class="pb-2">
      <template #prepend>
        <VAvatar
          color="warning"
          variant="tonal"
          rounded
          size="40"
          class="me-3"
        >
          <VIcon
            icon="bx-package"
            size="24"
          />
        </VAvatar>
      </template>

      <VCardTitle class="text-h6 font-weight-bold">
        Gear & Mileage Health
      </VCardTitle>
      <VCardSubtitle class="text-caption">
        Shoe cushioning wear & bike drivetrain maintenance
      </VCardSubtitle>

      <template #append>
        <VBtn
          size="small"
          variant="text"
          color="primary"
          append-icon="bx-chevron-right"
          to="/gear"
        >
          Manage
        </VBtn>
      </template>
    </VCardItem>

    <VCardText class="flex-grow-1 pt-1">
      <div class="d-flex flex-column gap-3">
        <div
          v-for="item in gearList.slice(0, 4)"
          :key="item.id"
          class="pa-3 rounded-lg gear-item"
        >
          <div class="d-flex align-center justify-space-between mb-1">
            <div class="d-flex align-center gap-2">
              <VAvatar
                :color="item.type === 'Shoes' ? 'primary' : 'info'"
                variant="tonal"
                size="30"
                rounded
              >
                <VIcon
                  :icon="item.type === 'Shoes' ? 'bx-run' : 'bx-cycling'"
                  size="18"
                />
              </VAvatar>
              <div>
                <div class="font-weight-bold text-body-2 line-clamp-1">
                  {{ item.name }}
                </div>
                <div class="text-caption text-medium-emphasis">
                  {{ item.activitiesCount }} activities logged
                </div>
              </div>
            </div>

            <div class="text-end">
              <div class="font-weight-black text-body-2">
                {{ item.currentKm }} <span class="text-caption text-medium-emphasis">/ {{ item.maxKm }} km</span>
              </div>
              <div
                class="text-caption font-weight-semibold"
                :class="`text-${getProgressColor(item.currentKm, item.maxKm)}`"
              >
                {{ Math.round((item.currentKm / item.maxKm) * 100) }}% wear
              </div>
            </div>
          </div>

          <VProgressLinear
            :model-value="(item.currentKm / item.maxKm) * 100"
            :color="getProgressColor(item.currentKm, item.maxKm)"
            height="6"
            rounded
            class="mt-2"
          />
        </div>
      </div>
    </VCardText>
  </VCard>
</template>

<style scoped>
.gear-item {
  background: rgba(var(--v-theme-surface), 0.6);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
</style>
