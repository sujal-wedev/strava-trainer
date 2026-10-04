<script setup lang="ts">
import { useStravaData } from '@/composables/useStravaData'

const { stravaApi, syncWithStrava, isSyncing } = useStravaData()
</script>

<template>
  <div class="strava-sync-floater">
    <VBtn
      color="primary"
      variant="flat"
      rounded="pill"
      class="elevation-6 font-weight-bold d-flex align-center text-none px-4 py-2"
      :loading="isSyncing"
      to="/strava-connect"
    >
      <VIcon
        icon="bx-bolt-circle"
        class="me-2"
        size="20"
      />
      <span>Strava Active</span>
      <span class="pulse-dot ms-2" />
    </VBtn>
  </div>
</template>

<style scoped>
.strava-sync-floater {
  position: fixed;
  z-index: 999;
  bottom: 24px;
  right: 28px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #71DD37;
  display: inline-block;
  box-shadow: 0 0 0 0 rgba(113, 221, 55, 0.7);
  animation: pulse-ring 1.8s infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(113, 221, 55, 0.7);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 7px rgba(113, 221, 55, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(113, 221, 55, 0);
  }
}
</style>
