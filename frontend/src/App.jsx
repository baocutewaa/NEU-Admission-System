import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Users, UserCheck, GraduationCap, Calendar, TrendingUp, AlertCircle } from 'lucide-react';
import { 
    fetchOverview, fetchRegions, fetchMajors, 
    fetchMethods, fetchMotivation, fetchClustering, fetchPreferenceMultivariate,
    fetchGenderDistribution, fetchGeographicEnrollment, fetchScoreAnalytics
} from './services/api';
import GenderAnalyticsChart from './components/GenderAnalyticsChart';
import GeoHeatmapChart from './components/GeoHeatmapChart';
import ScoreBoxplotChart from './components/ScoreBoxplotChart';

const App = () => {
    const [year, setYear] = useState(2024);
    const [methodFilter, setMethodFilter] = useState('');
    const [majorFilter, setMajorFilter] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [data, setData] = useState({
        overview: null,
        regions: [],
        majors: [],
        methods: [],
        motivation: null,
        clustering: [],
        multivariate: [],
        gender: [],
        geo: [],
        scores: []
    });

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            setError(null);
            try {
                const [
                    overviewRes, regionsRes, majorsRes, 
                    methodsRes, motivationRes, clusteringRes, multivariateRes,
                    genderRes, geoRes, scoreRes
                ] = await Promise.all([
                    fetchOverview(year),
                    fetchRegions(year),
                    fetchMajors(year),
                    fetchMethods(year),
                    fetchMotivation(year),
                    fetchClustering(year, 15),
                    fetchPreferenceMultivariate(year),
                    fetchGenderDistribution(year, methodFilter || null),
                    fetchGeographicEnrollment(year, methodFilter || null, majorFilter || null),
                    fetchScoreAnalytics(year, methodFilter || null, majorFilter || null)
                ]);

                setData({
                    overview: overviewRes,
                    regions: regionsRes,
                    majors: majorsRes,
                    methods: methodsRes,
                    motivation: motivationRes,
                    clustering: clusteringRes,
                    multivariate: multivariateRes,
                    gender: genderRes,
                    geo: geoRes,
                    scores: scoreRes
                });
            } catch (err) {
                console.error("Error fetching data:", err);
                setError("Failed to load dashboard data. Please make sure the backend is running.");
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [year, methodFilter, majorFilter]);

    // Common ECharts Theme settings to match our Dark Glassmorphism UI
    const chartTheme = {
        textStyle: { fontFamily: 'Inter, sans-serif', color: '#94a3b8' },
        tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            textStyle: { color: '#f8fafc' },
            backdropFilter: 'blur(4px)'
        },
        legend: { textStyle: { color: '#94a3b8' } }
    };

    const getFunnelOption = () => {
        if (!data.overview) return {};
        return {
            ...chartTheme,
            tooltip: { trigger: 'item', formatter: "{a} <br/>{b} : {c} ({d}%)" },
            series: [
                {
                    name: 'Tuyển sinh',
                    type: 'funnel',
                    left: '10%', top: 20, bottom: 20, width: '80%',
                    min: 0, max: data.overview.total_applicants,
                    minSize: '0%', maxSize: '100%',
                    sort: 'descending',
                    gap: 2,
                    label: { show: true, position: 'inside', formatter: '{b}: {c}', color: '#fff', fontSize: 14 },
                    labelLine: { length: 10, lineStyle: { width: 1, type: 'solid' } },
                    itemStyle: { borderColor: '#fff', borderWidth: 0 },
                    data: [
                        { value: data.overview.total_applicants, name: 'Tổng ứng viên', itemStyle: { color: '#3b82f6' } },
                        { value: data.overview.admitted_applicants, name: 'Trúng tuyển', itemStyle: { color: '#10b981' } },
                        { value: data.overview.enrolled_applicants, name: 'Nhập học', itemStyle: { color: '#8b5cf6' } }
                    ]
                }
            ]
        };
    };

    const getMajorsBarOption = () => {
        if (!data.majors.length) return {};
        // Sort by total applicants
        const sorted = [...data.majors].sort((a, b) => b.total_applicants - a.total_applicants).slice(0, 15);
        
        return {
            ...chartTheme,
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            legend: { data: ['Đăng ký', 'Trúng tuyển', 'Nhập học'], top: 0, textStyle: { color: '#94a3b8' } },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
            yAxis: { type: 'category', data: sorted.map(m => m.major_name).reverse(), axisLabel: { width: 150, overflow: 'truncate' } },
            series: [
                { name: 'Đăng ký', type: 'bar', stack: 'total', label: { show: false }, emphasis: { focus: 'series' }, data: sorted.map(m => m.total_applicants).reverse(), itemStyle: { color: '#3b82f6' } },
                { name: 'Trúng tuyển', type: 'bar', stack: 'total', label: { show: false }, emphasis: { focus: 'series' }, data: sorted.map(m => m.admitted_applicants).reverse(), itemStyle: { color: '#10b981' } },
                { name: 'Nhập học', type: 'bar', stack: 'total', label: { show: false }, emphasis: { focus: 'series' }, data: sorted.map(m => m.enrolled_applicants).reverse(), itemStyle: { color: '#8b5cf6' } }
            ]
        };
    };

    const getMethodsDonutOption = () => {
        if (!data.methods.length) return {};
        return {
            ...chartTheme,
            tooltip: { trigger: 'item' },
            legend: { orient: 'vertical', left: 'left', textStyle: { color: '#94a3b8' } },
            series: [
                {
                    name: 'Phương thức',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    itemStyle: { borderRadius: 10, borderColor: '#1e293b', borderWidth: 2 },
                    label: { show: false, position: 'center' },
                    emphasis: { label: { show: true, fontSize: 18, fontWeight: 'bold', color: '#fff' } },
                    labelLine: { show: false },
                    data: data.methods.map(m => ({ value: m.total_applicants, name: m.method_name }))
                }
            ]
        };
    };

    const getRegionsBarOption = () => {
        if (!data.regions.length) return {};
        const sorted = [...data.regions].sort((a, b) => b.total_applicants - a.total_applicants).slice(0, 10);
        return {
            ...chartTheme,
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: { type: 'category', data: sorted.map(r => r.region), axisLabel: { interval: 0, rotate: 30 } },
            yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
            series: [
                {
                    name: 'Ứng viên',
                    type: 'bar',
                    barWidth: '50%',
                    itemStyle: {
                        color: {
                            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
                            colorStops: [{ offset: 0, color: '#60a5fa' }, { offset: 1, color: '#3b82f6' }]
                        },
                        borderRadius: [4, 4, 0, 0]
                    },
                    data: sorted.map(r => r.total_applicants)
                }
            ]
        };
    };

    const getMotivationOption = () => {
        if (!data.motivation) return {};
        return {
            ...chartTheme,
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            legend: { data: ['Ứng viên', 'Trúng tuyển'], textStyle: { color: '#94a3b8' } },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: { type: 'category', data: ['Động lực cao (NV1-3)', 'Dự phòng (NV>3)'] },
            yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
            series: [
                {
                    name: 'Ứng viên',
                    type: 'bar',
                    data: [data.motivation.high_motivation.applicants, data.motivation.low_motivation.applicants],
                    itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] }
                },
                {
                    name: 'Trúng tuyển',
                    type: 'bar',
                    data: [data.motivation.high_motivation.admitted, data.motivation.low_motivation.admitted],
                    itemStyle: { color: '#10b981', borderRadius: [4, 4, 0, 0] }
                }
            ]
        };
    };

    const getClusteringGraphOption = () => {
        if (!data.clustering.length) return {};
        
        const nodesMap = new Map();
        const links = [];
        
        data.clustering.forEach(c => {
            const { nganh_1, nganh_2, frequency } = c;
            nodesMap.set(nganh_1, (nodesMap.get(nganh_1) || 0) + frequency);
            nodesMap.set(nganh_2, (nodesMap.get(nganh_2) || 0) + frequency);
            links.push({ source: nganh_1, target: nganh_2, value: frequency });
        });

        const nodes = Array.from(nodesMap.keys()).map(name => ({
            name,
            value: nodesMap.get(name),
            symbolSize: Math.max(10, Math.min(50, nodesMap.get(name) / 10)),
            itemStyle: { color: '#8b5cf6' }
        }));

        return {
            ...chartTheme,
            tooltip: { formatter: '{b}' },
            series: [{
                type: 'graph',
                layout: 'force',
                roam: true,
                label: { show: true, position: 'right', formatter: '{b}', color: '#cbd5e1' },
                force: { repulsion: 200, edgeLength: 100 },
                data: nodes,
                links: links.map(l => ({ ...l, lineStyle: { width: Math.max(1, l.value / 20), color: 'rgba(255,255,255,0.2)' } }))
            }]
        };
    };

    if (loading) {
        return (
            <div className="app-container">
                <div className="loader-container">
                    <div className="spinner"></div>
                    <h3 style={{ color: 'var(--primary-light)' }}>Đang tải dữ liệu hệ thống...</h3>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="app-container">
                <div className="loader-container" style={{ color: 'var(--danger)' }}>
                    <AlertCircle size={48} />
                    <h3>{error}</h3>
                </div>
            </div>
        );
    }

    return (
        <div className="app-container">
            <header className="header">
                <div className="header-title">
                    <GraduationCap size={32} />
                    NEU Admission Analytics
                </div>
                <div className="filters-container" style={{ display: 'flex', gap: '15px' }}>
                    <div className="filter-item">
                        <select value={methodFilter} onChange={(e) => setMethodFilter(e.target.value)} style={{ padding: '8px', borderRadius: '8px', backgroundColor: 'rgba(30, 41, 59, 0.7)', color: '#f8fafc', border: '1px solid rgba(255, 255, 255, 0.1)', outline: 'none' }}>
                            <option value="">Tất cả Phương thức</option>
                            {data.methods && data.methods.map(m => <option key={m.method_name} value={m.method_name}>{m.method_name}</option>)}
                        </select>
                    </div>
                    <div className="filter-item">
                        <select value={majorFilter} onChange={(e) => setMajorFilter(e.target.value)} style={{ padding: '8px', borderRadius: '8px', backgroundColor: 'rgba(30, 41, 59, 0.7)', color: '#f8fafc', border: '1px solid rgba(255, 255, 255, 0.1)', outline: 'none', maxWidth: '200px' }}>
                            <option value="">Tất cả Ngành</option>
                            {data.majors && data.majors.map(m => <option key={m.major_name} value={m.major_name}>{m.major_name}</option>)}
                        </select>
                    </div>
                    <div className="year-selector">
                        <Calendar size={20} color="var(--text-muted)" />
                        <select value={year} onChange={(e) => setYear(Number(e.target.value))}>
                            <option value={2023}>Năm 2023</option>
                            <option value={2024}>Năm 2024</option>
                            <option value={2025}>Năm 2025</option>
                        </select>
                    </div>
                </div>
            </header>

            <main className="main-content">
                {/* KPI Cards */}
                {data.overview && (
                    <div className="kpi-cards fade-in">
                        <div className="kpi-card glass-panel">
                            <div className="kpi-header">
                                <span className="kpi-title">Tổng Ứng Viên</span>
                                <div className="kpi-icon"><Users size={20} /></div>
                            </div>
                            <div className="kpi-value">{data.overview.total_applicants.toLocaleString()}</div>
                            <div className="kpi-subtext">Hồ sơ đăng ký xét tuyển hợp lệ</div>
                        </div>
                        <div className="kpi-card success glass-panel">
                            <div className="kpi-header">
                                <span className="kpi-title">Trúng Tuyển</span>
                                <div className="kpi-icon" style={{ color: 'var(--success)' }}><UserCheck size={20} /></div>
                            </div>
                            <div className="kpi-value">{data.overview.admitted_applicants.toLocaleString()}</div>
                            <div className="kpi-subtext">
                                <span className="trend-up"><TrendingUp size={14} className="mr-1" /> {data.overview.admission_rate_percent}%</span>
                                &nbsp;Tỉ lệ đỗ
                            </div>
                        </div>
                        <div className="kpi-card secondary glass-panel">
                            <div className="kpi-header">
                                <span className="kpi-title">Nhập Học</span>
                                <div className="kpi-icon" style={{ color: 'var(--secondary)' }}><GraduationCap size={20} /></div>
                            </div>
                            <div className="kpi-value">{data.overview.enrolled_applicants.toLocaleString()}</div>
                            <div className="kpi-subtext">
                                <span className="trend-up"><TrendingUp size={14} className="mr-1" /> {data.overview.enrollment_rate_percent}%</span>
                                &nbsp;Tỉ lệ nhập học
                            </div>
                        </div>
                    </div>
                )}

                {/* Dashboard Grid */}
                <div className="dashboard-grid fade-in" style={{ animationDelay: '0.1s' }}>
                    
                    {/* Funnel Chart */}
                    <div className="glass-panel chart-container col-span-4">
                        <div className="chart-header">
                            <h3 className="chart-title">Phễu Chuyển Đổi Tuyển Sinh</h3>
                            <p className="chart-subtitle">Từ ứng viên đến sinh viên chính thức</p>
                        </div>
                        <div className="chart-body">
                            <ReactECharts option={getFunnelOption()} style={{ height: '100%', width: '100%' }} />
                        </div>
                    </div>

                    {/* Majors Bar Chart */}
                    <div className="glass-panel chart-container col-span-8">
                        <div className="chart-header">
                            <h3 className="chart-title">Top 15 Ngành Học Hot Nhất</h3>
                            <p className="chart-subtitle">So sánh Đăng ký, Trúng tuyển và Nhập học</p>
                        </div>
                        <div className="chart-body">
                            <ReactECharts option={getMajorsBarOption()} style={{ height: '100%', width: '100%' }} />
                        </div>
                    </div>

                    {/* Methods Donut Chart */}
                    <div className="glass-panel chart-container col-span-4">
                        <div className="chart-header">
                            <h3 className="chart-title">Cơ Cấu Phương Thức Xét Tuyển</h3>
                            <p className="chart-subtitle">Phân bổ hồ sơ theo phương thức</p>
                        </div>
                        <div className="chart-body">
                            <ReactECharts option={getMethodsDonutOption()} style={{ height: '100%', width: '100%' }} />
                        </div>
                    </div>

                    {/* Motivation Chart */}
                    <div className="glass-panel chart-container col-span-8">
                        <div className="chart-header">
                            <h3 className="chart-title">Phân Tích Động Lực Ứng Viên</h3>
                            <p className="chart-subtitle">NV1-3 (Ưu tiên) vs NV&gt;3 (Dự phòng)</p>
                        </div>
                        <div className="chart-body">
                            <ReactECharts option={getMotivationOption()} style={{ height: '100%', width: '100%' }} />
                        </div>
                    </div>

                    {/* Regions Bar Chart */}
                    <div className="glass-panel chart-container col-span-6">
                        <div className="chart-header">
                            <h3 className="chart-title">Top 10 Địa Phương</h3>
                            <p className="chart-subtitle">Khu vực có lượng ứng viên đông đảo nhất</p>
                        </div>
                        <div className="chart-body">
                            <ReactECharts option={getRegionsBarOption()} style={{ height: '100%', width: '100%' }} />
                        </div>
                    </div>

                    {/* Clustering Network */}
                    <div className="glass-panel chart-container col-span-6">
                        <div className="chart-header">
                            <h3 className="chart-title">Mạng Lưới Nhóm Ngành</h3>
                            <p className="chart-subtitle">Các cặp ngành thường được đăng ký cùng nhau</p>
                        </div>
                        <div className="chart-body">
                            <ReactECharts option={getClusteringGraphOption()} style={{ height: '100%', width: '100%' }} />
                        </div>
                    </div>

                    {/* Advanced Gender Chart */}
                    <div className="glass-panel chart-container col-span-12">
                        <div className="chart-header">
                            <h3 className="chart-title">Phân Bổ Giới Tính Chuyên Sâu</h3>
                            <p className="chart-subtitle">Đăng ký & Tỉ lệ nhập học theo Giới tính</p>
                        </div>
                        <div className="chart-body" style={{ minHeight: '500px' }}>
                            <GenderAnalyticsChart data={data.gender} theme={chartTheme} />
                        </div>
                    </div>

                    {/* Geo Heatmap Chart */}
                    <div className="glass-panel chart-container col-span-12">
                        <div className="chart-header">
                            <h3 className="chart-title">Bản Đồ Nhiệt Tỉ Lệ Nhập Học</h3>
                            <p className="chart-subtitle">Phân bổ vùng miền trên lãnh thổ Việt Nam</p>
                        </div>
                        <div className="chart-body" style={{ minHeight: '600px' }}>
                            <GeoHeatmapChart data={data.geo} theme={chartTheme} />
                        </div>
                    </div>

                    {/* Score Analytics Chart */}
                    <div className="glass-panel chart-container col-span-12">
                        <div className="chart-header">
                            <h3 className="chart-title">Phân Tích Phổ Điểm THPT</h3>
                            <p className="chart-subtitle">Phân bổ phổ điểm, Điểm trung bình và Trung vị theo môn thi</p>
                        </div>
                        <div className="chart-body" style={{ minHeight: '400px' }}>
                            <ScoreBoxplotChart data={data.scores} theme={chartTheme} />
                        </div>
                    </div>

                </div>
            </main>
        </div>
    );
};

export default App;
