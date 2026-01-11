<template>
  <div class="app-wrapper">
    <div v-if="!selectedItem" class="search-view">
      <div class="search-container">
      <h1 class="main-title">影视大数据检索系统</h1>

      <!-- 模式切换：单独一行，居中 -->
      <div class="dataset-switch">
        <el-radio-group v-model="currentView" size="large">
          <el-radio-button label="movie">电影数据集</el-radio-button>
          <el-radio-button label="short">短剧数据集</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 搜索框 -->
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="请输入名称..."
          @keyup.enter="handleSearch"
          class="big-input"
        >
          <template #append>
            <el-button @click="handleSearch" type="primary">搜索</el-button>
          </template>
        </el-input>
        <p v-if="searchError" class="error-tip">{{ searchError }}</p>
      </div>


        <div v-if="results.length === 0 && !searchError" class="recommend-section">
          <div v-if="currentView === 'movie'">
            <h3 class="rec-title">🔥 高分电影推荐</h3>
            <div class="results-grid">
              <el-card v-for="(item, i) in movieRecs" :key="'m'+i" class="result-mini-card" @click="enterDetail(item)">
                <div class="card-image-wrapper">
                  <img :src="getImageUrl(item.image)" class="card-image" alt="电影海报">
                </div>
                <div class="mini-header">
                  <span class="mini-title">{{ item.title }}</span>
                  <el-tag type="warning" effect="dark" size="small">{{ item.rating }}</el-tag>
                </div>
                <p class="mini-desc">{{ item.genre }}</p>
                <el-button type="text">进入详情分析 >></el-button>
              </el-card>
            </div>
          </div>

          <div v-else>
            <h3 class="rec-title">⚡ 热门短剧推荐</h3>
            <div class="results-grid">
              <el-card v-for="(item, i) in shortRecs" :key="'s'+i" class="result-mini-card" @click="enterDetail(item)">
                <div class="card-image-wrapper">
                  <img :src="getImageUrl(item.image)" class="card-image" alt="短剧海报">
                </div>
                <div class="mini-header">
                  <span class="mini-title">{{ item.title }}</span>
                  <el-tag type="success" effect="dark" size="small">短剧</el-tag>
                </div>
                <p class="mini-desc">{{ item.genre }}</p>
                <el-button type="text">进入详情分析 >></el-button>
              </el-card>
            </div>
          </div>
        </div>

        <div class="results-grid" v-if="results.length > 0">
          <el-card
            v-for="(item, i) in results"
            :key="i"
            class="result-mini-card"
            @click="enterDetail(item)"
          >
            <div class="card-image-wrapper">
              <img :src="getImageUrl(item.image)" class="card-image">
            </div>

            <div class="mini-header">
              <span class="mini-title">{{ item.title }}</span>
              <el-tag
                :type="item.type === 'movie' ? 'primary' : 'success'"
                effect="dark"
                size="small"
              >
                {{ item.type === 'movie' ? item.rating : '短剧' }}
              </el-tag>
            </div>

            <p class="summary-preview">{{ item.description }}</p>
            <div class="bottom-info">
              <span class="genre-tag">{{ item.genre }}</span>
              <el-button type="text">进入详情分析 >></el-button>
            </div>
          </el-card>
        </div>

      </div>
    </div>

    <div v-else class="detail-view">
      <div class="nav-bar">
        <el-button icon="ArrowLeft" @click="selectedItem = null">返回搜索列表</el-button>
        <span class="nav-title">
          <el-tag class="mr-10">{{ selectedItem.type === 'movie' ? '电影详情' : '短剧详情' }}</el-tag>
          {{ selectedItem.title }}
        </span>
      </div>

      <div class="detail-body">
        <el-row :gutter="30" justify="center">
          <el-col :span="20">
            <el-card class="glass-card main-info">
              <template #header><div class="card-title">📌 基本资料</div></template>
              
              <div class="detail-image-box">
                <img :src="getImageUrl(selectedItem.image)" class="detail-main-image" alt="电影/短剧海报">
              </div>

              <template v-if="selectedItem.type === 'movie'">
                <div class="info-row">
                  <b>上映时间：</b> 
                  <el-tag size="small" type="info">{{ selectedItem.Release_Date }}</el-tag>
                </div>
                <div class="info-row">
                  <b>电影时长：</b> <span>{{ selectedItem.Duration }}</span>
                </div>
                <div class="info-row">
                  <b>导演信息：</b> <span>{{ selectedItem.Director }}</span>
                </div>
              </template>

              <div class="info-row"><b>类型标签：</b> {{ selectedItem.genre }}</div>
              
              <div class="info-row">
                <b>{{ selectedItem.type === 'movie' ? '演员阵容：' : '演职人员：' }}</b> 
                {{ selectedItem.Actors || selectedItem.actors }}
              </div>

              <div class="info-row">
                <b>内容简介：</b>
                <div class="full-summary">{{ selectedItem.description }}</div>
              </div>
            </el-card>

            <el-card class="glass-card graph-box">
              <template #header>
                <div class="card-title" style="color:#67C23A">🕸️ 知识关联图谱分析</div>
              </template>
              <div class="graph-tip">💡 提示：鼠标悬停在分类球体上可显示具体姓名</div>
              <div id="main-graph" style="width: 100%; height: 500px;"></div>
            </el-card>

            <template v-if="selectedItem.type === 'movie'">
              <el-card class="glass-card">
                <template #header>
                  <div class="card-title" style="color:#409EFF">📊 影评综合分析</div>
                </template>

                <!-- 上半部分：两张饼图 -->
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div id="emotion-pie" class="chart" style="height:350px;"></div>
                  </el-col>

                  <el-col :span="12">
                    <div id="dimension-pie" class="chart" style="height:350px;"></div>
                  </el-col>
                </el-row>

                <!-- 下半部分：词云 -->
                <el-row :gutter="20" style="margin-top: 20px;">
                  <el-col :span="24">
                    <div id="keyword-cloud" class="chart cloud" style="height:450px;"></div>
                  </el-col>
                </el-row>
              </el-card>

              <el-card class="glass-card recommend-list">
                <template #header>
                  <div class="card-title" style="color:#67C23A">✨ 智能推荐</div>
                </template>

                <el-row :gutter="20">
                  <el-col
                    :span="12"
                    v-for="rec in selectedItem.recommendations"
                    :key="rec.title"
                  >
                    <el-card shadow="hover" class="rec-card">
                      <div class="rec-card-body">
                        
                        <!-- 海报 -->
                        <img
                          :src="getImageUrl(rec.image)"
                          class="rec-poster"
                          alt="推荐电影海报"
                        />

                        <!-- 右侧信息 -->
                        <div class="rec-info">
                          <div class="rec-title-row">
                            <span class="rec-name">{{ rec.title }}</span>
                            <el-tag type="success" effect="dark">
                              推荐分 {{ rec.score.toFixed(2) }}
                            </el-tag>
                          </div>

                          <!-- 标签 -->
                          <div class="rec-tags">
                            <el-tag
                              v-for="(tag, i) in rec.tags"
                              :key="i"
                              size="small"
                              type="info"
                              effect="plain"
                            >
                              {{ tag }}
                            </el-tag>
                          </div>

                          <!-- 推荐理由 -->
                          <div class="rec-reason">
                            {{ rec.reason }}
                          </div>
                        </div>

                      </div>
                    </el-card>
                  </el-col>
                </el-row>
              </el-card>
            </template>

            <template v-else>
              <el-card class="glass-card hot-analysis">
                <template #header><div class="card-title hot-color">🔥 社交媒体热点总结</div></template>
                <div class="hot-list-container">
                  <div v-for="(point, index) in splitHotPoints(selectedItem.hotPoints)" :key="index" class="hot-point-item">
                    {{ point }}
                  </div>
                </div>
              </el-card>
            </template>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';
import 'echarts-wordcloud';

// 响应式变量
const searchQuery = ref('');
const currentView = ref('movie');
const results = ref([]);
const movieRecs = ref([]);
const shortRecs = ref([]);
const selectedItem = ref(null);
const searchError = ref('');

// --- 关键修改：定义后端基准地址 ---
// 以后如果后端地址变了，只需要改这一行
const API_BASE = "https://wwty-w-movie-recommend-api.hf.space";

// 新增：图片 URL 处理函数
const getImageUrl = (path) => {
  if (!path) return ''; // 没有路径则返回空
  return `${API_BASE}${path}`;
};

// 初始化：获取后端推荐数据
onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE}/api/recommend`);
    movieRecs.value = res.data.filter(i => i.type === 'movie');
    shortRecs.value = res.data.filter(i => i.type === 'short');
  } catch (e) {
    console.error("无法加载推荐数据");
  }
});

// 搜索逻辑
const handleSearch = async () => {
  if (!searchQuery.value) {
    results.value = [];
    return;
  }
  searchError.value = '';
  try {
    const res = await axios.get(`${API_BASE}/api/search`, {
      params: { name: searchQuery.value, mode: currentView.value }
    });
    if (res.data.error) {
      searchError.value = "未找到相关内容";
      results.value = [];
    } else {
      results.value = res.data;
    }
  } catch (e) {
    searchError.value = "后端连接异常";
  }
};

// 影评分析
const enterDetail = async (item) => {
  selectedItem.value = item;
  console.log("【1. 点击进入详情】", item);

  if (item.type === 'movie') {
    console.log("movie_id:", item.movie_id);
  } else {
    console.log("非电影类型，不调用影评分析接口:", item.type);
  }


  if (item.type === 'movie' && item.movie_id) {
    try {
      // 注意：这里必须用反引号和 ${}
      const res = await axios.get(`${API_BASE}/api/movie_analysis/${item.movie_id}`);
      
      // 关键：将分析结果直接赋值给 selectedItem.value
      selectedItem.value.analysis = res.data;
      console.log("接口返回的影评分析数据", res.data);

      // 关键：等待 Vue 完成 DOM 更新（让图表容器 div 加载出来）
      await nextTick();
      
      // 此时 DOM 已经准备好，执行图表初始化
      initReviewCharts(); 
    try {
      const recRes = await axios.get(
        `${API_BASE}/api/recommend/similar`,
        {
          params: { movie: item.title }
        }
      );

      // 把推荐结果挂到 selectedItem 上
      selectedItem.value.recommendations = recRes.data.recommendations;

      console.log("【智能推荐结果】", selectedItem.value.recommendations);
    } catch (e) {
      console.warn("暂无智能推荐数据");
      selectedItem.value.recommendations = [];
    }
    } catch (e) {
      console.error("影评分析请求失败", e);
    }
  }

  // 处理知识图谱
  await nextTick();
  initEcharts();
};


const renderEmotionPie = (data) => {
  const chart = echarts.init(document.getElementById('emotion-pie'));
  chart.setOption({
    title: {
      text: '情感占比',
      left: 'center',
      top: 0,
      textStyle: { fontSize: 18, fontWeight: 'bold', color: '#303133' }
    },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '55%',
      center: ['50%', '55%'],   // 下移一点给标题留空间
      data: Object.entries(data).map(([k, v]) => ({ name: k, value: v })),
      label: { fontSize: 14, color: '#333' },
    }]
  });
};

const renderDimensionPie = (data) => {
  const chart = echarts.init(document.getElementById('dimension-pie'));
  chart.setOption({
    title: {
      text: '讨论维度占比',
      left: 'center',
      top: 0,
      textStyle: { fontSize: 18, fontWeight: 'bold', color: '#303133' }
    },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '55%',
      center: ['50%', '55%'],
      data: Object.entries(data).map(([k, v]) => ({ name: k, value: v })),
      label: { fontSize: 14, color: '#333' },
    }]
  });
};

const renderKeywordCloud = (keywords) => {
  const dom = document.getElementById('keyword-cloud');
  if (!dom || !keywords || keywords.length === 0) return;

  // 清理旧实例
  echarts.dispose(dom);
  const chart = echarts.init(dom);

  const data = keywords.slice(0, 30).map(k => ({
    name: k.word,
    value: k.weight
  }));

  chart.setOption({
    title: {
      text: '影评关键词',
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#303133'
      }
    },
    tooltip: {
      show: true
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',          // 可选：circle / cardioid / diamond / triangle
      gridSize: 8,              // 越小词越密
      sizeRange: [20, 80],      // 字体大小范围（明显！）
      rotationRange: [-30, 30], // 轻微旋转，更像真实词云
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: () => {
          // 高饱和度颜色，保证明显
          const hue = Math.floor(Math.random() * 360);
          return `hsl(${hue}, 80%, 45%)`;
        }
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data
    }]
  });
};

const initReviewCharts = () => {
  // 从 selectedItem 中安全获取 analysis
  const a = selectedItem.value?.analysis;
  
  if (!a || !a.emotion_analysis) {
    console.warn("【警告】analysis 内部数据尚不完整，跳过渲染", a);
    return;
  }

  console.log("【3. 开始渲染图表】", a);
  renderEmotionPie(a.emotion_analysis);
  renderDimensionPie(a.dimension_analysis);
  renderKeywordCloud(a.top_keywords);
};



// 知识图谱
const initEcharts = () => {
  const chartDom = document.getElementById('main-graph');
  if (!chartDom || !selectedItem.value) return;
  const chart = echarts.init(chartDom);
  
  const data = selectedItem.value;
  const movieTitle = data.title || "未知";

  const nodes = [{ name: movieTitle, symbolSize: 85, itemStyle: { color: '#409EFF' } }];
  const links = [];

  const addCategoryNodes = (sourceText, categoryName, color, size) => {
    if (!sourceText || sourceText === "null" || sourceText === "None") return;

    const cleanText = sourceText.toString().replace(/导演[:：]\s*|主演[:：]\s*|演员[:：]\s*/g, '');
    const items = cleanText.split(/[,，/ ]+/).filter(i => i.trim());
    
    if (items.length > 0) {
      const allNames = items.join(', ');
      nodes.push({ 
        name: allNames, 
        displayLabel: categoryName,
        symbolSize: size, 
        itemStyle: { color: color },
        label: { show: true, formatter: categoryName } 
      });
      links.push({ source: movieTitle, target: allNames });
    }
  };

  // 电影额外展示导演节点
  if (data.type === 'movie') {
    addCategoryNodes(data.Director || data.director, '导演', '#67C23A', 65);
  }
  
  // 共用演员与类型节点
  addCategoryNodes(data.Actors || data.actors, '演员', '#E6A23C', 60);
  addCategoryNodes(data.Genre || data.genre, '类型', '#F56C6C', 55);

  chart.setOption({
    tooltip: {
      formatter: (params) => params.data.displayLabel ? `<b>${params.data.displayLabel}</b>: ${params.data.name}` : params.data.name
    },
    series: [{
      type: 'graph',
      layout: 'force',
      data: nodes,
      links: links,
      force: { repulsion: 1500, edgeLength: 200 },
      roam: true,
      label: { show: true, position: 'inside', fontSize: 14 },
      lineStyle: { color: '#ccc', width: 2, curveness: 0.1 }
    }]
  });
};

const splitHotPoints = (text) => {
  if (!text) return [];
  return text.split(/(?=\d\.)/).map(item => item.trim()).filter(item => item);
};
</script>

// 样式
<style scoped>

.dataset-switch {
  display: flex;
  justify-content: center;
  margin-bottom: 25px;
}

.search-container, 
.detail-body > .el-row > .el-col {
  max-width: 900px;
  margin: 0 auto;
}

/* 页面整体布局优化，增加间距 */
.app-wrapper { background: #f0f2f5; min-height: 100vh; padding: 40px 20px; }
.search-container { max-width: 1100px; margin: 0 auto; text-align: center; }
.main-title { font-size: 36px; color: #303133; margin-bottom: 50px; letter-spacing: 2px; }

/* 搜索框区域 */
.search-box { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 40px; }
.mode-switch { margin-bottom: 20px; }
.big-input { max-width: 700px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

/* 推荐标题 */
.recommend-section { margin-top: 20px; }
.rec-title { text-align: left; font-size: 22px; color: #444; margin: 30px 0 20px 10px; border-left: 6px solid #409eff; padding-left: 15px; }

/* 结果网格：增加间隙 */
.results-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 50px; }
.result-mini-card { cursor: pointer; transition: 0.3s; border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.result-mini-card:hover { transform: translateY(-8px); box-shadow: 0 12px 24px rgba(64,158,255,0.2); }
.mini-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.mini-title { font-size: 18px; font-weight: bold; color: #303133; }
.mini-desc { font-size: 14px; color: #909399; height: 40px; overflow: hidden; text-align: left; line-height: 1.4; }

/* 详情页样式 */
/* 修复：内容简介显示不全的问题 */
.full-summary {
  margin-top: 10px;
  line-height: 1.8;
  color: #555;
  background: #f8f9fb;
  padding: 20px;
  border-radius: 8px;
  
  /* 必须确保没有 max-height 或 overflow: hidden */
  height: auto !important; 
  min-height: 100px;
  overflow: visible !important; 
  
  white-space: pre-wrap; /* 保留文本换行 */
  word-break: break-all; /* 防止长字母撑破布局 */
  text-align: left;
}

/* 详情页字段行间距优化 */
.info-row {
  margin-bottom: 20px;
  font-size: 15px;
  line-height: 1.6;
  color: #303133;
}
.nav-bar { background: #fff; padding: 20px 40px; display: flex; align-items: center; border-bottom: 1px solid #ebeef5; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.nav-title { font-size: 22px; font-weight: bold; margin-left: 20px; }
.detail-body { padding: 40px 0; }
.glass-card { margin-bottom: 30px; border-radius: 15px; border: none; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
.card-title { font-size: 18px; font-weight: bold; display: flex; align-items: center; }

/* 图谱 */
.graph-tip { text-align: center; color: #909399; font-size: 13px; margin-bottom: 10px; }
.info-row { margin-bottom: 15px; font-size: 15px; line-height: 1.6; color: #444; text-align: left; }

/* 模块内容样式 */
.analysis-content { line-height: 1.8; color: #555; background: #f8f9fb; padding: 25px; border-radius: 12px; white-space: pre-wrap; text-align: left; border-left: 4px solid #409eff; }
.rec-item { padding: 20px; background: #f0f9eb; border-radius: 10px; margin-bottom: 15px; border: 1px solid #e1f3d8; text-align: left; }
.rec-name { color: #409eff; font-weight: bold; font-size: 16px; }
.rec-reason { font-size: 14px; color: #666; margin-top: 8px; }
.hot-point-item { background: #fffcf5; margin-bottom: 15px; padding: 15px 20px; border-radius: 8px; border-left: 5px solid #e6a23c; color: #666; text-align: left; line-height: 1.5; }
.error-tip { color: #f56c6c; margin-top: 15px; font-weight: bold; }
/* 图片占位符样式 */
.card-image-wrapper {
  width: 100%;
  height: 180px; /* 小卡片图片高度 */
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 15px;
  background-color: #f0f2f5; /* 占位背景色 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图片比例覆盖容器 */
  transition: transform 0.3s ease;
}

.result-mini-card:hover .card-image {
  transform: scale(1.05); /* 鼠标悬停放大效果 */
}

/* 详情页大图样式 */
.detail-image-box {
  width: 100%;
  max-width: 300px; /* 详情页图片最大宽度 */
  height: auto;
  margin: 0 0 30px 0; /* 居中显示并与下方内容隔开 */
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.card-image-wrapper {
  width: 100%;
  height: 180px; 
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 15px;
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}


.detail-main-image {
  width: 100%;
  height: auto;
  display: block; /* 移除图片底部空白 */
}

.chart {
  width: 100%;
  height: 300px;
}
.cloud {
  height: 350px;
}

/* 智能推荐卡片 */
.rec-card {
  border-radius: 12px;
}

.rec-card-body {
  display: flex;
  gap: 15px;
}

.rec-poster {
  width: 90px;
  height: 130px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.rec-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.rec-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.rec-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.rec-tags {
  margin-bottom: 8px;
}

.rec-tags .el-tag {
  margin-right: 6px;
  margin-bottom: 4px;
}

.rec-reason {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  text-align: left;
}


</style>