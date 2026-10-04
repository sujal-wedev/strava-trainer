<script lang="ts" setup>
import VerticalNavSectionTitle from "@/@layouts/components/VerticalNavSectionTitle.vue";
import VerticalNavLink from "@layouts/components/VerticalNavLink.vue";
</script>

<template>
  <!-- 👉 Training Cockpit -->
  <VerticalNavSectionTitle
    :item="{
      heading: 'Training Cockpit',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Training Overview',
      icon: 'bx-pulse',
      to: '/dashboard',
      badgeContent: 'Active',
      badgeClass: 'bg-primary text-white',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Activities & GPS',
      icon: 'bx-run',
      to: '/activities',
      badgeContent: '12 New',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />

  <!-- 👉 Training & Plans -->
  <VerticalNavSectionTitle
    :item="{
      heading: 'Training & Coaching',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Training Plans',
      icon: 'bx-calendar',
      to: '/training-plans',
      badgeContent: 'Week 8',
      badgeClass: 'bg-light-success text-success',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'AI Virtual Coach',
      icon: 'bx-bot',
      to: '/coach',
      badgeContent: 'Optimal',
      badgeClass: 'bg-light-info text-info',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Segments & PRs',
      icon: 'bx-trophy',
      to: '/segments',
      badgeContent: '3 PRs',
      badgeClass: 'bg-light-warning text-warning',
    }"
  />

  <!-- 👉 Equipment & Community -->
  <VerticalNavSectionTitle
    :item="{
      heading: 'Equipment & Athlete',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Gear & Shoe Tracker',
      icon: 'bx-package',
      to: '/gear',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Athlete Settings',
      icon: 'bx-user',
      to: '/account-settings',
    }"
  />

  <!-- 👉 Integrations -->
  <VerticalNavSectionTitle
    :item="{
      heading: 'Strava Sync',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Strava API & OAuth',
      icon: 'bx-bolt-circle',
      to: '/strava-connect',
      badgeContent: 'Connected',
      badgeClass: 'bg-success text-white',
    }"
  />
</template>
