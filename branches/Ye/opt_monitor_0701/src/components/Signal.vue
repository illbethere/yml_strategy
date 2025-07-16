# npm run dev -- --host
<template>
  <div class="dashboard-root">
    <div class="top-area">
      <el-card class="table-card">
        <template #header>
          <div>1分钟数据 (所有期货)</div>
        </template>
        <el-checkbox-group v-model="selectedExchanges" style="margin-bottom: 8px;">
          <el-checkbox v-for="ex in exchangeList" :key="ex" :label="ex">{{ ex }}</el-checkbox>
        </el-checkbox-group>
        <div class="table-scroll">
          <el-table :data="filteredMin1Data" border height="100%" :row-class-name="tableRowClassName">
            <el-table-column v-for="col in min1Columns" :key="col.prop" :prop="col.prop" :label="col.label" />
          </el-table>
        </div>
      </el-card>
      <el-card class="table-card">
        <template #header>
          <div>期权持仓盈亏</div>
        </template>
        <el-checkbox-group v-model="selectedOptionExchanges" style="margin-bottom: 8px;">
          <el-checkbox v-for="ex in optionExchangeList" :key="ex" :label="ex">{{ ex }}</el-checkbox>
        </el-checkbox-group>
        <div class="table-scroll">
          <el-table :data="sortedFilteredOptionData" border :row-class-name="optionRowClassName">
            <el-table-column v-for="col in optionColumns" :key="col.prop" :prop="col.prop" :label="col.label"
              :sortable="col.sortable" />
          </el-table>
        </div>
      </el-card>
    </div>
    <div class="bottom-area">
      <el-card class="log-card">
        <template #header>
          <span>操作日志</span>
        </template>
        <div class="log-list">
          <div v-for="log in logs" :key="log.time + log.msg" class="log-item">
            <b>{{ log.time }}</b> - {{ log.msg }}
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'

const min1Data = ref([])
const optionData = ref([])
const logs = ref([])

const fetchAllData = async () => {
  try {
    const res = await axios.post('http://192.168.11.62:5173/api/update')
    if (res.data && res.data.results_all) min1Data.value = res.data.results_all
    if (res.data && res.data.logs) logs.value = res.data.logs
    const resOpt = await axios.get('http://192.168.11.62:5173/api/options')
    if (resOpt.data) optionData.value = resOpt.data
  } catch (e) {
    logs.value.push({ time: new Date().toLocaleTimeString(), msg: 'API请求失败' })
  }
}

onMounted(() => {
  fetchAllData()
  setInterval(fetchAllData, 1000)
})

// 1. 自动提取所有出现过的交易所
const exchangeList = computed(() => {
  const set = new Set(min1Data.value.map(row => row.contract.split('.').pop().toUpperCase()))
  return Array.from(set)
})

// 2. 被勾选的交易所，默认全部（响应式自动全选）
const selectedExchanges = ref([])

// 3. 当有新交易所出现时自动全选
watch(exchangeList, (val) => {
  if (val.length && selectedExchanges.value.length === 0) {
    selectedExchanges.value = val
  }
})

// 4. 根据checkbox过滤后的数据
const filteredMin1Data = computed(() => {
  if (!selectedExchanges.value.length) return []
  return min1Data.value.filter(row => {
    const ex = row.contract.split('.').pop().toUpperCase()
    return selectedExchanges.value.includes(ex)
  })
})

// 1. 自动提取所有option出现过的交易所
const optionExchangeList = computed(() => {
  const set = new Set(optionData.value.map(row => row.option_code.split('.').pop().toUpperCase()))
  return Array.from(set)
})

// 2. 被勾选的交易所（响应式tickbox），默认全部
const selectedOptionExchanges = ref([])

// 3. 新交易所出现时自动全选
watch(optionExchangeList, (val) => {
  if (val.length && selectedOptionExchanges.value.length === 0) {
    selectedOptionExchanges.value = val
  }
})

// 4. 根据checkbox过滤optionData
const filteredOptionData = computed(() => {
  if (!selectedOptionExchanges.value.length) return []
  return optionData.value.filter(row => {
    const ex = row.option_code.split('.').pop().toUpperCase()
    return selectedOptionExchanges.value.includes(ex)
  })
})

const sortedFilteredOptionData = computed(() => {
  // 浅拷贝一份再排序，避免影响源数据
  return [...filteredOptionData.value].sort((a, b) => (b.gain_loss || 0) - (a.gain_loss || 0))
})

const min1Columns = [
  { prop: 'contract', label: '合约' },
  { prop: 'signal', label: '信号' },
  { prop: 'pos', label: '正向' },
  { prop: 'neg', label: '负向' },
  { prop: 'strike', label: '行权价' },
  { prop: 'min', label: '最低价' },
  { prop: 'max', label: '最高价' },
  { prop: 'price', label: '当前价' },
]

const optionColumns = [
  { prop: 'option_code', label: '合约代码' },
  { prop: 'current_opt_price', label: '期权现价' },
  { prop: 'gain_loss', label: '浮动盈亏' },
  { prop: 'gain_loss_pct', label: '盈亏率(%)' },
  { prop: 'pos', label: '持仓数量' },
  { prop: 'alarm_price', label: '报警价' },
  { prop: 'iv', label: 'iv' },
  { prop: 'delta', label: 'delta' },

]

const tableRowClassName = ({ row }) => {
  if (row.signal === 1) return 'signal-green'
  if (row.signal === -1) return 'signal-red'
  return ''
}

const optionRowClassName = ({ row }) => {
  if (row.gain_loss > 0) return 'profit-row'
  if (row.gain_loss < 0) return 'loss-row'
  return ''
}

</script>

<style>
html,
body,
#app {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-root {
  min-height: 100vh;
  min-width: 100vw;
  background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 40%, #f0fdfa 100%);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  gap: 0;
  padding: 1% 1%;
}

.top-area {
  display: flex;
  flex: 1 1 0;
  /* ★ 自动撑满除日志区剩余空间 */
  gap: 24px;
  min-height: 0;
  /* ★ 保证flex溢出时内部可压缩 */
  align-items: stretch;
  padding-bottom: 1%;
}

.table-card {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

.table-scroll {
  flex: 1 1 0;
  /* ★ 自动占满卡片剩余空间 */
  min-height: 0;
  max-height: 60vh;
  overflow-y: auto;
  /* ★ 内容多了只在这里滚动 */
}

:deep(.el-table) {
  flex: 1 1 0;
  min-height: 120px;
  /* 表格无数据也不会塌陷 */
  background: transparent;
}

.bottom-area {
  height: 170px;
  min-height: 100px;
  display: flex;
  width: 100%;
}

.log-card {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  width: 100%;
  /* ★ 必须有 */
}

.log-list {
  flex: 1 1 0;
  max-height: 120px;
  min-height: 60px;
  overflow-y: auto;
  /* ★ 内容超出时自身滚动 */
  font-size: 14px;
  color: #222;
  padding-right: 8px;
}

.log-item {
  line-height: 1.8;
  border-bottom: 1px solid #e0e0e0;
}

.signal-green {
  background: #81fd81 !important;
}

.signal-red {
  background: #ff8181 !important;
}

.profit-row {
  background: #81fd81 !important;
}

.loss-row {
  background: #ff8181 !important;
}
</style>
