# npm run dev -- --host
<template>
  <div class="dashboard-root">
    <!-- 账户导航栏 -->
    <div class="account-navbar">
      <el-card class="navbar-card">
        <div style="display: flex; align-items: center;">
          <span style="font-weight:bold; margin-right: 10px;">当前查看账户：</span>
          <el-select v-model="currentViewAccountId" placeholder="请选择账户" style="width: 220px;"
            @change="fetchAccountInfo">
            <el-option v-for="item in accountList" :key="item.account_id"
              :label="item.account_id + ' - ' + item.username + ' (' + item.account_type + ')'"
              :value="item.account_id" />
          </el-select>
          <span v-if="accountInfo" style="margin-left: 20px; color: #666;">更新时间：{{ accountInfo.update_time }}</span>
        </div>
      </el-card>
    </div>
    <!-- 账户状态显示区域 -->
    <div class="account-status">
      <el-card class="status-card">
        <template #header>
          <div>账户专属信息</div>
        </template>
        <div class="status-content">
          <div v-if="accountInfo">
            <div class="status-item"><span class="label">风险度:</span><span class="value">{{ accountInfo.risk }}</span>
            </div>
            <div class="status-item"><span class="label">资金:</span><span class="value">{{ accountInfo.balance }}</span>
            </div>
            <div class="status-item"><span class="label">持仓:</span>
              <span class="value" v-if="accountInfo.positions && accountInfo.positions.length">
                <span v-for="pos in accountInfo.positions" :key="pos.symbol" style="margin-right: 10px;">
                  {{ pos.symbol }}({{ pos.volume }}) <span
                    :style="{ color: pos.profit >= 0 ? '#67c23a' : '#f56c6c' }">{{
                      pos.profit }}</span>
                </span>
              </span>
              <span class="value" v-else>无</span>
            </div>
          </div>
          <div v-else style="color:#aaa;">请选择账户查看信息</div>
        </div>
      </el-card>
    </div>

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
            <el-table-column label="操作" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" @click="orderDialogOpen(scope.row)">下单</el-button>
              </template>
            </el-table-column>
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
    <el-dialog v-model="orderDialogVisible" title="下单" width="500px">
      <el-form :model="orderForm">
        <el-form-item label="子账户">
          <div style="margin-bottom: 10px;">
            <el-button size="small" @click="selectAllAccounts">全选</el-button>
            <el-button size="small" @click="clearAllAccounts">取消全选</el-button>
            <span style="margin-left: 10px; color: #666;">
              已选择 {{ orderForm.selected_accounts.length }}/{{ accountList.length }} 个账户
            </span>
          </div>
          <el-checkbox-group v-model="orderForm.selected_accounts" style="width: 100%;">
            <el-checkbox v-for="item in accountList" :key="item.account_id" :label="item.account_id"
              style="display: block; margin-bottom: 8px;">
              {{ item.account_id }} - {{ item.username }} ({{ item.account_type }})
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="合约">
          <el-input v-model="orderForm.contract" disabled />
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="orderForm.price" :min="0" />
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number v-model="orderForm.volume" :min="1" />
        </el-form-item>
        <el-form-item label="方向">
          <el-select v-model="orderForm.direction">
            <el-option label="买入" value="buy" />
            <el-option label="卖出" value="sell" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="orderDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitOrder" :disabled="orderForm.selected_accounts.length === 0">
          确认下单 ({{ orderForm.selected_accounts.length }}个账户)
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const min1Data = ref([])
const optionData = ref([])
const logs = ref([])
const accountList = ref([])
const accountInfo = ref(null) // 新增：用于存储当前查看账户的详细信息
const currentViewAccountId = ref('') // 新增：用于存储当前选中的账户ID

// 自动适配API地址
const API_HOST = window.location.hostname
const API_PORT = 5000
const API_BASE = `http://${API_HOST}:${API_PORT}`

// 你也可以手动指定（如：'http://192.168.11.64:5000'）
// const API_BASE = 'http://192.168.11.64:5000'

const fetchAllData = async () => {
  try {
    const res = await axios.post(`${API_BASE}/api/update`)
    if (res.data && res.data.results_all) min1Data.value = res.data.results_all
    if (res.data && res.data.logs) logs.value = res.data.logs
    const resOpt = await axios.get(`${API_BASE}/api/options`)
    if (resOpt.data) optionData.value = resOpt.data
  } catch (e) {
    let msg = 'API请求失败'
    if (e.response) {
      msg += `（状态码：${e.response.status}）`
    } else if (e.request) {
      msg += '（无法连接到后端，请检查网络和端口）'
    } else {
      msg += `（${e.message}）`
    }
    logs.value.push({ time: new Date().toLocaleTimeString(), msg })
  }
}

const fetchAccounts = async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/accounts`)
    accountList.value = res.data
    // 默认选第一个账户
    if (accountList.value.length && !currentViewAccountId.value) {
      currentViewAccountId.value = accountList.value[0].account_id
    }
  } catch (e) {
    accountList.value = []
  }
}

const fetchAccountInfo = async () => {
  if (!currentViewAccountId.value) {
    accountInfo.value = null
    return
  }
  try {
    const res = await axios.get(`${API_BASE}/api/account_info?account_id=${currentViewAccountId.value}`)
    if (res.data && res.data.status === 'ok') {
      accountInfo.value = res.data.data
    } else {
      accountInfo.value = null
    }
  } catch (e) {
    accountInfo.value = null
    let msg = '获取账户信息失败'
    if (e.response) {
      msg += `（状态码：${e.response.status}）`
    } else if (e.request) {
      msg += '（无法连接到后端，请检查网络和端口）'
    } else {
      msg += `（${e.message}）`
    }
    logs.value.push({ time: new Date().toLocaleTimeString(), msg })
  }
}

onMounted(() => {
  fetchAccounts()
  fetchAllData()
  setInterval(fetchAllData, 1000)
  // 页面加载后自动拉取一次账户信息
  watch(
    () => currentViewAccountId.value,
    () => fetchAccountInfo(),
    { immediate: true }
  )
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
  { prop: 'action', label: '操作' }, // 新增
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

const orderDialogVisible = ref(false)
const orderForm = ref({
  contract: '',
  price: 0,
  volume: 1,
  direction: 'buy',
  account_id: '', // 新增
  selected_accounts: [] // 新增
})

function orderDialogOpen(row) {
  orderForm.value = {
    contract: row.contract,
    price: row.price,
    volume: 1,
    direction: 'buy',
    selected_accounts: [] // 清空已选账户
  }
  orderDialogVisible.value = true
}

async function submitOrder() {
  try {
    if (orderForm.value.selected_accounts.length === 0) {
      ElMessage.warning('请至少选择一个子账户')
      return
    }

    // 为每个选中的账户发送下单请求
    const promises = orderForm.value.selected_accounts.map(async (account_id) => {
      try {
        const res = await axios.post(`${API_BASE}/api/order`, {
          contract: orderForm.value.contract,
          price: orderForm.value.price,
          volume: orderForm.value.volume,
          direction: orderForm.value.direction,
          account_id: account_id,
          order_type: 'option'
        })
        return { account_id, success: res.data.status === 'ok', msg: res.data.msg }
      } catch (e) {
        return { account_id, success: false, msg: e.message || '请求失败' }
      }
    })

    // 等待所有请求完成
    const results = await Promise.all(promises)

    // 统计结果
    const successCount = results.filter(r => r.success).length
    const failCount = results.length - successCount

    if (failCount === 0) {
      ElMessage.success(`下单成功！所有 ${successCount} 个账户下单成功`)
    } else if (successCount === 0) {
      ElMessage.error(`下单失败！所有 ${failCount} 个账户下单失败`)
    } else {
      ElMessage.warning(`部分成功！${successCount} 个成功，${failCount} 个失败`)
    }

    // 显示详细结果
    const successAccounts = results.filter(r => r.success).map(r => r.account_id)
    const failAccounts = results.filter(r => !r.success).map(r => r.account_id)

    if (successAccounts.length > 0) {
      console.log('成功账户:', successAccounts)
    }
    if (failAccounts.length > 0) {
      console.log('失败账户:', failAccounts)
    }

    orderDialogVisible.value = false
  } catch (e) {
    ElMessage.error('下单请求失败')
  }
}

function selectAllAccounts() {
  orderForm.value.selected_accounts = accountList.value.map(item => item.account_id)
}

function clearAllAccounts() {
  orderForm.value.selected_accounts = []
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

.account-navbar {
  margin-bottom: 1%;
  padding: 0 1%;
}

.navbar-card {
  background-color: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.account-status {
  margin-bottom: 1%;
  padding: 0 1%;
}

.status-card {
  background-color: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.status-content {
  padding: 10px 15px;
}

.status-item {
  margin-bottom: 5px;
  display: flex;
  align-items: center;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  color: #555;
  min-width: 80px;
}

.value {
  font-weight: bold;
  color: #333;
}

.connected {
  color: #67c23a;
  /* 绿色 */
}

.disconnected {
  color: #f56c6c;
  /* 红色 */
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
