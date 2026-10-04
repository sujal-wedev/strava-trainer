<script setup lang="ts">
import { useStravaData } from '@/composables/useStravaData'

const { ctlAtlForm } = useStravaData()
</script>

<template>
  <VCard class="h-100 d-flex flex-column coach-card overflow-hidden">
    <VCardItem class="pb-2">
      <template #prepend>
        <VAvatar
          color="info"
          variant="tonal"
          rounded
          size="40"
          class="me-3"
        >
          <VIcon
            icon="bx-bot"
            size="24"
          />
        </VAvatar>
      </template>

      <VCardTitle class="text-h6 font-weight-bold">
        AI Virtual Coach Advice
      </VCardTitle>
      <VCardSubtitle class="text-caption">
        Physiological load analysis & daily training adaptation
      </VCardSubtitle>

      <template #append>
        <VChip
          size="small"
          color="success"
          variant="flat"
          class="font-weight-bold"
        >
          Readiness: 94%
        </VChip>
      </template>
    </VCardItem>

    <VCardText class="flex-grow-1 pt-2 d-flex flex-column justify-space-between">
      <!-- Coach Insight Bubble -->
      <div class="pa-3 rounded-lg coach-bubble mb-3">
        <div class="d-flex align-center gap-2 mb-2">
          <VIcon
            icon="bx-bulb"
            color="warning"
            size="20"
          />
          <span class="text-subtitle-2 font-weight-bold text-primary">
            Target Focus: Aerobic Assimilation
          </span>
        </div>
        <p class="text-body-2 text-medium-emphasis mb-2">
          "Great execution on Saturday's 22.4km long run. Your cardiac drift was exceptionally low (&lt;2.8%), proving your aerobic threshold base is fully dialed.
          Your form is <strong>+{{ ctlAtlForm.tsbForm }} TSB</strong>. Keep tomorrow's shakeout strictly in Zone 1/2 to supercompensate."
        </p>

        <div class="d-flex align-center gap-2 pt-2 border-t text-caption text-medium-emphasis">
          <VIcon
            icon="bx-check-double"
            color="success"
            size="16"
          />
          <span>Recommended Next: <strong>8.0 km Easy Shakeout @ 4:55/km + 4x100m Strides</strong></span>
        </div>
      </div>

      <!-- Recovery Vitals -->
      <div class="d-flex flex-column gap-2 mb-2">
        <div class="text-caption font-weight-bold text-uppercase text-disabled">
          Biomarkers & Recovery Signals
        </div>

        <VRow dense>
          <VCol cols="4">
            <div class="pa-2 rounded text-center recovery-metric">
              <div class="text-caption text-disabled">
                Resting HR
              </div>
              <div class="text-h6 font-weight-black text-success">
                42 <span class="text-caption">bpm</span>
              </div>
              <div class="text-caption text-success font-weight-bold" style="font-size: 0.65rem !important;">
                Optimal (-2)
              </div>
            </div>
          </VCol>

          <VCol cols="4">
            <div class="pa-2 rounded text-center recovery-metric">
              <div class="text-caption text-disabled">
                HRV Score
              </div>
              <div class="text-h6 font-weight-black text-info">
                78 <span class="text-caption">ms</span>
              </div>
              <div class="text-caption text-info font-weight-bold" style="font-size: 0.65rem !important;">
                Balanced (+6)
              </div>
            </div>
          </VCol>

          <VCol cols="4">
            <div class="pa-2 rounded text-center recovery-metric">
              <div class="text-caption text-disabled">
                Sleep Recovery
              </div>
              <div class="text-h6 font-weight-black text-primary">
                8h 14m
              </div>
              <div class="text-caption text-primary font-weight-bold" style="font-size: 0.65rem !important;">
                92% Quality
              </div>
            </div>
          </VCol>
        </VRow>
      </div>

      <!-- Action button -->
      <VBtn
        block
        variant="tonal"
        color="info"
        size="small"
        prepend-icon="bx-chat"
        to="/coach"
        class="mt-2"
      >
        Chat with Virtual Coach
      </VBtn>
    </VCardText>
  </VCard>
</template>

<style scoped>
.coach-bubble {
  background: rgba(var(--v-theme-surface), 0.7);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-left: 3px solid #03C3EC;
}

.recovery-metric {
  background: rgba(var(--v-theme-surface), 0.5);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
</style>
