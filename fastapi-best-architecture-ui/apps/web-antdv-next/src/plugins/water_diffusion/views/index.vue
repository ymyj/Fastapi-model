<script lang="ts" setup>
import { Page } from '@vben/common-ui';

const backendUrl = 'http://localhost:8000';
</script>

<template>
  <Page
    class="h-full"
    description="模拟地下水污染物的垂向扩散过程，支持多地质分层、动态参数调整与实时可视化"
    title="地下水污染垂向扩散模拟"
  >
    <template #extra>
      <a
        :href="`${backendUrl}/simulations/water-diffusion/`"
        class="text-primary hover:underline"
        rel="noopener noreferrer"
        target="_blank"
      >
        在新窗口打开
      </a>
    </template>
    <div class="flex-1">
      <iframe
        :src="`${backendUrl}/simulations/water-diffusion/`"
        class="h-[calc(100vh-180px)] w-full rounded-md border-none"
        title="地下水污染垂向扩散模拟"
      />
    </div>
  </Page>
</template>
