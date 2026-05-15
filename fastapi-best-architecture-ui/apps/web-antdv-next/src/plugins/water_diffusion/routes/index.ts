import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    name: 'Demo',
    path: '/demo',
    meta: {
      title: '演示',
      icon: 'mdi:demo',
      order: 50,
    },
    children: [
      {
        name: 'PluginWaterDiffusion',
        path: '/demo/water-diffusion',
        component: () => import('#/plugins/water_diffusion/views/index.vue'),
        meta: {
          title: '地下水污染模拟',
          icon: 'mdi:water-circle',
        },
      },
    ],
  },
];

export default routes;
