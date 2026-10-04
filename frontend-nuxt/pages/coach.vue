<script setup lang="ts">
import { ref } from 'vue'
import { useStravaData } from '@/composables/useStravaData'

const { athlete, ctlAtlForm } = useStravaData()

interface ChatMessage {
  sender: 'coach' | 'athlete'
  text: string
  time: string
}

const chatMessages = ref<ChatMessage[]>([
  {
    sender: 'coach',
    text: 'Good morning, Alex! Your recovery biomarkers look outstanding today. Resting HR dropped to 42 bpm and HRV is at 78 ms. Your Form is +12 TSB. How do your legs feel after Saturday’s 22.4 km progressive run?',
    time: '08:00 AM',
  },
  {
    sender: 'athlete',
    text: 'Legs feel surprisingly bouncy. My hamstrings were slightly tight on kilometer 18 yesterday, but foam rolling helped.',
    time: '08:05 AM',
  },
  {
    sender: 'coach',
    text: 'Excellent. Your cardiac drift on that run was under 2.8%, which is world-class aerobic decoupling for a 1h 41m effort. For today, stick strictly to the 8.0 km easy shakeout (4:55-5:10/km) plus 4 relaxed 100m strides to keep neuromuscular firing without adding glycogen stress.',
    time: '08:06 AM',
  },
])

const userInput = ref('')

const sendMessage = () => {
  if (!userInput.value.trim()) return

  chatMessages.value.push({
    sender: 'athlete',
    text: userInput.value,
    time: 'Just now',
  })

  const question = userInput.value.toLowerCase()
  userInput.value = ''

  setTimeout(() => {
    let reply = "Based on your current training load (CTL 78, ATL 66), your body is adapting smoothly. Maintain high protein intake (1.8g/kg) and ensure you stay hydrated with 2.8L water + electrolytes."
    if (question.includes('shoe') || question.includes('carbon') || question.includes('plate')) {
      reply = "For Sunday's shakeout, use your Asics Superblast 2 or daily trainer. Save the Nike Alphafly 3 for race-pace simulations and long runs over 28km to prevent unnecessary tendon strain."
    } else if (question.includes('rest') || question.includes('tired') || question.includes('sore')) {
      reply = "If you notice persistent fatigue, feel free to swap today's 8km run for a 35-minute easy spin on the bike or an active mobility session. Remember: fitness is gained during recovery, not exhaustion!"
    } else if (question.includes('fuel') || question.includes('gel') || question.includes('eat')) {
      reply = "Aim for 60-80g of carbohydrates per hour during your Sunday long runs (roughly one Maurten or SiS gel every 25-30 minutes). Practice your race-day fueling protocol now!"
    }

    chatMessages.value.push({
      sender: 'coach',
      text: reply,
      time: 'Just now',
    })
  }, 700)
}

const quickPrompts = [
  'Should I wear carbon plate shoes for easy runs?',
  'My legs feel heavy, can I cross-train on the bike?',
  'How many carbs per hour should I consume during 25km+ runs?',
]

const askQuick = (prompt: string) => {
  userInput.value = prompt
  sendMessage()
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="d-flex flex-wrap align-center justify-space-between gap-3 mb-6">
      <div>
        <h2 class="text-h4 font-weight-bold text-high-emphasis mb-1">
          AI Virtual Coach & Performance Lab
        </h2>
        <div class="text-body-2 text-medium-emphasis">
          Real-time physiological load modeling, recovery intelligence, and training adjustments
        </div>
      </div>

      <div class="d-flex align-center gap-2">
        <VChip
          color="success"
          size="default"
          variant="flat"
          class="font-weight-bold"
        >
          <VIcon start icon="bx-pulse" />
          Optimal Readiness (94%)
        </VChip>
      </div>
    </div>

    <VRow>
      <!-- Left Column: Biomarkers & Safety Ratios -->
      <VCol cols="12" md="5">
        <!-- ACWR Safety Meter -->
        <VCard class="mb-4">
          <VCardItem class="pb-2">
            <template #prepend>
              <VAvatar color="primary" variant="tonal" rounded size="36" class="me-2">
                <VIcon icon="bx-tachometer" size="20" />
              </VAvatar>
            </template>
            <VCardTitle class="text-h6 font-weight-bold">
              Acute-to-Chronic Workload Ratio
            </VCardTitle>
            <VCardSubtitle class="text-caption">
              Injury risk prevention & training spikes detection
            </VCardSubtitle>
          </VCardItem>

          <VCardText>
            <div class="text-center py-4">
              <div class="text-h2 font-weight-black text-primary mb-1">
                {{ ctlAtlForm.acwrRatio }}
              </div>
              <VChip color="success" size="small" variant="tonal" class="font-weight-bold">
                Optimal Sweet Spot (0.8 - 1.3)
              </VChip>
              <p class="text-caption text-medium-emphasis mt-2 mb-0">
                Workload is balanced perfectly. Injury risk is evaluated at &lt; 8%.
              </p>
            </div>

            <VDivider class="my-3" />

            <div class="d-flex justify-space-between text-caption mb-1">
              <span>Undertraining (&lt; 0.8)</span>
              <span class="font-weight-bold text-success">Sweet Spot (0.8 - 1.3)</span>
              <span class="text-error">Danger Zone (&gt; 1.5)</span>
            </div>
            <VProgressLinear
              :model-value="65"
              color="success"
              height="8"
              rounded
            />
          </VCardText>
        </VCard>

        <!-- Recovery Biomarkers Grid -->
        <VCard>
          <VCardItem class="pb-2">
            <template #prepend>
              <VAvatar color="info" variant="tonal" rounded size="36" class="me-2">
                <VIcon icon="bx-dna" size="20" />
              </VAvatar>
            </template>
            <VCardTitle class="text-h6 font-weight-bold">
              Recovery Biomarkers
            </VCardTitle>
          </VCardItem>

          <VCardText>
            <VList density="compact">
              <VListItem class="px-0 py-2 border-b">
                <template #prepend>
                  <VIcon icon="bx-heart" color="error" class="me-3" />
                </template>
                <VListItemTitle class="font-weight-medium">Resting Heart Rate</VListItemTitle>
                <VListItemSubtitle class="text-caption">Baseline: 44 bpm</VListItemSubtitle>
                <template #append>
                  <span class="text-h6 font-weight-bold text-success">42 bpm</span>
                </template>
              </VListItem>

              <VListItem class="px-0 py-2 border-b">
                <template #prepend>
                  <VIcon icon="bx-pulse" color="info" class="me-3" />
                </template>
                <VListItemTitle class="font-weight-medium">Heart Rate Variability (HRV)</VListItemTitle>
                <VListItemSubtitle class="text-caption">Autonomic balance</VListItemSubtitle>
                <template #append>
                  <span class="text-h6 font-weight-bold text-info">78 ms</span>
                </template>
              </VListItem>

              <VListItem class="px-0 py-2 border-b">
                <template #prepend>
                  <VIcon icon="bx-moon" color="primary" class="me-3" />
                </template>
                <VListItemTitle class="font-weight-medium">Sleep Recovery Duration</VListItemTitle>
                <VListItemSubtitle class="text-caption">Deep + REM: 3h 18m</VListItemSubtitle>
                <template #append>
                  <span class="text-h6 font-weight-bold text-primary">8h 14m</span>
                </template>
              </VListItem>

              <VListItem class="px-0 py-2">
                <template #prepend>
                  <VIcon icon="bx-droplet" color="warning" class="me-3" />
                </template>
                <VListItemTitle class="font-weight-medium">Hydration & Sweat Loss</VListItemTitle>
                <VListItemSubtitle class="text-caption">Target replenishment</VListItemSubtitle>
                <template #append>
                  <span class="text-h6 font-weight-bold text-warning">2.8 L</span>
                </template>
              </VListItem>
            </VList>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Right Column: Interactive AI Coach Chat -->
      <VCol cols="12" md="7">
        <VCard class="d-flex flex-column" style="min-height: 580px;">
          <!-- Chat Header -->
          <VCardItem class="border-b pa-4">
            <template #prepend>
              <VBadge dot color="success" offset-x="2" offset-y="2">
                <VAvatar color="info" variant="flat" size="44">
                  <VIcon icon="bx-bot" size="26" color="white" />
                </VAvatar>
              </VBadge>
            </template>
            <VCardTitle class="text-h6 font-weight-bold">
              Strava AI Performance Coach
            </VCardTitle>
            <VCardSubtitle class="text-caption">
              Trained on Strava telemetry, exercise science, and {{ athlete.name }}'s history
            </VCardSubtitle>
          </VCardItem>

          <!-- Chat History -->
          <VCardText class="flex-grow-1 overflow-y-auto pa-4 d-flex flex-column gap-3" style="max-height: 400px;">
            <div
              v-for="(msg, idx) in chatMessages"
              :key="idx"
              class="d-flex"
              :class="msg.sender === 'athlete' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="pa-3 rounded-lg max-w-75"
                :class="msg.sender === 'athlete' ? 'bg-primary text-white' : 'bg-var-theme-background border'"
                style="max-width: 80%;"
              >
                <p class="text-body-2 mb-1" style="white-space: pre-wrap;">
                  {{ msg.text }}
                </p>
                <div
                  class="text-caption text-end"
                  :class="msg.sender === 'athlete' ? 'text-white-50' : 'text-disabled'"
                  style="font-size: 0.65rem !important;"
                >
                  {{ msg.time }}
                </div>
              </div>
            </div>
          </VCardText>

          <!-- Quick Suggestions -->
          <div class="px-4 pb-2 d-flex flex-wrap gap-2 border-t pt-2">
            <span class="text-caption text-disabled align-self-center">Suggested:</span>
            <VChip
              v-for="(prompt, idx) in quickPrompts"
              :key="idx"
              size="x-small"
              variant="outlined"
              color="primary"
              class="cursor-pointer"
              @click="askQuick(prompt)"
            >
              {{ prompt }}
            </VChip>
          </div>

          <!-- Chat Input -->
          <div class="pa-4 pt-1">
            <div class="d-flex align-center gap-2">
              <VTextField
                v-model="userInput"
                placeholder="Ask your coach anything about paces, workouts, or fueling..."
                variant="outlined"
                density="compact"
                hide-details
                @keyup.enter="sendMessage"
              />
              <VBtn
                color="primary"
                variant="flat"
                icon="bx-send"
                @click="sendMessage"
              />
            </div>
          </div>
        </VCard>
      </VCol>
    </VRow>
  </div>
</template>
