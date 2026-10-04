<script lang="ts" setup>
import AccountSettingsAccount from '@/views/pages/account-settings/AccountSettingsAccount.vue'
import AccountSettingsNotification from '@/views/pages/account-settings/AccountSettingsNotification.vue'
import AccountSettingsSecurity from '@/views/pages/account-settings/AccountSettingsSecurity.vue'
import AccountSettingsZones from '@/views/pages/account-settings/AccountSettingsZones.vue'

const route = useRoute()

const activeTab = ref(route.params.tab || 'account')

// tabs
const tabs = [
  { title: 'Athlete Profile', icon: 'bx-user', tab: 'account' },
  { title: 'Heart Rate & Zones', icon: 'bx-pulse', tab: 'zones' },
  { title: 'Security', icon: 'bx-lock-open', tab: 'security' },
  { title: 'Notifications', icon: 'bx-bell', tab: 'notification' },
]
</script>

<template>
  <div>
    <VTabs
      v-model="activeTab"
      show-arrows
      class="v-tabs-pill"
    >
      <VTab
        v-for="item in tabs"
        :key="item.icon"
        :value="item.tab"
      >
        <VIcon
          size="20"
          start
          :icon="item.icon"
        />
        {{ item.title }}
      </VTab>
    </VTabs>

    <VWindow
      v-model="activeTab"
      class="mt-5 disable-tab-transition"
    >
      <!-- Athlete Profile -->
      <VWindowItem value="account">
        <AccountSettingsAccount />
      </VWindowItem>

      <!-- Zones & Vitals -->
      <VWindowItem value="zones">
        <AccountSettingsZones />
      </VWindowItem>

      <!-- Security -->
      <VWindowItem value="security">
        <AccountSettingsSecurity />
      </VWindowItem>

      <!-- Notification -->
      <VWindowItem value="notification">
        <AccountSettingsNotification />
      </VWindowItem>
    </VWindow>
  </div>
</template>
