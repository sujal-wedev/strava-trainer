<script setup lang="ts">
const personalRecords = [
  { distance: '1 km', time: '2:48', pace: '2:48/km', date: 'Jul 2025', activity: 'Track Speed Session' },
  { distance: '1 Mile', time: '4:36', pace: '2:51/km', date: 'Aug 2025', activity: 'Mile Championship' },
  { distance: '5 km', time: '15:42', pace: '3:08/km', date: 'Nov 2025', activity: 'Boulder Autumn 5K' },
  { distance: '10 km', time: '32:18', pace: '3:13/km', date: 'Mar 2026', activity: 'Valencia 10K Road Race' },
  { distance: 'Half Marathon', time: '1:12:44', pace: '3:26/km', date: 'May 2026', activity: 'Berlin Half Marathon' },
  { distance: 'Marathon', time: '2:38:14', pace: '3:45/km', date: 'Dec 2025', activity: 'Valencia Marathon 2025' },
  { distance: '40 km Time Trial (Bike)', time: '54m 12s', pace: '44.2 km/h', date: 'Jun 2026', activity: 'Girona Coastal TT' },
]

const topSegments = [
  {
    name: 'Flagstaff Mountain Climb (Boulder)',
    distance: '5.2 km',
    avgGrade: '7.8%',
    elevationGain: '405 m',
    myBest: '16m 42s',
    myRank: '4th overall (Top 1%)',
    komTime: '15m 12s',
    trophy: 'KOM Contender',
    type: 'Ride',
  },
  {
    name: 'Magnolia Road Long Dirt Sprint',
    distance: '3.8 km',
    avgGrade: '3.2%',
    elevationGain: '122 m',
    myBest: '12m 04s',
    myRank: '1st Overall 👑 (KOM)',
    komTime: '12m 04s',
    trophy: 'Current Crown',
    type: 'Run',
  },
  {
    name: 'Els Àngels Classic Ascent (Girona)',
    distance: '10.1 km',
    avgGrade: '4.6%',
    elevationGain: '468 m',
    myBest: '26m 18s',
    myRank: '8th of 4,200',
    komTime: '24m 02s',
    trophy: 'Top 10 Cup',
    type: 'Ride',
  },
  {
    name: 'Boulder Reservoir Flat 5K Loop',
    distance: '5.0 km',
    avgGrade: '0.4%',
    elevationGain: '18 m',
    myBest: '15m 48s',
    myRank: '2nd overall',
    komTime: '15m 32s',
    trophy: 'Silver Cup',
    type: 'Run',
  },
]
</script>

<template>
  <div>
    <!-- Header -->
    <div class="d-flex flex-wrap align-center justify-space-between gap-3 mb-6">
      <div>
        <h2 class="text-h4 font-weight-bold text-high-emphasis mb-1">
          Segments & Personal Records (PRs)
        </h2>
        <div class="text-body-2 text-medium-emphasis">
          Historical benchmarks, KOM/QOM trophies, and local leaderboard efforts
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <VChip
          color="warning"
          size="default"
          variant="flat"
          class="font-weight-bold"
        >
          👑 1 KOM Crown • 48 Trophies
        </VChip>
      </div>
    </div>

    <!-- Personal Records Table -->
    <VCard class="mb-6">
      <VCardItem class="pb-2">
        <template #prepend>
          <VAvatar color="warning" variant="tonal" rounded size="40" class="me-3">
            <VIcon icon="bx-trophy" size="24" />
          </VAvatar>
        </template>
        <VCardTitle class="text-h6 font-weight-bold">
          All-Time Personal Bests
        </VCardTitle>
        <VCardSubtitle class="text-caption">
          Verified Strava GPS race and workout splits
        </VCardSubtitle>
      </VCardItem>

      <VTable class="elevation-0">
        <thead>
          <tr>
            <th class="text-uppercase text-caption font-weight-bold">Distance</th>
            <th class="text-uppercase text-caption font-weight-bold">Record Time</th>
            <th class="text-uppercase text-caption font-weight-bold">Pace</th>
            <th class="text-uppercase text-caption font-weight-bold">Date</th>
            <th class="text-uppercase text-caption font-weight-bold">Activity Name</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pr in personalRecords" :key="pr.distance">
            <td class="font-weight-bold text-body-1">{{ pr.distance }}</td>
            <td class="font-weight-black text-primary text-body-1">{{ pr.time }}</td>
            <td class="font-weight-medium">{{ pr.pace }}</td>
            <td class="text-medium-emphasis">{{ pr.date }}</td>
            <td class="text-medium-emphasis font-weight-medium">{{ pr.activity }}</td>
          </tr>
        </tbody>
      </VTable>
    </VCard>

    <!-- Top Segments & Leaderboards -->
    <h3 class="text-h5 font-weight-bold mb-4">
      Featured Strava Segments & Crowns
    </h3>

    <VRow>
      <VCol
        v-for="seg in topSegments"
        :key="seg.name"
        cols="12"
        md="6"
      >
        <VCard class="h-100 pa-2">
          <VCardItem class="pb-2">
            <template #prepend>
              <VAvatar
                :color="seg.type === 'Run' ? 'primary' : 'info'"
                variant="tonal"
                rounded
                size="40"
                class="me-3"
              >
                <VIcon :icon="seg.type === 'Run' ? 'bx-run' : 'bx-cycling'" size="24" />
              </VAvatar>
            </template>
            <VCardTitle class="text-h6 font-weight-bold">
              {{ seg.name }}
            </VCardTitle>
            <VCardSubtitle class="text-caption">
              {{ seg.distance }} • {{ seg.avgGrade }} avg grade • +{{ seg.elevationGain }}
            </VCardSubtitle>
            <template #append>
              <VChip color="warning" size="small" variant="flat" class="font-weight-bold">
                {{ seg.trophy }}
              </VChip>
            </template>
          </VCardItem>

          <VCardText class="pt-2">
            <div class="pa-3 rounded bg-var-theme-background d-flex justify-space-between align-center mb-2">
              <div>
                <div class="text-caption text-disabled">My Personal Record</div>
                <div class="text-h6 font-weight-black text-primary">{{ seg.myBest }}</div>
                <div class="text-caption text-success font-weight-semibold">{{ seg.myRank }}</div>
              </div>

              <div class="text-end">
                <div class="text-caption text-disabled">Overall KOM Time</div>
                <div class="text-h6 font-weight-bold">{{ seg.komTime }}</div>
                <div class="text-caption text-disabled">Leaderboard record</div>
              </div>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>
