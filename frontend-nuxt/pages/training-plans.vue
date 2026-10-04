<script setup lang="ts">
import { ref } from 'vue'
import { useStravaData } from '@/composables/useStravaData'

const { trainingPlan } = useStravaData()
const activeTab = ref(1) // Week 8
const addWorkoutDialog = ref(false)

const newWorkout = ref({
  title: '',
  sport: 'Run',
  distance: '',
  pace: '',
  day: 'Sun',
})

const getSportIcon = (sport: string) => {
  if (sport === 'Run') return 'bx-run'
  if (sport === 'Ride') return 'bx-cycling'
  if (sport === 'Swim') return 'bx-swim'
  return 'bx-bed'
}

const getSportColor = (sport: string) => {
  if (sport === 'Run') return 'primary'
  if (sport === 'Ride') return 'info'
  if (sport === 'Swim') return 'success'
  return 'secondary'
}
</script>

<template>
  <div>
    <!-- Page Header -->
    <div class="d-flex flex-wrap align-center justify-space-between gap-3 mb-6">
      <div>
        <h2 class="text-h4 font-weight-bold text-high-emphasis mb-1">
          Structured Training Plans
        </h2>
        <div class="text-body-2 text-medium-emphasis">
          Periodized endurance training, daily workout targets, and periodization cycles
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <VBtn
          color="primary"
          prepend-icon="bx-plus"
          @click="addWorkoutDialog = true"
        >
          Schedule Workout
        </VBtn>
      </div>
    </div>

    <!-- Active Plan Overview Banner -->
    <VCard class="mb-6 pa-2 border-primary border-s-4">
      <VCardText>
        <VRow align="center">
          <VCol cols="12" md="8">
            <div class="d-flex align-center gap-2 mb-2">
              <VChip
                color="primary"
                size="small"
                variant="flat"
                class="font-weight-bold"
              >
                Active Plan
              </VChip>
              <VChip
                color="success"
                size="small"
                variant="tonal"
              >
                16-Week Marathon Specificity
              </VChip>
            </div>

            <h3 class="text-h5 font-weight-black mb-1">
              Valencia Marathon Sub-2:35 Build
            </h3>
            <p class="text-body-2 text-medium-emphasis mb-0">
              Designed by Elite Coach & Exercise Physiologist. Focuses on 80/20 polarized volume, marathon pace efficiency, and lactate clearance intervals.
            </p>
          </VCol>

          <VCol cols="12" md="4" class="text-md-end">
            <div class="text-caption text-disabled text-uppercase font-weight-bold">
              Current Microcycle
            </div>
            <div class="text-h4 font-weight-black text-primary">
              Week 8 of 16
            </div>
            <div class="text-caption text-medium-emphasis">
              Target: 75 km • 56 Days to Race
            </div>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>

    <!-- Weekly Timeline Tabs -->
    <VTabs
      v-model="activeTab"
      color="primary"
      class="mb-6"
    >
      <VTab :value="0">
        <VIcon start icon="bx-check-circle" color="success" />
        Week 7 (Completed - 72.8 km)
      </VTab>
      <VTab :value="1">
        <VIcon start icon="bx-pulse" color="primary" />
        Week 8: Current Peak (64.8 / 75 km)
      </VTab>
      <VTab :value="2">
        <VIcon start icon="bx-time" color="disabled" />
        Week 9: Recovery Week (55 km)
      </VTab>
    </VTabs>

    <!-- Workout Day Cards for Selected Week -->
    <div v-if="trainingPlan[activeTab]">
      <div class="mb-4">
        <h3 class="text-h6 font-weight-bold">
          {{ trainingPlan[activeTab].title }}
        </h3>
        <p class="text-body-2 text-medium-emphasis">
          {{ trainingPlan[activeTab].focus }}
        </p>
      </div>

      <VRow>
        <VCol
          v-for="(w, idx) in trainingPlan[activeTab].workouts"
          :key="idx"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <VCard
            class="h-100 d-flex flex-column workout-card"
            :class="{
              'border-today': w.status === 'today',
              'opacity-75': w.status === 'done',
            }"
          >
            <VCardText class="pa-4 flex-grow-1 d-flex flex-column justify-space-between">
              <div>
                <div class="d-flex align-center justify-space-between mb-3">
                  <VChip
                    size="small"
                    :color="getSportColor(w.sport)"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    <VIcon start :icon="getSportIcon(w.sport)" size="16" />
                    {{ w.day }} • {{ w.sport }}
                  </VChip>

                  <VChip
                    size="x-small"
                    :color="w.status === 'done' ? 'success' : w.status === 'today' ? 'primary' : 'secondary'"
                    variant="flat"
                    class="font-weight-bold text-uppercase"
                  >
                    {{ w.status }}
                  </VChip>
                </div>

                <h4 class="text-body-1 font-weight-bold mb-2">
                  {{ w.title }}
                </h4>

                <div class="pa-3 rounded bg-var-theme-background mb-3">
                  <div class="d-flex justify-space-between text-caption mb-1">
                    <span class="text-disabled">Distance:</span>
                    <span class="font-weight-bold text-primary">{{ w.distance }}</span>
                  </div>
                  <div class="d-flex justify-space-between text-caption">
                    <span class="text-disabled">Target Pace:</span>
                    <span class="font-weight-semibold">{{ w.targetPace }}</span>
                  </div>
                </div>
              </div>

              <div>
                <VBtn
                  v-if="w.status === 'today'"
                  block
                  color="primary"
                  variant="flat"
                  size="small"
                  prepend-icon="bx-play-circle"
                >
                  Start Workout
                </VBtn>
                <div v-else-if="w.status === 'done'" class="text-center text-caption text-success font-weight-bold">
                  <VIcon icon="bx-check-double" size="16" class="me-1" />
                  Synced with Strava GPS
                </div>
                <div v-else class="text-center text-caption text-disabled">
                  Scheduled on Strava
                </div>
              </div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>
    </div>

    <!-- Add Workout Dialog -->
    <VDialog
      v-model="addWorkoutDialog"
      max-width="500"
    >
      <VCard title="Schedule Custom Workout">
        <VCardText>
          <VRow>
            <VCol cols="12">
              <VTextField
                v-model="newWorkout.title"
                label="Workout Title (e.g. 5x1km Threshold Intervals)"
                placeholder="Morning Speed Session"
                variant="outlined"
              />
            </VCol>
            <VCol cols="6">
              <VSelect
                v-model="newWorkout.sport"
                label="Sport"
                :items="['Run', 'Ride', 'Swim', 'Rest']"
                variant="outlined"
              />
            </VCol>
            <VCol cols="6">
              <VSelect
                v-model="newWorkout.day"
                label="Scheduled Day"
                :items="['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']"
                variant="outlined"
              />
            </VCol>
            <VCol cols="6">
              <VTextField
                v-model="newWorkout.distance"
                label="Distance (e.g. 12 km)"
                variant="outlined"
              />
            </VCol>
            <VCol cols="6">
              <VTextField
                v-model="newWorkout.pace"
                label="Target Pace (e.g. 4:10/km)"
                variant="outlined"
              />
            </VCol>
          </VRow>
        </VCardText>

        <VCardActions class="pa-4">
          <VSpacer />
          <VBtn
            variant="text"
            color="secondary"
            @click="addWorkoutDialog = false"
          >
            Cancel
          </VBtn>
          <VBtn
            variant="flat"
            color="primary"
            @click="addWorkoutDialog = false"
          >
            Save & Sync to Strava
          </VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </div>
</template>

<style scoped>
.workout-card {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
.border-today {
  border: 2px solid #FC4C02 !important;
  box-shadow: 0 4px 18px rgba(252, 76, 2, 0.15) !important;
}
</style>
