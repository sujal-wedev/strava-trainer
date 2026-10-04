<script setup lang="ts">
import { ref, computed } from 'vue'
import { useStravaData, type StravaActivity } from '@/composables/useStravaData'

const { recentActivities, athlete } = useStravaData()

const selectedSport = ref('All')
const searchQuery = ref('')
const selectedActivity = ref<StravaActivity>(recentActivities.value[0])
const kudosMap = ref<Record<string, number>>({})
const kudosGiven = ref<Record<string, boolean>>({})

// Initialize kudos
recentActivities.value.forEach(act => {
  kudosMap.value[act.id] = act.kudos
  kudosGiven.value[act.id] = false
})

const toggleKudos = (id: string) => {
  if (kudosGiven.value[id]) {
    kudosMap.value[id]--
    kudosGiven.value[id] = false
  } else {
    kudosMap.value[id]++
    kudosGiven.value[id] = true
  }
}

const filteredActivities = computed(() => {
  return recentActivities.value.filter(act => {
    const matchesSport = selectedSport.value === 'All' || act.type === selectedSport.value
    const matchesSearch = act.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          act.pace.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesSport && matchesSearch
  })
})

const mockSplits = computed(() => {
  if (!selectedActivity.value) return []
  const count = Math.min(Math.round(selectedActivity.value.distanceKm), 10)
  const baseSec = 270 // ~4:30
  return Array.from({ length: count }, (_, i) => {
    const variance = (Math.sin(i * 1.5) * 8) - (i > count * 0.7 ? 6 : 0)
    const sec = Math.round(baseSec + variance)
    const m = Math.floor(sec / 60)
    const s = sec % 60
    return {
      km: i + 1,
      split: `${m}:${s < 10 ? '0' : ''}${s} /km`,
      elevation: `+${Math.round(8 + Math.abs(Math.cos(i) * 12))}m`,
      avgHr: Math.round(146 + i * 2.2),
    }
  })
})

const getSportIcon = (type: string) => {
  if (type === 'Run') return 'bx-run'
  if (type === 'Ride') return 'bx-cycling'
  if (type === 'Swim') return 'bx-swim'
  return 'bx-pulse'
}

const getSportColor = (type: string) => {
  if (type === 'Run') return 'primary'
  if (type === 'Ride') return 'info'
  if (type === 'Swim') return 'success'
  return 'warning'
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="d-flex flex-wrap align-center justify-space-between gap-3 mb-6">
      <div>
        <h2 class="text-h4 font-weight-bold text-high-emphasis mb-1">
          Activity Feed & GPS Analysis
        </h2>
        <div class="text-body-2 text-medium-emphasis">
          Detailed telemetry, heart rate zones, elevation profiles, and kudos
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <VBtn
          color="primary"
          prepend-icon="bx-sync"
          variant="tonal"
          to="/strava-connect"
        >
          Strava Live Sync
        </VBtn>
      </div>
    </div>

    <!-- Filter & Search Controls -->
    <VCard class="mb-6">
      <VCardText class="d-flex flex-wrap align-center justify-space-between gap-4">
        <div class="d-flex align-center flex-wrap gap-2">
          <VBtnToggle
            v-model="selectedSport"
            mandatory
            color="primary"
            variant="outlined"
            density="comfortable"
          >
            <VBtn value="All">All Sports</VBtn>
            <VBtn value="Run" prepend-icon="bx-run">Runs</VBtn>
            <VBtn value="Ride" prepend-icon="bx-cycling">Rides</VBtn>
            <VBtn value="Swim" prepend-icon="bx-swim">Swims</VBtn>
          </VBtnToggle>
        </div>

        <div style="min-width: 260px;" class="flex-grow-1 flex-md-grow-0">
          <VTextField
            v-model="searchQuery"
            density="compact"
            placeholder="Search workouts or paces..."
            prepend-inner-icon="bx-search"
            variant="outlined"
            hide-details
            clearable
          />
        </div>
      </VCardText>
    </VCard>

    <!-- Main Content: Left List, Right Inspector -->
    <VRow>
      <!-- Activity Feed List -->
      <VCol cols="12" md="6" lg="5">
        <div class="d-flex flex-column gap-4">
          <VCard
            v-for="activity in filteredActivities"
            :key="activity.id"
            class="activity-card cursor-pointer transition-swing"
            :class="{ 'border-primary-active': selectedActivity.id === activity.id }"
            @click="selectedActivity = activity"
          >
            <VCardText class="pa-4">
              <div class="d-flex align-center justify-space-between mb-3">
                <div class="d-flex align-center gap-3">
                  <VAvatar
                    :color="getSportColor(activity.type)"
                    variant="tonal"
                    rounded
                    size="44"
                  >
                    <VIcon
                      :icon="getSportIcon(activity.type)"
                      size="24"
                    />
                  </VAvatar>
                  <div>
                    <div class="text-caption font-weight-bold text-uppercase" :class="`text-${getSportColor(activity.type)}`">
                      {{ activity.type }}
                    </div>
                    <div class="text-caption text-disabled">
                      {{ activity.date }}
                    </div>
                  </div>
                </div>

                <div class="d-flex align-center gap-1">
                  <VChip
                    size="x-small"
                    color="primary"
                    variant="tonal"
                    class="font-weight-bold"
                  >
                    Suffer {{ activity.sufferScore }}
                  </VChip>
                  <VChip
                    v-if="activity.trophies > 0"
                    size="x-small"
                    color="warning"
                    variant="flat"
                    class="font-weight-bold"
                  >
                    🏆 {{ activity.trophies }}
                  </VChip>
                </div>
              </div>

              <h4 class="text-h6 font-weight-bold mb-2">
                {{ activity.title }}
              </h4>

              <div class="d-flex flex-wrap align-center justify-space-between gap-2 pa-3 rounded bg-var-theme-background mb-3">
                <div>
                  <div class="text-caption text-disabled">Distance</div>
                  <div class="text-body-1 font-weight-black text-primary">{{ activity.distance }}</div>
                </div>
                <div>
                  <div class="text-caption text-disabled">Time</div>
                  <div class="text-body-1 font-weight-bold">{{ activity.time }}</div>
                </div>
                <div>
                  <div class="text-caption text-disabled">Avg Pace</div>
                  <div class="text-body-1 font-weight-bold">{{ activity.pace }}</div>
                </div>
                <div>
                  <div class="text-caption text-disabled">Avg HR</div>
                  <div class="text-body-1 font-weight-bold text-error">{{ activity.avgHr }} bpm</div>
                </div>
              </div>

              <p v-if="activity.notes" class="text-caption text-medium-emphasis mb-3 line-clamp-2">
                {{ activity.notes }}
              </p>

              <div class="d-flex align-center justify-space-between pt-2 border-t text-caption">
                <span v-if="activity.gearName" class="text-disabled d-flex align-center">
                  <VIcon icon="bx-purchase-tag" size="14" class="me-1" />
                  {{ activity.gearName }}
                </span>
                <span v-else />

                <div class="d-flex align-center gap-2">
                  <VBtn
                    size="small"
                    variant="tonal"
                    :color="kudosGiven[activity.id] ? 'primary' : 'secondary'"
                    @click.stop="toggleKudos(activity.id)"
                  >
                    <VIcon icon="bx-like" size="16" class="me-1" />
                    {{ kudosMap[activity.id] }} Kudos
                  </VBtn>
                  <span class="text-medium-emphasis">
                    <VIcon icon="bx-comment" size="14" class="me-1" />{{ activity.comments }}
                  </span>
                </div>
              </div>
            </VCardText>
          </VCard>
        </div>
      </VCol>

      <!-- Activity Deep Dive Inspector -->
      <VCol cols="12" md="6" lg="7">
        <VCard v-if="selectedActivity" class="sticky-top">
          <!-- Banner Header -->
          <VCardItem class="border-b pb-4">
            <template #prepend>
              <VAvatar
                :color="getSportColor(selectedActivity.type)"
                variant="flat"
                rounded
                size="48"
                class="me-3"
              >
                <VIcon
                  :icon="getSportIcon(selectedActivity.type)"
                  size="28"
                  color="white"
                />
              </VAvatar>
            </template>

            <VCardTitle class="text-h5 font-weight-black">
              {{ selectedActivity.title }}
            </VCardTitle>
            <VCardSubtitle class="text-body-2">
              Recorded by {{ athlete.name }} • {{ selectedActivity.date }}
            </VCardSubtitle>

            <template #append>
              <VBtn
                variant="flat"
                color="primary"
                size="small"
                prepend-icon="bx-share-alt"
              >
                Share
              </VBtn>
            </template>
          </VCardItem>

          <VCardText class="pa-5">
            <!-- Simulated GPS Map & Elevation Path Visualizer -->
            <div class="gps-route-box pa-4 rounded-xl mb-4 position-relative overflow-hidden">
              <div class="d-flex justify-space-between align-center mb-2">
                <span class="text-caption font-weight-bold text-uppercase text-primary d-flex align-center">
                  <VIcon icon="bx-map-alt" size="16" class="me-1" /> GPS Track Route Preview
                </span>
                <span class="text-caption text-medium-emphasis">
                  Elev Gain: {{ selectedActivity.elevation }} • Max HR: {{ selectedActivity.maxHr }} bpm
                </span>
              </div>

              <!-- Stylized GPS Vector Track -->
              <svg viewBox="0 0 600 160" class="w-100" style="height: 140px;">
                <defs>
                  <linearGradient id="routeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#FC4C02" stop-opacity="0.8" />
                    <stop offset="50%" stop-color="#FFAB00" stop-opacity="0.9" />
                    <stop offset="100%" stop-color="#FC4C02" stop-opacity="1" />
                  </linearGradient>
                  <linearGradient id="elevationFill" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#FC4C02" stop-opacity="0.25" />
                    <stop offset="100%" stop-color="#FC4C02" stop-opacity="0.0" />
                  </linearGradient>
                </defs>
                <path
                  d="M10 120 Q 80 40, 160 80 T 310 50 T 450 110 T 590 30"
                  fill="none"
                  stroke="url(#routeGradient)"
                  stroke-width="5"
                  stroke-linecap="round"
                />
                <path
                  d="M10 120 Q 80 40, 160 80 T 310 50 T 450 110 T 590 30 L 590 160 L 10 160 Z"
                  fill="url(#elevationFill)"
                />
                <!-- Start & Finish Pins -->
                <circle cx="10" cy="120" r="7" fill="#71DD37" stroke="#fff" stroke-width="2" />
                <circle cx="590" cy="30" r="7" fill="#FC4C02" stroke="#fff" stroke-width="2" />
              </svg>

              <div class="d-flex justify-space-between text-caption text-disabled mt-1">
                <span>Start: 0.0 km</span>
                <span class="text-primary font-weight-bold">Peak: +{{ selectedActivity.elevation }}</span>
                <span>Finish: {{ selectedActivity.distance }}</span>
              </div>
            </div>

            <!-- Key Telemetry Metrics Grid -->
            <VRow class="mb-4">
              <VCol cols="6" sm="3">
                <div class="pa-3 rounded bg-var-theme-background text-center">
                  <div class="text-caption text-disabled">Distance</div>
                  <div class="text-h6 font-weight-black text-primary">{{ selectedActivity.distance }}</div>
                </div>
              </VCol>
              <VCol cols="6" sm="3">
                <div class="pa-3 rounded bg-var-theme-background text-center">
                  <div class="text-caption text-disabled">Moving Time</div>
                  <div class="text-h6 font-weight-black">{{ selectedActivity.time }}</div>
                </div>
              </VCol>
              <VCol cols="6" sm="3">
                <div class="pa-3 rounded bg-var-theme-background text-center">
                  <div class="text-caption text-disabled">Avg Pace</div>
                  <div class="text-h6 font-weight-black">{{ selectedActivity.pace }}</div>
                </div>
              </VCol>
              <VCol cols="6" sm="3">
                <div class="pa-3 rounded bg-var-theme-background text-center">
                  <div class="text-caption text-disabled">Calories</div>
                  <div class="text-h6 font-weight-black">{{ selectedActivity.calories }} kcal</div>
                </div>
              </VCol>
            </VRow>

            <!-- Splits & Kilometer Laps Table -->
            <h4 class="text-subtitle-1 font-weight-bold mb-3 d-flex align-center gap-2">
              <VIcon icon="bx-list-ol" color="primary" size="20" />
              Kilometer Splits & Heart Rate
            </h4>

            <VTable density="compact" class="elevation-0 border rounded">
              <thead>
                <tr>
                  <th class="text-uppercase text-caption font-weight-bold">Km</th>
                  <th class="text-uppercase text-caption font-weight-bold">Pace</th>
                  <th class="text-uppercase text-caption font-weight-bold">Elevation</th>
                  <th class="text-uppercase text-caption font-weight-bold">Avg HR</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="split in mockSplits" :key="split.km">
                  <td class="font-weight-bold">{{ split.km }}</td>
                  <td class="font-weight-medium text-primary">{{ split.split }}</td>
                  <td class="text-medium-emphasis">{{ split.elevation }}</td>
                  <td>
                    <span class="text-error font-weight-bold">{{ split.avgHr }}</span> bpm
                  </td>
                </tr>
              </tbody>
            </VTable>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>

<style scoped>
.activity-card {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
.activity-card:hover {
  border-color: #FC4C02;
}
.border-primary-active {
  border-color: #FC4C02 !important;
  box-shadow: 0 4px 18px rgba(252, 76, 2, 0.15) !important;
}
.gps-route-box {
  background: rgba(var(--v-theme-surface), 0.8);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
.sticky-top {
  position: sticky;
  top: 90px;
}
</style>
