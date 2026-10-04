export interface StravaActivity {
  id: string
  title: string
  type: 'Run' | 'Ride' | 'Swim' | 'Workout'
  distance: string
  distanceKm: number
  time: string
  pace: string
  elevation: string
  elevationM: number
  avgHr: number
  maxHr: number
  calories: number
  sufferScore: number
  kudos: number
  comments: number
  trophies: number
  date: string
  gearName?: string
  notes?: string
}

export interface TrainingPlanWeek {
  weekNum: number
  title: string
  focus: string
  targetKm: number
  completedKm: number
  status: 'completed' | 'in-progress' | 'upcoming'
  workouts: {
    day: string
    title: string
    sport: 'Run' | 'Ride' | 'Swim' | 'Rest'
    distance: string
    targetPace: string
    status: 'done' | 'today' | 'planned'
  }[]
}

export interface GearItem {
  id: string
  name: string
  brand: string
  type: 'Shoes' | 'Bike'
  currentKm: number
  maxKm: number
  status: 'good' | 'warning' | 'replace'
  photoIcon: string
  activitiesCount: number
}

export const useStravaData = () => {
  const isSyncing = useState('strava_is_syncing', () => false)
  const lastSyncTime = useState('strava_last_sync', () => 'Just now')

  const athlete = useState('strava_athlete', () => ({
    name: 'Alex Morgan',
    username: '@alex_climber',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=250&q=80',
    location: 'Boulder, CO / Girona, Spain',
    club: 'Strava Pro Collective & Salomon Elite',
    badge: 'Pro Athlete',
    bio: 'Marathoner (PB 2:38:14) & 70.3 Triathlete. Sub-2:35 Valencia Marathon build.',
    stats: {
      activities: 1842,
      allTimeKm: 14850,
      trophies: 48,
      kudosReceived: '34.2k',
      following: 420,
      followers: 2890,
    },
    metrics: {
      vo2Max: 65,
      restingHr: 42,
      maxHr: 194,
      thresholdPace: '3:40 /km',
      ftpWatts: 290,
    },
  }))

  const weeklySummary = useState('strava_weekly_summary', () => ({
    currentKm: 64.8,
    targetKm: 75.0,
    progressPct: 86,
    activeTimeHours: 5.8,
    elevationClimbedM: 1280,
    sufferScore: 342,
    sufferCategory: 'Optimal Training Zone',
    activitiesCount: 6,
    vsLastWeekPct: 12.4,
  }))

  const ctlAtlForm = useState('strava_training_load', () => ({
    ctlFitness: 78,
    atlFatigue: 66,
    tsbForm: 12,
    formStatus: 'Fresh & Race Primed',
    formColor: 'success',
    acwrRatio: 0.98,
    acwrStatus: 'Sweet Spot (0.8 - 1.3)',
    history30Days: [
      { date: 'Sep 05', ctl: 62, atl: 58, tsb: 4 },
      { date: 'Sep 10', ctl: 65, atl: 68, tsb: -3 },
      { date: 'Sep 15', ctl: 68, atl: 74, tsb: -6 },
      { date: 'Sep 20', ctl: 71, atl: 70, tsb: 1 },
      { date: 'Sep 25', ctl: 74, atl: 82, tsb: -8 },
      { date: 'Sep 30', ctl: 76, atl: 72, tsb: 4 },
      { date: 'Oct 04', ctl: 78, atl: 66, tsb: 12 },
    ],
  }))

  const recentActivities = useState<StravaActivity[]>('strava_recent_activities', () => [
    {
      id: 'act-101',
      title: 'Saturday Marathon Pace Progressive Long Run 🏃‍♂️💨',
      type: 'Run',
      distance: '22.4 km',
      distanceKm: 22.4,
      time: '1h 41m 24s',
      pace: '4:31 /km',
      elevation: '245 m',
      elevationM: 245,
      avgHr: 154,
      maxHr: 172,
      calories: 1640,
      sufferScore: 142,
      kudos: 56,
      comments: 7,
      trophies: 3,
      date: 'Today at 07:15 AM',
      gearName: 'Nike Alphafly 3 Proto',
      notes: 'Strong splits on the second half. Heart rate stayed well within Zone 3 threshold.',
    },
    {
      id: 'act-102',
      title: 'Tempo Threshold Mountain Pass Climb 🚴⚡',
      type: 'Ride',
      distance: '48.6 km',
      distanceKm: 48.6,
      time: '1h 28m 40s',
      pace: '32.9 km/h',
      elevation: '680 m',
      elevationM: 680,
      avgHr: 146,
      maxHr: 168,
      calories: 1220,
      sufferScore: 112,
      kudos: 39,
      comments: 4,
      trophies: 2,
      date: 'Yesterday at 05:30 PM',
      gearName: 'Specialized S-Works SL8',
      notes: 'Cadence averaged 92 rpm. Crisp power transfer on the switchbacks.',
    },
    {
      id: 'act-103',
      title: 'Track Tuesday: 6x1000m @ 3:32/km (Fast cadence) 🔥',
      type: 'Run',
      distance: '13.5 km',
      distanceKm: 13.5,
      time: '59m 10s',
      pace: '4:23 /km',
      elevation: '45 m',
      elevationM: 45,
      avgHr: 166,
      maxHr: 184,
      calories: 980,
      sufferScore: 98,
      kudos: 44,
      comments: 9,
      trophies: 4,
      date: 'Oct 2, 2026',
      gearName: 'Asics Superblast 2',
      notes: 'Consistency: 3:32, 3:33, 3:31, 3:32, 3:30, 3:28. Recoveries were 200m jog.',
    },
    {
      id: 'act-104',
      title: 'Threshold Interval Swim & Open Water Prep 🏊',
      type: 'Swim',
      distance: '2,600 m',
      distanceKm: 2.6,
      time: '46m 30s',
      pace: '1:47 /100m',
      elevation: '0 m',
      elevationM: 0,
      avgHr: 138,
      maxHr: 154,
      calories: 610,
      sufferScore: 54,
      kudos: 24,
      comments: 2,
      trophies: 1,
      date: 'Sep 30, 2026',
      notes: 'Felt buoyant and smooth. 10x100m off 1:40 leaving plenty in the tank.',
    },
  ])

  const gearList = useState<GearItem[]>('strava_gear', () => [
    {
      id: 'gear-1',
      name: 'Nike Alphafly 3 Proto',
      brand: 'Nike',
      type: 'Shoes',
      currentKm: 285,
      maxKm: 600,
      status: 'good',
      photoIcon: 'bx-run',
      activitiesCount: 22,
    },
    {
      id: 'gear-2',
      name: 'Asics Superblast 2',
      brand: 'Asics',
      type: 'Shoes',
      currentKm: 540,
      maxKm: 750,
      status: 'warning',
      photoIcon: 'bx-run',
      activitiesCount: 46,
    },
    {
      id: 'gear-3',
      name: 'Saucony Endorphin Speed 4',
      brand: 'Saucony',
      type: 'Shoes',
      currentKm: 195,
      maxKm: 600,
      status: 'good',
      photoIcon: 'bx-run',
      activitiesCount: 18,
    },
    {
      id: 'gear-4',
      name: 'Specialized S-Works Tarmac SL8',
      brand: 'Specialized',
      type: 'Bike',
      currentKm: 2650,
      maxKm: 8000,
      status: 'good',
      photoIcon: 'bx-cycling',
      activitiesCount: 64,
    },
    {
      id: 'gear-5',
      name: 'Trek Madone SLR 9 eTap',
      brand: 'Trek',
      type: 'Bike',
      currentKm: 4320,
      maxKm: 8000,
      status: 'warning',
      photoIcon: 'bx-cycling',
      activitiesCount: 92,
    },
  ])

  const trainingPlan = useState<TrainingPlanWeek[]>('strava_training_plan', () => [
    {
      weekNum: 7,
      title: 'Week 7: High Volume Threshold Aerobics',
      focus: 'Aerobic base + 2x threshold quality sessions',
      targetKm: 72,
      completedKm: 72.8,
      status: 'completed',
      workouts: [
        { day: 'Mon', title: 'Recovery Aerobic Run', sport: 'Run', distance: '8 km', targetPace: '5:05/km', status: 'done' },
        { day: 'Tue', title: 'Threshold Cruise Intervals (5x1.5k)', sport: 'Run', distance: '14 km', targetPace: '3:45/km', status: 'done' },
        { day: 'Wed', title: 'Endurance Base Spin', sport: 'Ride', distance: '40 km', targetPace: '31 km/h', status: 'done' },
        { day: 'Thu', title: 'Steady State Run', sport: 'Run', distance: '12 km', targetPace: '4:25/km', status: 'done' },
        { day: 'Fri', title: 'Active Recovery & Swim', sport: 'Swim', distance: '2 km', targetPace: '1:55/100m', status: 'done' },
        { day: 'Sat', title: 'Long Run with MP blocks', sport: 'Run', distance: '24 km', targetPace: '4:20/km', status: 'done' },
        { day: 'Sun', title: 'Full Rest & Foam Roll', sport: 'Rest', distance: '0 km', targetPace: '-', status: 'done' },
      ],
    },
    {
      weekNum: 8,
      title: 'Week 8: Peak Specificity & VO2 Max (Current)',
      focus: 'Marathon pace consolidation and speed endurance',
      targetKm: 75,
      completedKm: 64.8,
      status: 'in-progress',
      workouts: [
        { day: 'Mon', title: 'Easy Recovery Run', sport: 'Run', distance: '8.2 km', targetPace: '5:00/km', status: 'done' },
        { day: 'Tue', title: 'Track 6x1000m VO2 Max', sport: 'Run', distance: '13.5 km', targetPace: '3:32/km', status: 'done' },
        { day: 'Wed', title: 'Mountain Pass Aerobic Climb', sport: 'Ride', distance: '48.6 km', targetPace: '32.9 km/h', status: 'done' },
        { day: 'Thu', title: 'Threshold Run', sport: 'Run', distance: '11.0 km', targetPace: '4:15/km', status: 'done' },
        { day: 'Fri', title: 'Recovery Swim', sport: 'Swim', distance: '2.6 km', targetPace: '1:47/100m', status: 'done' },
        { day: 'Sat', title: 'Progressive Long Run (22km)', sport: 'Run', distance: '22.4 km', targetPace: '4:31/km', status: 'done' },
        { day: 'Sun', title: 'Sunday Easy Shakeout + 4 Strides', sport: 'Run', distance: '8.0 km', targetPace: '4:55/km', status: 'today' },
      ],
    },
    {
      weekNum: 9,
      title: 'Week 9: Recovery & Absorption Week',
      focus: 'Volume reduction (-25%) to supercompensate fitness',
      targetKm: 55,
      completedKm: 0,
      status: 'upcoming',
      workouts: [
        { day: 'Mon', title: 'Rest & Mobility', sport: 'Rest', distance: '0 km', targetPace: '-', status: 'planned' },
        { day: 'Tue', title: 'Short Fartlek Run', sport: 'Run', distance: '10 km', targetPace: '4:10/km', status: 'planned' },
        { day: 'Wed', title: 'Easy Recovery Ride', sport: 'Ride', distance: '30 km', targetPace: '28 km/h', status: 'planned' },
        { day: 'Thu', title: 'Aerobic Base Run', sport: 'Run', distance: '10 km', targetPace: '4:45/km', status: 'planned' },
        { day: 'Fri', title: 'Technique Swim', sport: 'Swim', distance: '2 km', targetPace: '1:50/100m', status: 'planned' },
        { day: 'Sat', title: 'Moderate Long Run', sport: 'Run', distance: '16 km', targetPace: '4:35/km', status: 'planned' },
        { day: 'Sun', title: 'Rest & Stretch', sport: 'Rest', distance: '0 km', targetPace: '-', status: 'planned' },
      ],
    },
  ])

  const stravaApi = useState('strava_api_config', () => ({
    isConnected: true,
    athleteId: '19482014',
    athleteName: 'Alex Morgan',
    clientId: '149832',
    clientSecretMasked: '••••••••••••••••••••••••39ba',
    accessTokenMasked: '92fb••••••••••••••••••••••••10ab',
    tokenExpiresInHours: 4.8,
    rateLimit15Min: { used: 142, limit: 600 },
    rateLimitDaily: { used: 480, limit: 30000 },
    webhookActive: true,
    autoUploadWorkouts: true,
    syncSegments: true,
  }))

  const syncWithStrava = async () => {
    isSyncing.value = true
    await new Promise(resolve => setTimeout(resolve, 1400))
    isSyncing.value = false
    lastSyncTime.value = 'Just now'
  }

  return {
    athlete,
    weeklySummary,
    ctlAtlForm,
    recentActivities,
    gearList,
    trainingPlan,
    stravaApi,
    isSyncing,
    lastSyncTime,
    syncWithStrava,
  }
}
