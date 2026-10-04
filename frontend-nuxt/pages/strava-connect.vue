<script setup lang="ts">
import { ref } from 'vue'
import { useStravaData } from '@/composables/useStravaData'

const { stravaApi, athlete, isSyncing, syncWithStrava } = useStravaData()

const testSyncSuccess = ref(false)
const showClientSecret = ref(false)

const triggerSync = async () => {
  await syncWithStrava()
  testSyncSuccess.value = true
  setTimeout(() => {
    testSyncSuccess.value = false
  }, 4000)
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="d-flex flex-wrap align-center justify-space-between gap-3 mb-6">
      <div>
        <h2 class="text-h4 font-weight-bold text-high-emphasis mb-1">
          Strava API & OAuth 2.0 Integration
        </h2>
        <div class="text-body-2 text-medium-emphasis">
          Manage developer credentials, athlete authorization tokens, and webhook push subscriptions
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <VBtn
          color="primary"
          prepend-icon="bx-sync"
          :loading="isSyncing"
          @click="triggerSync"
        >
          Test Sync Now
        </VBtn>
      </div>
    </div>

    <!-- Alert on successful sync -->
    <VAlert
      v-if="testSyncSuccess"
      type="success"
      variant="tonal"
      class="mb-6"
      closable
    >
      <strong>Strava API Sync Successful!</strong> 12 activities, 4 segment efforts, and current fitness CTL/ATL refreshed from Strava servers.
    </VAlert>

    <VRow>
      <!-- Left Column: Connection Status & Athlete Token -->
      <VCol cols="12" md="6">
        <!-- Connected Account Card -->
        <VCard class="mb-6">
          <VCardItem class="pb-2">
            <template #prepend>
              <VAvatar color="primary" variant="flat" rounded size="42" class="me-3">
                <VIcon icon="bx-bolt-circle" size="26" color="white" />
              </VAvatar>
            </template>
            <VCardTitle class="text-h6 font-weight-bold">
              Strava OAuth Authorization
            </VCardTitle>
            <VCardSubtitle class="text-caption">
              Athlete Profile & Token Link
            </VCardSubtitle>
            <template #append>
              <VChip color="success" size="small" variant="flat" class="font-weight-bold">
                ● Connected
              </VChip>
            </template>
          </VCardItem>

          <VCardText>
            <div class="d-flex align-center gap-3 pa-3 rounded bg-var-theme-background mb-4">
              <VAvatar size="48">
                <VImg :src="athlete.avatar" />
              </VAvatar>
              <div>
                <div class="font-weight-bold text-body-1">
                  {{ athlete.name }}
                </div>
                <div class="text-caption text-medium-emphasis">
                  Strava Athlete ID: <strong>{{ stravaApi.athleteId }}</strong> • Strava Summit Subscriber
                </div>
              </div>
            </div>

            <VList density="compact">
              <VListItem class="px-0 py-2 border-b">
                <VListItemTitle class="text-caption text-disabled">OAuth Scopes Granted</VListItemTitle>
                <template #append>
                  <div class="d-flex gap-1">
                    <VChip size="x-small" color="primary" variant="tonal">read</VChip>
                    <VChip size="x-small" color="primary" variant="tonal">activity:read_all</VChip>
                    <VChip size="x-small" color="primary" variant="tonal">profile:read_all</VChip>
                  </div>
                </template>
              </VListItem>

              <VListItem class="px-0 py-2 border-b">
                <VListItemTitle class="text-caption text-disabled">Access Token Expiry</VListItemTitle>
                <template #append>
                  <span class="text-caption font-weight-bold text-success">
                    Active (Renews in {{ stravaApi.tokenExpiresInHours }} hrs)
                  </span>
                </template>
              </VListItem>

              <VListItem class="px-0 py-2">
                <VListItemTitle class="text-caption text-disabled">Real-time Webhook Push</VListItemTitle>
                <template #append>
                  <VSwitch
                    v-model="stravaApi.webhookActive"
                    color="primary"
                    density="compact"
                    hide-details
                  />
                </template>
              </VListItem>
            </VList>

            <div class="d-flex gap-2 mt-4">
              <VBtn
                variant="outlined"
                color="primary"
                prepend-icon="bx-refresh"
                size="small"
                @click="triggerSync"
              >
                Refresh Bearer Token
              </VBtn>
              <VBtn
                variant="text"
                color="error"
                size="small"
              >
                Disconnect
              </VBtn>
            </div>
          </VCardText>
        </VCard>

        <!-- Rate Limits Card -->
        <VCard>
          <VCardItem class="pb-2">
            <template #prepend>
              <VAvatar color="info" variant="tonal" rounded size="36" class="me-2">
                <VIcon icon="bx-tachometer" size="20" />
              </VAvatar>
            </template>
            <VCardTitle class="text-h6 font-weight-bold">
              Strava API Rate Limits
            </VCardTitle>
            <VCardSubtitle class="text-caption">
              Compliant with Strava v3 throughput guidelines
            </VCardSubtitle>
          </VCardItem>

          <VCardText>
            <!-- 15-Minute Limit -->
            <div class="mb-4">
              <div class="d-flex justify-space-between text-caption mb-1">
                <span>15-Minute Window</span>
                <span class="font-weight-bold">{{ stravaApi.rateLimit15Min.used }} / {{ stravaApi.rateLimit15Min.limit }} requests</span>
              </div>
              <VProgressLinear
                :model-value="(stravaApi.rateLimit15Min.used / stravaApi.rateLimit15Min.limit) * 100"
                color="primary"
                height="8"
                rounded
              />
            </div>

            <!-- Daily Limit -->
            <div>
              <div class="d-flex justify-space-between text-caption mb-1">
                <span>Daily Limit (24 hours)</span>
                <span class="font-weight-bold">{{ stravaApi.rateLimitDaily.used }} / {{ stravaApi.rateLimitDaily.limit }} requests</span>
              </div>
              <VProgressLinear
                :model-value="(stravaApi.rateLimitDaily.used / stravaApi.rateLimitDaily.limit) * 100"
                color="success"
                height="8"
                rounded
              />
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Right Column: Developer API Credentials -->
      <VCol cols="12" md="6">
        <VCard>
          <VCardItem class="pb-2">
            <template #prepend>
              <VAvatar color="warning" variant="tonal" rounded size="36" class="me-2">
                <VIcon icon="bx-code-curly" size="20" />
              </VAvatar>
            </template>
            <VCardTitle class="text-h6 font-weight-bold">
              Strava App Credentials
            </VCardTitle>
            <VCardSubtitle class="text-caption">
              Created on strava.com/settings/api
            </VCardSubtitle>
          </VCardItem>

          <VCardText>
            <VRow>
              <VCol cols="12">
                <VTextField
                  v-model="stravaApi.clientId"
                  label="Strava Client ID"
                  variant="outlined"
                  hint="Your unique numeric Application ID"
                  persistent-hint
                />
              </VCol>

              <VCol cols="12">
                <VTextField
                  v-model="stravaApi.clientSecretMasked"
                  label="Client Secret"
                  :type="showClientSecret ? 'text' : 'password'"
                  :append-inner-icon="showClientSecret ? 'bx-show' : 'bx-hide'"
                  variant="outlined"
                  hint="Keep your Client Secret private"
                  persistent-hint
                  @click:append-inner="showClientSecret = !showClientSecret"
                />
              </VCol>

              <VCol cols="12">
                <VTextField
                  model-value="http://localhost:3000/api/auth/callback/strava"
                  label="OAuth Authorization Callback Domain"
                  readonly
                  variant="outlined"
                  append-inner-icon="bx-copy"
                />
              </VCol>

              <VCol cols="12">
                <VCheckbox
                  v-model="stravaApi.autoUploadWorkouts"
                  label="Automatically sync completed workouts to Strava"
                  density="compact"
                  hide-details
                />
                <VCheckbox
                  v-model="stravaApi.syncSegments"
                  label="Sync starred segments and leaderboard rankings"
                  density="compact"
                  hide-details
                />
              </VCol>

              <VCol cols="12">
                <VBtn
                  color="primary"
                  block
                  prepend-icon="bx-save"
                >
                  Save API Settings
                </VBtn>
              </VCol>
            </VRow>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>
