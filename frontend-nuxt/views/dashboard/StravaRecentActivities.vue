<script setup lang="ts">
import { useStravaData } from '@/composables/useStravaData'

const { recentActivities } = useStravaData()

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
  <VCard class="h-100 d-flex flex-column">
    <VCardItem class="pb-2">
      <template #prepend>
        <VAvatar
          color="primary"
          variant="tonal"
          rounded
          size="40"
          class="me-3"
        >
          <VIcon
            icon="bx-run"
            size="24"
          />
        </VAvatar>
      </template>

      <VCardTitle class="text-h6 font-weight-bold">
        Recent Strava Activities
      </VCardTitle>
      <VCardSubtitle class="text-caption">
        Synced live from Strava GPS devices & Apple Watch
      </VCardSubtitle>

      <template #append>
        <VBtn
          size="small"
          variant="text"
          color="primary"
          append-icon="bx-chevron-right"
          to="/activities"
        >
          View All (12)
        </VBtn>
      </template>
    </VCardItem>

    <VCardText class="flex-grow-1 pt-2">
      <VList class="card-list">
        <template
          v-for="(activity, index) in recentActivities"
          :key="activity.id"
        >
          <VListItem class="px-0 py-3">
            <template #prepend>
              <VAvatar
                :color="getSportColor(activity.type)"
                variant="tonal"
                rounded
                size="44"
                class="me-3"
              >
                <VIcon
                  :icon="getSportIcon(activity.type)"
                  size="24"
                />
              </VAvatar>
            </template>

            <VListItemTitle class="font-weight-bold text-body-1 mb-1">
              {{ activity.title }}
            </VListItemTitle>

            <VListItemSubtitle class="d-flex align-center flex-wrap gap-x-3 gap-y-1 text-caption">
              <span class="text-primary font-weight-bold">{{ activity.distance }}</span>
              <span>•</span>
              <span><VIcon icon="bx-time" size="14" class="me-1" />{{ activity.time }}</span>
              <span>•</span>
              <span><VIcon icon="bx-tachometer" size="14" class="me-1" />{{ activity.pace }}</span>
              <span>•</span>
              <span><VIcon icon="bx-trending-up" size="14" class="me-1" />{{ activity.elevation }}</span>
              <span>•</span>
              <span><VIcon icon="bx-heart" size="14" class="me-1 text-error" />{{ activity.avgHr }} bpm</span>
            </VListItemSubtitle>

            <template #append>
              <div class="text-end">
                <div class="d-flex align-center justify-end gap-1 mb-1">
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
                    🏆 {{ activity.trophies }} PR
                  </VChip>
                </div>
                <div class="text-caption text-medium-emphasis d-flex align-center justify-end gap-2">
                  <span><VIcon icon="bx-like" size="12" class="me-1 text-primary" />{{ activity.kudos }}</span>
                  <span><VIcon icon="bx-comment" size="12" class="me-1" />{{ activity.comments }}</span>
                  <span class="d-none d-sm-inline">{{ activity.date }}</span>
                </div>
              </div>
            </template>
          </VListItem>

          <VDivider v-if="index < recentActivities.length - 1" />
        </template>
      </VList>
    </VCardText>
  </VCard>
</template>
