<script setup lang="ts">
import { useStravaData } from '@/composables/useStravaData'

const { athlete, weeklySummary, ctlAtlForm, syncWithStrava, isSyncing } = useStravaData()
</script>

<template>
  <VCard class="strava-banner-card overflow-hidden position-relative">
    <div class="strava-accent-stripe" />
    <VCardText class="pa-6">
      <VRow align="center">
        <!-- Left: Athlete Info & Status -->
        <VCol
          cols="12"
          md="8"
        >
          <div class="d-flex flex-wrap align-center gap-3 mb-3">
            <VAvatar
              size="64"
              class="elevation-2 border-primary border-2"
            >
              <VImg
                :src="athlete.avatar"
                alt="Alex Morgan"
              />
            </VAvatar>

            <div>
              <div class="d-flex align-center flex-wrap gap-2">
                <h3 class="text-h5 font-weight-bold mb-0">
                  {{ athlete.name }}
                </h3>
                <VChip
                  size="small"
                  color="primary"
                  variant="flat"
                  class="font-weight-bold text-uppercase"
                >
                  <VIcon
                    start
                    icon="bx-badge-check"
                    size="16"
                  />
                  {{ athlete.badge }}
                </VChip>
                <VChip
                  size="small"
                  color="success"
                  variant="tonal"
                  class="font-weight-medium"
                >
                  <VIcon
                    start
                    icon="bx-pulse"
                    size="16"
                  />
                  {{ ctlAtlForm.formStatus }} (+{{ ctlAtlForm.tsbForm }} TSB)
                </VChip>
              </div>

              <div class="text-body-2 text-medium-emphasis mt-1 d-flex align-center flex-wrap gap-x-3">
                <span><VIcon
                  icon="bx-map-pin"
                  size="14"
                  class="me-1"
                />{{ athlete.location }}</span>
                <span>•</span>
                <span><VIcon
                  icon="bx-group"
                  size="14"
                  class="me-1"
                />{{ athlete.club }}</span>
              </div>
            </div>
          </div>

          <!-- Training Phase Notice -->
          <div class="strava-phase-box rounded-lg pa-3 mb-2 d-flex flex-wrap align-center justify-space-between gap-2">
            <div class="d-flex align-center gap-2">
              <VAvatar
                color="primary"
                variant="tonal"
                size="36"
                rounded
              >
                <VIcon
                  icon="bx-calendar-star"
                  size="20"
                />
              </VAvatar>
              <div>
                <div class="text-caption font-weight-bold text-uppercase text-primary">
                  Current Target Focus
                </div>
                <div class="text-body-2 font-weight-semibold">
                  Valencia Marathon Prep — Week 8 of 16 (Peak VO2 & Specificity)
                </div>
              </div>
            </div>

            <div class="d-flex align-center gap-3 text-caption font-weight-medium">
              <div>
                <span class="text-medium-emphasis">Goal: </span>
                <span class="text-primary font-weight-bold">Sub-2:35:00</span>
              </div>
              <div class="d-none d-sm-block text-disabled">
                |
              </div>
              <div>
                <span class="text-medium-emphasis">Days to Race: </span>
                <span class="font-weight-bold">56 Days</span>
              </div>
            </div>
          </div>

          <p class="text-body-2 text-medium-emphasis mb-0">
            {{ athlete.bio }}
          </p>
        </VCol>

        <!-- Right: Action & Quick Stats -->
        <VCol
          cols="12"
          md="4"
          class="d-flex flex-column align-md-end justify-center"
        >
          <div class="w-100 text-md-end mb-4">
            <div class="text-caption text-uppercase font-weight-bold text-disabled mb-1">
              Weekly Mileage Target
            </div>
            <div class="d-flex align-center justify-md-end gap-2 mb-2">
              <span class="text-h4 font-weight-black text-primary">{{ weeklySummary.currentKm }}</span>
              <span class="text-h6 text-medium-emphasis">/ {{ weeklySummary.targetKm }} km</span>
            </div>
            <VProgressLinear
              :model-value="weeklySummary.progressPct"
              color="primary"
              height="8"
              rounded
              class="mb-2"
            />
            <div class="text-caption text-medium-emphasis d-flex justify-space-between justify-md-end gap-3">
              <span>{{ weeklySummary.progressPct }}% Complete</span>
              <span class="text-success font-weight-semibold">+{{ weeklySummary.vsLastWeekPct }}% vs last week</span>
            </div>
          </div>

          <div class="d-flex flex-wrap gap-2 w-100 justify-md-end">
            <VBtn
              color="primary"
              variant="flat"
              prepend-icon="bx-sync"
              :loading="isSyncing"
              @click="syncWithStrava"
            >
              Sync Strava
            </VBtn>
            <VBtn
              color="primary"
              variant="tonal"
              prepend-icon="bx-calendar-event"
              to="/training-plans"
            >
              View Plan
            </VBtn>
          </div>
        </VCol>
      </VRow>
    </VCardText>
  </VCard>
</template>

<style scoped lang="scss">
.strava-banner-card {
  border-left: 4px solid #FC4C02 !important;
  background: linear-gradient(135deg, rgba(252, 76, 2, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
}

.strava-accent-stripe {
  position: absolute;
  top: 0;
  right: 0;
  width: 160px;
  height: 100%;
  background: radial-gradient(circle at top right, rgba(252, 76, 2, 0.08), transparent 70%);
  pointer-events: none;
}

.strava-phase-box {
  background: rgba(var(--v-theme-surface), 0.7);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
</style>
