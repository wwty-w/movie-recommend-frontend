<template>
  <div class="app-wrapper">
    <div v-if="!selectedItem" class="search-view">
      <div class="search-container">
        <h1 class="main-title">影视大数据检索系统</h1>

        <div class="dataset-switch">
          <el-radio-group v-model="currentView" size="large">
            <el-radio-button label="movie">电影</el-radio-button>
            <el-radio-button label="short">短剧</el-radio-button>
          </el-radio-group>
        </div>

        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="请输入名称..."
            @keyup.enter="handleSearch"
            class="big-input"
            style="width: 100%;"
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
              <el-tag v-if="item.has_knowledge_graph" type="info" effect="plain" size="mini" style="margin-left: 5px;">
                知识图谱
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
          <el-tag v-if="selectedItem.has_knowledge_graph" type="success" size="small" style="margin-left: 10px;">
            知识图谱已加载
          </el-tag>
        </span>
      </div>

      <div class="detail-body grid-layout">
        <div class="top-row">
          <el-card class="glass-card main-info">
            <template #header><div class="card-title">📌 基本资料</div></template>
            <div class="basic-info-content">
              <div class="image-and-info">
                <div class="detail-image-box" style="width: 280px; height: 400px;">
                  <img :src="getImageUrl(selectedItem.image)" class="detail-main-image" alt="海报">
                </div>
                <div class="quick-info">
                  <template v-if="selectedItem.type === 'movie'">
                    <div class="info-item">
                      <span class="info-label">上映时间：</span>
                      <span class="info-value">{{ selectedItem.Release_Date || '未知' }}</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">电影时长：</span>
                      <span class="info-value">{{ selectedItem.Duration || '未知' }}分钟</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">导演：</span>
                      <span class="info-value">{{ selectedItem.Director || '未知' }}</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">评分：</span>
                      <span class="info-value">{{ selectedItem.rating || '未知' }}</span>
                    </div>
                  </template>
                  
                  <div class="info-item">
                    <span class="info-label">类型标签：</span>
                    <div class="info-value">
                      <el-tag
                        v-for="(genre, idx) in (selectedItem.knowledgeGraph?.movie_info?.data?.genres || [])"
                        :key="idx"
                        size="small"
                        type="info"
                        style="margin-right: 5px; margin-bottom: 5px;"
                      >
                        {{ genre }}
                      </el-tag>
                      <span v-if="!selectedItem.knowledgeGraph || !selectedItem.knowledgeGraph.movie_info?.data?.genres">
                        {{ selectedItem.genre || '未知' }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="info-item">
                    <span class="info-label">{{ selectedItem.type === 'movie' ? '演员阵容：' : '演职人员：' }}</span>
                    <span class="info-value actors">
                      <template v-if="selectedItem.knowledgeGraph?.movie_info?.data?.actors">
                        <span v-for="(actor, idx) in selectedItem.knowledgeGraph.movie_info.data.actors" :key="idx">
                          {{ actor }}{{ idx < selectedItem.knowledgeGraph.movie_info.data.actors.length - 1 ? '、' : '' }}
                        </span>
                      </template>
                      <template v-else>
                        {{ selectedItem.Actors || selectedItem.actors || '未知' }}
                      </template>
                    </span>
                  </div>

                  <!-- 短剧简介放在这里 -->
                  <div v-if="selectedItem.type === 'short'" class="info-item">
                    <span class="info-label">内容简介：</span>
                    <div class="short-description">
                      {{ selectedItem.description && selectedItem.description !== '暂无简介' 
                        ? selectedItem.description 
                        : (selectedItem.knowledgeGraph?.movie_info?.data?.overview || '暂无简介') }}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 电影的内容简介保持在下方 -->
              <div v-if="selectedItem.type === 'movie'" class="description-section">
                <h4>内容简介：</h4>
                <div class="full-summary">
                  {{ selectedItem.description && selectedItem.description !== '暂无简介' 
                    ? selectedItem.description 
                    : (selectedItem.knowledgeGraph?.movie_info?.data?.overview || '暂无简介') }}
                </div>
              </div>
            </div>
          </el-card>

          <el-card class="glass-card recommend-list">
            <template #header>
              <div class="card-title" :style="{ color: selectedItem.type === 'movie' ? '#67C23A' : '#F56C6C' }">
                {{ selectedItem.type === 'movie' ? '✨ 智能推荐' : '🔥 热点评析' }}
              </div>
            </template>

            <div v-if="selectedItem.type === 'movie'" class="vertical-rec-list">
              <div v-for="rec in selectedItem.recommendations" :key="rec.title" class="vertical-rec-item" >
                <div class="vertical-rec-content">
                  <img :src="getImageUrl(rec.image)" class="vertical-rec-poster" alt="推荐海报">
                  <div class="vertical-rec-info">
                    <div class="vertical-rec-title">
                      <span class="rec-name">{{ rec.title }}</span>
                      <el-tag type="success" size="small" effect="dark">{{ rec.score?.toFixed(2) || '0.00' }}</el-tag>
                    </div>
                    <div class="vertical-rec-tags">
                      <el-tag v-for="(tag, i) in rec.tags || []" :key="i" size="mini" type="info" effect="plain">{{ tag }}</el-tag>
                    </div>
                    <p class="vertical-rec-reason">{{ rec.reason || '暂无推荐理由' }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="hot-list-container side-bar-hot">
              <div v-for="(point, index) in splitHotPoints(selectedItem.hotPoints)" :key="index" class="hot-point-item">
                <div class="hot-point-badge">热点 {{ index + 1 }}</div>
                <p class="hot-point-content">{{ point }}</p>
              </div>
            </div>
          </el-card>
        </div>

        <div class="center-row" v-if="selectedItem.type === 'movie'">
          <el-card class="glass-card emotion-chart">
            <template #header><div class="card-title" style="color:#409EFF">📊 情感分析</div></template>
            <div id="emotion-pie"></div>
          </el-card>
          <el-card class="glass-card dimension-chart">
            <template #header><div class="card-title" style="color:#E6A23C">📈 讨论维度</div></template>
            <div id="dimension-pie"></div>
          </el-card>
        </div>

        <div class="bottom-row" :style="selectedItem.type === 'short' ? 'display: block;' : ''">
          <el-card v-if="selectedItem.type === 'movie'" class="glass-card keyword-chart">
            <template #header><div class="card-title" style="color:#F56C6C; text-align: center;">☁️ 关键词云</div></template>
            <div id="keyword-cloud"></div>
          </el-card>

          <el-card class="glass-card graph-box" :style="selectedItem.type === 'short' ? 'width: 100%; margin-bottom: 20px;' : ''">
            <template #header><div class="card-title" style="color:#67C23A">🕸️ 知识关联图谱</div></template>
            <div class="graph-tip">💡 鼠标悬停查看详情，滚轮缩放，拖拽移动</div>
            <div id="main-graph"></div>
          </el-card>
        </div>

        <div class="comment-row" v-if="selectedItem.comments && selectedItem.comments.length > 0">
          <el-card class="glass-card comment-card" style="width: 100%;">
            <template #header>
              <div class="card-title" style="color:#67C23A">
                💬 {{ selectedItem.type === 'movie' ? '精选影评' : '精彩评论' }} ({{ selectedItem.comments.length }})
              </div>
            </template>
            <div class="comment-scroll-container">
              <div v-for="(comment, index) in selectedItem.comments" :key="index" class="comment-item">
                <p class="comment-text">{{ comment.text }}</p>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
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

const BASE_URL = 'https://wwty-w-movie-recommend-api.hf.space';

// 获取图片URL
const getImageUrl = (path) => {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  // 确保拼接路径正确
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${BASE_URL}${cleanPath}`;
};

// 初始化推荐数据
onMounted(async () => {
  try {
    const res = await axios.get(`${BASE_URL}/api/recommend`);
    movieRecs.value = res.data.filter(i => i.type === 'movie');
    shortRecs.value = res.data.filter(i => i.type === 'short');
  } catch (e) {
    console.error("无法加载推荐数据");
    movieRecs.value = [
      { title: '测试电影1', type: 'movie', rating: '8.5', genre: '动作', image: '/images/test1.jpg' },
      { title: '测试电影2', type: 'movie', rating: '9.0', genre: '剧情', image: '/images/test2.jpg' }
    ];
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
    const res = await axios.get(`${BASE_URL}/api/search`, {
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
    results.value = [
      { 
        title: '测试电影结果', 
        type: 'movie', 
        rating: '8.5', 
        genre: '动作/冒险',
        description: '这是一部测试电影的描述',
        image: '/images/test.jpg',
        movie_id: 'test123'
      }
    ];
  }
};

// 进入详情页
const enterDetail = async (item) => {
  selectedItem.value = item;

  // 获取知识图谱数据
  try {
    const kgRes = await axios.get(`${BASE_URL}/api/knowledge_graph/${item.title}`);
    selectedItem.value.knowledgeGraph = kgRes.data;
    console.log('知识图谱数据加载成功:', selectedItem.value.knowledgeGraph);
  } catch (e) {
    console.log("知识图谱数据获取失败:", e);
    selectedItem.value.knowledgeGraph = null;
  }

  // 如果当前项没有影评（比如从相似推荐点进来的），则去后台抓取
  if (!item.comments && item.movie_id) {
    try {
      const res = await axios.get(`${BASE_URL}/api/movie_comments/${item.movie_id}`);
      selectedItem.value.comments = res.data.comments;
    } catch (e) {
      console.log("该电影暂无影评");
    }
  }

  if (item.type === 'movie') {
    try {
      if (item.movie_id) {
        const res = await axios.get(`${BASE_URL}/api/movie_analysis/${item.movie_id}`);
        selectedItem.value.analysis = res.data;
      }
      
      try {
        const recRes = await axios.get(`${BASE_URL}/api/recommend/similar`, {
          params: { movie: item.title }
        });
        selectedItem.value.recommendations = recRes.data.recommendations || [];
      } catch (e) {
        selectedItem.value.recommendations = [];
      }
      
      await nextTick();
      initReviewCharts();
      initEcharts();
    } catch (e) {
      selectedItem.value.analysis = {
        emotion_analysis: { "喜爱": 35, "感动": 25, "震撼": 20, "失望": 15, "无感": 5 },
        dimension_analysis: { "剧情": 40, "演技": 25, "特效": 20, "音乐": 10, "导演": 5 },
        top_keywords: [
          { word: "特效震撼", weight: 95 },
          { word: "剧情紧凑", weight: 88 },
          { word: "演技在线", weight: 82 },
          { word: "音乐感人", weight: 75 },
          { word: "导演功力", weight: 70 }
        ]
      };
      selectedItem.value.recommendations = [
        {
          title: "相关推荐1",
          score: 8.7,
          tags: ["动作", "冒险"],
          reason: "基于您的观影偏好推荐",
          image: "/images/rec1.jpg"
        },
        {
          title: "相关推荐2",
          score: 8.5,
          tags: ["科幻", "剧情"],
          reason: "相似题材高分作品",
          image: "/images/rec2.jpg"
        }
      ];
      await nextTick();
      initReviewCharts();
      initEcharts();
    }
  } else {
    selectedItem.value.recommendations = [];
    await nextTick();
    initEcharts();
  }
};

// 监听知识图谱数据变化
watch(() => selectedItem.value?.knowledgeGraph, (newVal) => {
  if (newVal) {
    nextTick(() => {
      initEcharts();
    });
  }
}, { immediate: false });

const initEcharts = () => {
  const chartDom = document.getElementById('main-graph');
  if (!chartDom || !selectedItem.value) return;
  
  echarts.dispose(chartDom);
  const chart = echarts.init(chartDom);
  
  const kgData = selectedItem.value.knowledgeGraph;
  
  // 1. 初始化容器
  let finalNodes = [];
  let finalLinks = [];
  let finalCategories = [];
  let categoryNames = [];

  // 2. 解析数据逻辑
  if (kgData && kgData.graph) {
    // 提取数据
    const { nodes, links } = kgData.graph;
    finalCategories = kgData.categories || [];
    categoryNames = finalCategories.map(c => c.name);

    // 处理节点 (赋给 finalNodes)
    finalNodes = nodes.map(node => ({
      ...node,
      name: node.id, // ECharts 显示标签必须有 name
      category: node.category,
      symbolSize: node.symbolSize || 30,
      draggable: true
    }));

    // 处理连线 (赋给 finalLinks)
    finalLinks = links.map(link => ({
      source: link.source,
      target: link.target,
      label: {
        show: true,
        formatter: link.label || '',
        fontSize: 10
      },
      lineStyle: { curveness: 0.1 }
    }));

  } else {
    // 兜底方案
    const data = selectedItem.value;
    finalCategories = [{ name: '核心' }, { name: '属性' }];
    categoryNames = ['核心', '属性'];
    
    finalNodes = [{ id: 'root', name: data.title, symbolSize: 50, category: 0 }];
    
    if (data.Director) {
      finalNodes.push({ id: 'dir', name: data.Director, symbolSize: 35, category: 1 });
      finalLinks.push({ 
        source: 'root', 
        target: 'dir', 
        label: { show: true, formatter: '导演' } 
      });
    }
  }

  // 3. 配置图表参数 (使用 final 前缀的变量)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.dataType === 'node') {
          return `<b>${params.data.id}</b><br/>类型: ${params.data.category || '未知'}`;
        }
        return `${params.data.source} → ${params.data.label?.formatter || ''} → ${params.data.target}`;
      }
    },
    legend: [{
      data: categoryNames,
      orient: 'horizontal',
      bottom: 0
    }],
    series: [{
      type: 'graph',
      layout: 'force',
      data: finalNodes,
      links: finalLinks,
      categories: finalCategories,
      roam: true,
      label: {
        show: true,
        position: 'right',
        formatter: '{b}' 
      },
      force: {
        repulsion: 600, // 增加斥力让节点散开
        edgeLength: 120,
        gravity: 0.1
      },
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: 8,
      lineStyle: {
        color: 'source',
        opacity: 0.6,
        width: 1.5
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 3 }
      }
    }]
  };
    
  chart.setOption(option);

  // 4. 响应式
  window.addEventListener('resize', () => chart.resize());
};

// 保留原有的饼图和词云图函数（保持不变）
const renderEmotionPie = (data) => {
  const chartDom = document.getElementById('emotion-pie');
  if (!chartDom) return;
  
  echarts.dispose(chartDom);
  const chart = echarts.init(chartDom);
  
  const emotionColorMap = {
    '喜爱': '#F7B2C7',
    '感动': '#C9D4F7',
    '震撼': '#B8E5FA',
    '怀旧': '#ffcd87',
    '失望': '#6e6280',
    '愤怒': '#F56C6C',
    '无感': '#CBE4B1'
  };
  
  const chartData = Object.entries(data).map(([name, value], index) => ({
    name,
    value,
    itemStyle: {
      color: emotionColorMap[name] || 
        ['#C9D4F7', '#F7B2C7', '#6e6280', '#ffcd87', '#FFFAA0', '#CBE4B1', '#B3DDCB', '#B8E5FA'][index % 8]
    }
  }));
  
  chart.setOption({
    title: {
      text: '情感占比',
      left: 'center',
      top: '0%',
      textStyle: { fontSize: 16, fontWeight: 'bold', color: '#666' }
    },
    tooltip: { trigger: 'item', formatter: '{a}<br/>{b}: {d}%' },
    legend: {
      orient: 'horizontal',
      bottom: '2%',
      textStyle: { color: '#666', fontSize: 12 }
    },
    series: [{
      name: '情感占比',
      type: 'pie',
      radius: ['45%', '65%'],
      center: ['50%', '50%'],
      data: chartData,
      label: { 
        fontSize: 13, 
        color: '#555', 
        formatter: '{b}',
        position: 'outside'
      },
      labelLine: { 
        length: 15,
        length2: 10
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        }
      }
    }],
    grid: {
      top: '25%',
      bottom: '20%',
      left: '10%',
      right: '10%'
    }
  });
};

const renderDimensionPie = (data) => {
  const chartDom = document.getElementById('dimension-pie');
  if (!chartDom) return;
  
  echarts.dispose(chartDom);
  const chart = echarts.init(chartDom);
  
  const dimensionColorMap = {
    '剧情': '#C9D4F7',
    '演技': '#B8E5FA',
    '视觉': '#FFFAA0',
    '听觉': '#CBE4B1',
    '主题': '#ffcd87',
    '台词': '#B3DDCB',
    '导演': '#F7B2C7'
  };
  
  const chartData = Object.entries(data).map(([name, value], index) => ({
    name,
    value,
    itemStyle: {
      color: dimensionColorMap[name] || 
        ['#C9D4F7', '#F7B2C7', '#f4cec7', '#ffcd87', '#FFFAA0', '#CBE4B1', '#B3DDCB', '#B8E5FA'][index % 8]
    }
  }));
  
  chart.setOption({
    title: {
      text: '讨论维度占比',
      left: 'center',
      top: '0%',
      textStyle: { fontSize: 16, fontWeight: 'bold', color: '#666' }
    },
    tooltip: { trigger: 'item', formatter: '{a}<br/>{b}: {d}%' },
    legend: {
      orient: 'horizontal',
      bottom: '2%',
      textStyle: { color: '#666', fontSize: 12 }
    },
    series: [{
      name: '讨论维度',
      type: 'pie',
      radius: ['45%', '65%'],
      center: ['50%', '50%'],
      data: chartData,
      label: { 
        fontSize: 13, 
        color: '#555', 
        formatter: '{b}',
        position: 'outside'
      },
      labelLine: { 
        length: 15,
        length2: 10
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        }
      }
    }],
    grid: {
      top: '25%',
      bottom: '20%',
      left: '10%',
      right: '10%'
    }
  });
};

const renderKeywordCloud = (keywords) => {
  const chartDom = document.getElementById('keyword-cloud');
  if (!chartDom || !keywords || keywords.length === 0) return;
  
  echarts.dispose(chartDom);
  const chart = echarts.init(chartDom);

  const data = keywords.slice(0, 30).map(k => ({
    name: k.word,
    value: k.weight
  }));

  const colorPalette = ['#C9D4F7', '#F7B2C7', '#f4cec7', '#EEC78A', '#FFFAA0', '#CBE4B1', '#B3DDCB', '#B8E5FA'];

  chart.setOption({
    title: {
      text: '影评关键词',
      left: 'center',
      top: 20,
      textStyle: { fontSize: 18, fontWeight: 'bold', color: '#666' }
    },
    tooltip: {
      show: true,
      formatter: function (params) {
        return `<strong>${params.name}</strong><br/>权重: ${params.value}`;
      }
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      gridSize: 15,
      sizeRange: [20, 80],
      rotationRange: [-30, 30],
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'Microsoft YaHei, Arial, sans-serif',
        fontWeight: 'bold'
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      data: data.map((word, index) => ({
        name: word.name,
        value: word.value,
        textStyle: {
          color: colorPalette[index % colorPalette.length]
        }
      }))
    }],
    grid: {
      top: '15%',
      bottom: '10%',
      left: '5%',
      right: '5%'
    }
  });
};

const initReviewCharts = () => {
  const a = selectedItem.value?.analysis;
  if (!a || !a.emotion_analysis) return;

  setTimeout(() => {
    renderEmotionPie(a.emotion_analysis);
    renderDimensionPie(a.dimension_analysis);
    renderKeywordCloud(a.top_keywords);
  }, 100);
};

// 分割热点文本
const splitHotPoints = (text) => {
  if (!text) return [];
  return text.split(/(?=\d\.)/).map(item => item.trim()).filter(item => item);
};
</script>

<style scoped>
/* 样式部分保持完全不变，使用原来的样式 */
.app-wrapper {
  min-height: 100vh;
  background: #f0f2f5;
  padding: 20px;
}

.grid-layout {
  display: flex;
  flex-direction: column;
  gap: 25px;
  padding: 25px;
  max-width: 1800px;
  margin: 0 auto;
}

/* 修改第一行：两个卡片各占一半 */
.top-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  min-height: 600px;
  height: auto;
}

/* 调整基本资料卡片宽度 */
.main-info {
  height: 100%;
}

.graph-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: visible !important;
}

.graph-box :deep(.el-card__header) {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.graph-subtitle {
  font-size: 12px;
  color: #909399;
  font-weight: normal;
}

.graph-tip {
  text-align: center;
  color: #909399;
  font-size: 13px;
  margin-bottom: 10px;
  padding: 5px;
  background: #f8f9fa;
  border-radius: 4px;
}

/* 知识图谱容器加大 */
#main-graph {
  flex: 1;
  width: 100%;
  min-height: 400px;
  margin: 0;
  padding: 0;
  overflow: visible !important;
}

.glass-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  overflow: visible !important;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.main-info :deep(.el-card__body) {
  padding: 25px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: visible;
}

.basic-info-content {
  flex: 1.2;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.image-and-info {
  display: flex;
  gap: 25px;
  margin-bottom: 25px;
  min-height: 220px;
}

.detail-image-box {
  flex-shrink: 0;
  width: 280px;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.detail-main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.quick-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-width: 0;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-label {
  font-weight: bold;
  color: #606266;
  font-size: 16px;
}

.info-value {
  color: #303133;
  font-size: 17px;
  line-height: 1.5;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px;
}

.info-value.actors {
  max-height: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.description-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 200px;
}

.description-section h4 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 16px;
}

.full-summary {
  flex: 1;
  background: #f8f9fb;
  padding: 20px;
  border-radius: 8px;
  line-height: 1.8;
  color: #555;
  overflow-y: visible !important;
  height: auto !important;
  max-height: none !important;
  font-size: 14.5px;
  text-align: justify;
  white-space: pre-wrap;
  word-break: break-all;
}

.recommend-list :deep(.el-card__body) {
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.vertical-rec-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 5px;
}

.vertical-rec-item {
  background: #f8f9fb;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  border-left: 3px solid #409eff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.vertical-rec-item:hover {
  background: #f0f7ff;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(64,158,255,0.1);
}

.vertical-rec-content {
  display: flex;
  gap: 12px;
}

.vertical-rec-poster {
  width: 60px;
  height: 85px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
}

.vertical-rec-info {
  flex: 1;
  min-width: 0;
}

.vertical-rec-title {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.rec-name {
  font-weight: bold;
  font-size: 14px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  margin-right: 8px;
}

.vertical-rec-tags {
  margin-bottom: 5px;
}

.vertical-rec-tags .el-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}

.vertical-rec-reason {
  font-size: 12px;
  color: #606266;
  line-height: 1.4;
  overflow: visible;
  white-space: normal;
  word-break: break-word;
}

.no-rec {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 第二行：情感分析和讨论维度（保持不变） */
.center-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  height: 450px;
}

.center-row.full-width {
  grid-template-columns: 1fr;
}

.emotion-chart,
.dimension-chart {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.emotion-chart :deep(.el-card__body),
.dimension-chart :deep(.el-card__body) {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: visible;
}

#emotion-pie,
#dimension-pie {
  flex: 1;
  width: 100%;
}

/* 第三行：词云图和知识图谱（知识图谱更宽） */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1.8fr;
  gap: 25px;
  height: 700px;
  min-height: 700px;
}

.keyword-chart,
.graph-box {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.keyword-chart :deep(.el-card__body),
.graph-box :deep(.el-card__body) {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: visible !important;
}

#keyword-cloud,
#main-graph {
  flex: 1;
  width: 100%;
  min-height: 500px;
}

.hot-analysis {
  height: 100%;
}

.hot-analysis :deep(.el-card__body) {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.hot-list-container {
  flex: 1;
  overflow-y: auto;
}

.hot-point-item {
  background: #fffcf5;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  border-left: 5px solid #e6a23c;
  line-height: 1.6;
  transition: all 0.3s ease;
}

.hot-point-item:hover {
  background: #fff8e1;
  transform: translateX(5px);
}

.no-hot-points {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.nav-bar {
  background: #fff;
  padding: 15px 30px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ebeef5;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.nav-title {
  font-size: 20px;
  font-weight: bold;
  margin-left: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.mr-10 {
  margin-right: 10px;
}

.comment-row {
  width: 100%;
  margin-bottom: 25px;
}

.comment-card {
  height: 400px;
}

.comment-scroll-container {
  height: 320px;
  overflow-y: auto;
  padding-right: 10px;
}

.comment-item {
  background: #f8f9fb;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #edf2f7;
  transition: all 0.3s ease;
}

.comment-item:hover {
  background: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-color: #67C23A;
}

.comment-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.comment-text {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  text-align: justify;
  margin: 0;
}

/* 新增的短剧简介样式 */
.short-description {
  background: #f8f9fb;
  padding: 15px;
  border-radius: 8px;
  line-height: 1.6;
  color: #555;
  font-size: 14px;
  text-align: justify;
  white-space: pre-wrap;
  word-break: break-word;
  margin-top: 5px;
  max-height: 150px;
  overflow-y: auto;
}

/* 调整短剧页面的基本资料卡片高度 */
.detail-view .top-row .main-info {
  height: auto;
  min-height: 500px;
}

@media (max-width: 1400px) {
  .grid-layout {
    max-width: 1400px;
  }
  
  .top-row {
    height: 600px;
    min-height: 600px;
  }
  
  .center-row {
    height: 400px;
  }
  
  .bottom-row {
    height: 600px;
    min-height: 600px;
  }
}

@media (max-width: 1200px) {
  .top-row {
    grid-template-columns: 1fr;
    height: auto;
    min-height: auto;
  }
  
  .main-info,
  .recommend-list {
    height: 500px;
  }
  
  .center-row {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .emotion-chart,
  .dimension-chart {
    height: 400px;
  }
  
  .bottom-row {
    grid-template-columns: 1fr;
    height: auto;
    min-height: auto;
  }
  
  .keyword-chart,
  .graph-box {
    height: 450px;
  }
  
  /* 响应式调整短剧简介 */
  .detail-view .top-row .main-info {
    height: auto;
    min-height: 450px;
  }
  
  .short-description {
    max-height: 120px;
  }
}

@media (max-width: 768px) {
  .grid-layout {
    padding: 15px;
    gap: 20px;
  }
  
  .top-row {
    gap: 15px;
  }
  
  .main-info,
  .recommend-list {
    height: 450px;
  }
  
  .image-and-info {
    flex-direction: column;
  }
  
  .detail-image-box {
    width: 100%;
    height: 200px;
    align-self: center;
  }
  
  .center-row {
    gap: 15px;
  }
  
  .emotion-chart,
  .dimension-chart {
    height: 350px;
  }
  
  .bottom-row {
    gap: 15px;
  }
  
  .keyword-chart,
  .graph-box {
    height: 400px;
  }
  
  /* 响应式调整短剧简介 */
  .short-description {
    max-height: 100px;
    padding: 12px;
    font-size: 13px;
  }
  
  .detail-view .top-row .main-info {
    min-height: 400px;
  }
}

.search-container {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.main-title {
  font-size: 36px;
  color: #303133;
  margin-bottom: 40px;
  letter-spacing: 2px;
}

.dataset-switch {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.search-box {
  background: white;
  padding: 20px;
  border-radius: 18px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
  margin-bottom: 40px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.big-input {
  max-width: 1000px;
  margin: 0 auto;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
  margin-bottom: 40px;
}

.result-mini-card {
  cursor: pointer;
  transition: 0.3s;
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.result-mini-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(64,158,255,0.2);
}

.card-image-wrapper {
  width: 100%;
  height: 360px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 15px;
  background-color: #f0f2f5;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mini-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.mini-title {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
  flex: 1;
  margin-right: 10px;
}

.mini-desc {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
}

.summary-preview {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  word-break: break-all;
}

.bottom-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.genre-tag {
  background: #f0f2f5;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;
}

.error-tip {
  color: #f56c6c;
  margin-top: 10px;
  font-size: 14px;
}

.rec-title {
  font-size: 24px;
  color: #303133;
  margin-bottom: 20px;
  text-align: center;
}

.comment-scroll-container::-webkit-scrollbar {
  width: 6px;
}
.comment-scroll-container::-webkit-scrollbar-thumb {
  background-color: #e2e8f0;
  border-radius: 10px;
}

.vertical-rec-list::-webkit-scrollbar {
  width: 6px;
}
.vertical-rec-list::-webkit-scrollbar-thumb {
  background-color: #e2e8f0;
  border-radius: 10px;
}
</style>
