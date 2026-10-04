<script setup lang="ts">
import { ref } from 'vue'

const vitals = ref({
  restingHr: 42,
  maxHr: 194,
  thresholdHr: 172,
  thresholdPace: '3:40',
  ftpWatts: 290,
  weightKg: 64.5,
  vo2Max: 65,
  autoCalculateZones: true,
})

const isSaved = ref(false)

const saveVitals = () => {
  isSaved.value = true
  setTimeout(() => {
    isSaved.value = false
  }, 3000)
}
</script>

<template>
  <VCard title="Athlete Physiological Settings & Zones">
    <VCardText>
      <VAlert
        v-if="isSaved"
        type="success"
        variant="tonal"
        class="mb-4"
      >
        Athlete physiological metrics & heart rate training zones updated successfully!
      </VAlert>

      <VRow>
        <VCol cols="12" md="4">
          <VTextField
            v-model="vitals.restingHr"
            label="Resting Heart Rate (bpm)"
            type="number"
            variant="outlined"
            hint="Measured upon waking"
            persistent-hint
          />
        </VCol>

        <VCol cols="12" md="4">
          <VTextField
            v-model="vitals.maxHr"
            label="Maximum Heart Rate (bpm)"
            type="number"
            variant="outlined"
            hint="From stress test or all-out 5k"
            persistent-hint
          />
        </VCol>

        <VCol cols="12" md="4">
          <VTextField
            v-model="vitals.thresholdHr"
            label="Lactate Threshold HR (LTHR)"
            type="number"
            variant="outlined"
            hint="1-hour time trial average"
            persistent-hint
          />
        </VCol>

        <VCol cols="12" md="4">
          <VTextField
            v-model="vitals.thresholdPace"
            label="Lactate Threshold Pace (/km)"
            variant="outlined"
            hint="Functional threshold running pace"
            persistent-hint
          />
        </VCol>

        <VCol cols="12" md="4">
          <VTextField
            v-model="vitals.ftpWatts"
            label="Cycling FTP (Watts)"
            type="number"
            variant="outlined"
            hint="Functional Threshold Power"
            persistent-hint
          />
        </VCol>

        <VCol cols="12" md="4">
          <VTextField
            v-model="vitals.vo2Max"
            label="VO2 Max Estimate (ml/kg/min)"
            type="number"
            variant="outlined"
            hint="Calculated from GPS race performance"
            persistent-hint
          />
        </VCol>

        <VCol cols="12">
          <VSwitch
            v-model="vitals.autoCalculateZones"
            label="Auto-update training zones based on new Strava activities"
            color="primary"
          />
        </VCol>

        <VCol cols="12" class="d-flex gap-4">
          <VBtn color="primary" @click="saveVitals">Save Zones</VBtn>
          <VBtn variant="tonal" color="secondary">Recalculate Defaults</VBtn>
        </VCol>
      </VRow>
    </VCardText>
  </VCard>
</template>
