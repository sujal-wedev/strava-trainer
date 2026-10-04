<script setup lang="ts">
import { ref, computed } from 'vue'
import { useStravaData } from '@/composables/useStravaData'

const { gearList } = useStravaData()
const selectedType = ref('All')
const addGearDialog = ref(false)

const newGear = ref({
  name: '',
  brand: '',
  type: 'Shoes' as 'Shoes' | 'Bike',
  maxKm: 600,
})

const filteredGear = computed(() => {
  if (selectedType.value === 'All') return gearList.value
  return gearList.value.filter(g => g.type === selectedType.value)
})

const addNewGearItem = () => {
  if (!newGear.value.name) return
  gearList.value.push({
    id: `gear-${Date.now()}`,
    name: newGear.value.name,
    brand: newGear.value.brand || 'Custom',
    type: newGear.value.type,
    currentKm: 0,
    maxKm: Number(newGear.value.maxKm) || 600,
    status: 'good',
    photoIcon: newGear.value.type === 'Shoes' ? 'bx-run' : 'bx-cycling',
    activitiesCount: 0,
  })
  addGearDialog.value = false
  newGear.value.name = ''
  newGear.value.brand = ''
}

const getWearColor = (current: number, max: number) => {
  const pct = (current / max) * 100
  if (pct >= 85) return 'error'
  if (pct >= 65) return 'warning'
  return 'success'
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="d-flex flex-wrap align-center justify-space-between gap-3 mb-6">
      <div>
        <h2 class="text-h4 font-weight-bold text-high-emphasis mb-1">
          Gear & Shoe Mileage Garage
        </h2>
        <div class="text-body-2 text-medium-emphasis">
          Track shoe foam degradation, bike component wear, and avoid overuse injuries
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <VBtn
          color="primary"
          prepend-icon="bx-plus"
          @click="addGearDialog = true"
        >
          Add New Gear
        </VBtn>
      </div>
    </div>

    <!-- Filter Buttons -->
    <VCard class="mb-6">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4">
        <VBtnToggle
          v-model="selectedType"
          mandatory
          color="primary"
          variant="outlined"
          density="comfortable"
        >
          <VBtn value="All">All Equipment ({{ gearList.length }})</VBtn>
          <VBtn value="Shoes" prepend-icon="bx-run">Running Shoes</VBtn>
          <VBtn value="Bike" prepend-icon="bx-cycling">Bikes & Drivetrains</VBtn>
        </VBtnToggle>

        <div class="text-caption text-medium-emphasis">
          <VIcon icon="bx-info-circle" size="16" class="me-1 text-primary" />
          Recommended shoe replacement interval: 600 - 800 km
        </div>
      </VCardText>
    </VCard>

    <!-- Gear Grid -->
    <VRow>
      <VCol
        v-for="item in filteredGear"
        :key="item.id"
        cols="12"
        md="6"
        lg="4"
      >
        <VCard class="h-100 d-flex flex-column pa-2">
          <VCardItem class="pb-2">
            <template #prepend>
              <VAvatar
                :color="item.type === 'Shoes' ? 'primary' : 'info'"
                variant="tonal"
                size="44"
                rounded
                class="me-3"
              >
                <VIcon :icon="item.type === 'Shoes' ? 'bx-run' : 'bx-cycling'" size="26" />
              </VAvatar>
            </template>

            <VCardTitle class="text-h6 font-weight-bold">
              {{ item.name }}
            </VCardTitle>
            <VCardSubtitle class="text-caption">
              {{ item.brand }} • {{ item.activitiesCount }} logged activities
            </VCardSubtitle>

            <template #append>
              <VChip
                size="x-small"
                :color="getWearColor(item.currentKm, item.maxKm)"
                variant="tonal"
                class="font-weight-bold text-uppercase"
              >
                {{ Math.round((item.currentKm / item.maxKm) * 100) }}% Used
              </VChip>
            </template>
          </VCardItem>

          <VCardText class="flex-grow-1 pt-2 d-flex flex-column justify-space-between">
            <div class="pa-3 rounded bg-var-theme-background mb-3">
              <div class="d-flex justify-space-between align-center mb-1">
                <span class="text-caption text-disabled">Logged Mileage:</span>
                <span class="text-body-1 font-weight-black text-primary">{{ item.currentKm }} km</span>
              </div>
              <div class="d-flex justify-space-between align-center mb-2">
                <span class="text-caption text-disabled">Max Lifespan:</span>
                <span class="text-body-2 font-weight-semibold">{{ item.maxKm }} km</span>
              </div>

              <VProgressLinear
                :model-value="(item.currentKm / item.maxKm) * 100"
                :color="getWearColor(item.currentKm, item.maxKm)"
                height="8"
                rounded
              />

              <div class="d-flex justify-space-between text-caption text-medium-emphasis mt-2">
                <span>0 km</span>
                <span class="font-weight-bold" :class="`text-${getWearColor(item.currentKm, item.maxKm)}`">
                  {{ Math.max(item.maxKm - item.currentKm, 0) }} km remaining
                </span>
                <span>{{ item.maxKm }} km</span>
              </div>
            </div>

            <!-- Maintenance Advice -->
            <div class="d-flex align-center gap-2 text-caption">
              <VIcon
                :icon="(item.currentKm / item.maxKm) > 0.7 ? 'bx-error-circle' : 'bx-check-circle'"
                :color="getWearColor(item.currentKm, item.maxKm)"
                size="16"
              />
              <span v-if="(item.currentKm / item.maxKm) > 0.7" class="text-warning font-weight-medium">
                Cushioning rebound decreased. Consider transitioning to warmups.
              </span>
              <span v-else class="text-success font-weight-medium">
                Midsole response & outsole grip in prime racing shape.
              </span>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Add Gear Dialog -->
    <VDialog v-model="addGearDialog" max-width="480">
      <VCard title="Add Equipment to Garage">
        <VCardText>
          <VRow>
            <VCol cols="12">
              <VTextField
                v-model="newGear.name"
                label="Model Name (e.g. Nike Vaporfly 3)"
                variant="outlined"
              />
            </VCol>
            <VCol cols="6">
              <VTextField
                v-model="newGear.brand"
                label="Brand (e.g. Nike, Asics, Trek)"
                variant="outlined"
              />
            </VCol>
            <VCol cols="6">
              <VSelect
                v-model="newGear.type"
                label="Type"
                :items="['Shoes', 'Bike']"
                variant="outlined"
              />
            </VCol>
            <VCol cols="12">
              <VTextField
                v-model="newGear.maxKm"
                label="Expected Lifespan (km)"
                type="number"
                variant="outlined"
              />
            </VCol>
          </VRow>
        </VCardText>

        <VCardActions class="pa-4">
          <VSpacer />
          <VBtn variant="text" color="secondary" @click="addGearDialog = false">Cancel</VBtn>
          <VBtn variant="flat" color="primary" @click="addNewGearItem">Save Gear</VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </div>
</template>
