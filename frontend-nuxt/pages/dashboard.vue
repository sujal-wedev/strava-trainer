<script setup lang="ts">
import StravaAthleteBanner from '@/views/dashboard/StravaAthleteBanner.vue'
import StravaTrainingLoadChart from '@/views/dashboard/StravaTrainingLoadChart.vue'
import StravaWeeklyVolume from '@/views/dashboard/StravaWeeklyVolume.vue'
import StravaHeartRateZones from '@/views/dashboard/StravaHeartRateZones.vue'
import StravaVirtualCoach from '@/views/dashboard/StravaVirtualCoach.vue'
import StravaGearCard from '@/views/dashboard/StravaGearCard.vue'
import StravaRecentActivities from '@/views/dashboard/StravaRecentActivities.vue'
import { useStravaData } from '@/composables/useStravaData'

const { weeklySummary } = useStravaData()
</script>

<template>
  <VRow class="match-height">
    <!-- 👉 Athlete Summary Banner -->
    <VCol cols="12">
      <StravaAthleteBanner />
    </VCol>

    <!-- 👉 4 Core Training Metrics -->
    <VCol
      cols="12"
      sm="6"
      md="3"
    >
      <VCard class="pa-2">
        <VCardText class="d-flex align-center gap-3">
          <VAvatar
            color="primary"
            variant="tonal"
            size="48"
            rounded
          >
            <VIcon
              icon="bx-run"
              size="28"
            />
          </VAvatar>
          <div>
            <div class="text-caption text-medium-emphasis font-weight-medium">
              Weekly Distance
            </div>
            <div class="text-h5 font-weight-black text-primary">
              {{ weeklySummary.currentKm }} <span class="text-body-2 text-medium-emphasis">/ {{ weeklySummary.targetKm }} km</span>
            </div>
            <div class="text-caption text-success font-weight-bold">
              <VIcon
                icon="bx-up-arrow-alt"
                size="14"
              /> +{{ weeklySummary.vsLastWeekPct }}% vs last week
            </div>
          </div>
        </VCardText>
      </VCard>
    </VCol>

    <VCol
      cols="12"
      sm="6"
      md="3"
    >
      <VCard class="pa-2">
        <VCardText class="d-flex align-center gap-3">
          <VAvatar
            color="primary"
            variant="tonal"
            size="48"
            rounded
          >
            <VIcon
              icon="bx-pulse"
              size="28"
            />
          </VAvatar>
          <div>
            <div class="text-caption text-medium-emphasis font-weight-medium">
              Relative Suffer Score
            </div>
            <div class="text-h5 font-weight-black text-primary">
              {{ weeklySummary.sufferScore }}
            </div>
            <div class="text-caption text-primary font-weight-bold">
              Optimal Training Zone
            </div>
          </div>
        </VCardText>
      </VCard>
    </VCol>

    <VCol
      cols="12"
      sm="6"
      md="3"
    >
      <VCard class="pa-2">
        <VCardText class="d-flex align-center gap-3">
          <VAvatar
            color="info"
            variant="tonal"
            size="48"
            rounded
          >
            <VIcon
              icon="bx-timer"
              size="28"
            />
          </VAvatar>
          <div>
            <div class="text-caption text-medium-emphasis font-weight-medium">
              Active Time
            </div>
            <div class="text-h5 font-weight-black text-info">
              {{ weeklySummary.activeTimeHours }} hrs
            </div>
            <div class="text-caption text-medium-emphasis font-weight-bold">
              Across {{ weeklySummary.activitiesCount }} workouts
            </div>
          </div>
        </VCardText>
      </VCard>
    </VCol>

    <VCol
      cols="12"
      sm="6"
      md="3"
    >
      <VCard class="pa-2">
        <VCardText class="d-flex align-center gap-3">
          <VAvatar
            color="success"
            variant="tonal"
            size="48"
            rounded
          >
            <VIcon
              icon="bx-trending-up"
              size="28"
            />
          </VAvatar>
          <div>
            <div class="text-caption text-medium-emphasis font-weight-medium">
              Elevation Gain
            </div>
            <div class="text-h5 font-weight-black text-success">
              {{ weeklySummary.elevationClimbedM }} m
            </div>
            <div class="text-caption text-success font-weight-bold">
              <VIcon
                icon="bx-up-arrow-alt"
                size="14"
              /> +340 m mountain climbing
            </div>
          </div>
        </VCardText>
      </VCard>
    </VCol>

    <!-- 👉 Performance Load & Form Chart -->
    <VCol
      cols="12"
      lg="8"
    >
      <StravaTrainingLoadChart />
    </VCol>

    <!-- 👉 Weekly Volume Distribution -->
    <VCol
      cols="12"
      lg="4"
    >
      <StravaWeeklyVolume />
    </VCol>

    <!-- 👉 Heart Rate Zones -->
    <VCol
      cols="12"
      md="4"
    >
      <StravaHeartRateZones />
    </VCol>

    <!-- 👉 AI Virtual Coach -->
    <VCol
      cols="12"
      md="4"
    >
      <StravaVirtualCoach />
    </VCol>

    <!-- 👉 Gear Mileage Health -->
    <VCol
      cols="12"
      md="4"
    >
      <StravaGearCard />
    </VCol>

    <!-- 👉 Recent Strava Activities -->
    <VCol cols="12">
      <StravaRecentActivities />
    </VCol>
  </VRow>
</template>
