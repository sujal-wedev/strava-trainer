<template>
  <div class="h-100 d-flex align-center justify-md-space-between justify-center text-medium-emphasis text-caption">
    <!-- 👉 Footer: left content -->
    <span class="d-flex align-center">
      &copy;
      {{ new Date().getFullYear() }}
      <span class="font-weight-bold text-primary mx-1">STRAVA TRAINER</span>
      — Powered by Vuetify & NuxtJS
    </span>
    <!-- 👉 Footer: right content -->
    <span class="d-md-flex gap-x-4 text-primary d-none">
      <NuxtLink to="/dashboard">Training Cockpit</NuxtLink>
      <NuxtLink to="/activities">Activities</NuxtLink>
      <NuxtLink to="/training-plans">Plans</NuxtLink>
      <NuxtLink to="/strava-connect">Strava API</NuxtLink>
    </span>
  </div>
</template>
