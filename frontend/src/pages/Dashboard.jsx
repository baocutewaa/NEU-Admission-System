import { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Users, UserCheck, GraduationCap, TrendingUp, AlertTriangle } from 'lucide-react';
import { formatNumber } from '../utils/format';

import { 
    fetchOverview, fetchRegions, fetchMajors, 
    fetchMethods, fetchMotivation, fetchClustering, fetchPreferenceMultivariate,
    fetchGenderDistribution, fetchGeographicEnrollment, fetchScoreAnalytics
} from '../services/api';

import GenderAnalyticsChart from '../components/charts/GenderAnalyticsChart';
import GeoHeatmapChart from '../components/charts/GeoHeatmapChart';
import ScoreBoxplotChart from '../components/charts/ScoreBoxplotChart';

const Dashboard = ({ year, methodFilter, majorFilter }) => {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({
        overview: {}, regions: [], majors: [], methods: [],
        motivation: {}, clustering: [], multivariate: [], gender: [], geo: [], scores: []
    });

    useEffect(() => {
        let isMounted = true;
        const loadData = async () => {
            setLoading(true);
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

                if (isMounted) {
                    setData({
                        overview: overviewRes || { total_applicants: 0, admitted_applicants: 0, enrolled_applicants: 0, admission_rate_percent: 0, enrollment_rate_percent: 0 },
                        regions: regionsRes || [],
                        majors: majorsRes || [],
                        methods: methodsRes || [],
                        motivation: motivationRes || { high_motivation: { applicants: 0, admitted: 0 }, low_motivation: { applicants: 0, admitted: 0 } },
                        clustering: clusteringRes || [],
                        multivariate: multivariateRes || [],
                        gender: genderRes || [],
                        geo: geoRes || [],
                        scores: scoreRes || []
                    });
                }
            } catch (err) {
                console.warn("Lỗi tải dữ liệu. Hệ thống tự động hiển thị khung giao diện rỗng.", err);
            } finally {
                if (isMounted) setLoading(false);
            }
        };
        loadData();
        return () => { isMounted = false; };
    }, [year, methodFilter, majorFilter]);

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
        const total = data.overview?.total_applicants || 0;
        return {
            ...chartTheme,
            tooltip: { trigger: 'item', formatter: "{a} <br/>{b} : {c} ({d}%)" },
            series: [{
                name: 'Tuyển sinh', type: 'funnel',
                left: '10%', top: 20, bottom: 20, width: '80%',
                min: 0, max: total || 100,
                minSize: '0%', maxSize: '100%',
                sort: 'descending', gap: 2,
                label: { show: true, position: 'inside', formatter: '{b}: {c}', color: '#fff', fontSize: 14 },
                data: [
                    { value: total, name: 'Tổng ứng viên', itemStyle: { color: '#3b82f6' } },
                    { value: data.overview?.admitted_applicants || 0, name: 'Trúng tuyển', itemStyle: { color: '#10b981' } },
                    { value: data.overview?.enrolled_applicants || 0, name: 'Nhập học', itemStyle: { color: '#8b5cf6' } }
                ]
            }]
        };
    };

    const getMajorsBarOption = () => {
        if (!data.majors || !data.majors.length) return {};
        const sorted = [...data.majors].sort((a, b) => (b.total_applicants || 0) - (a.total_applicants || 0)).slice(0, 15);
        return {
            ...chartTheme,
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            legend: { data: ['Đăng ký', 'Trúng tuyển', 'Nhập học'], top: 0 },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
            yAxis: { type: 'category', data: sorted.map(m => m.major_name || 'Chưa rõ').reverse(), axisLabel: { width: 150, overflow: 'truncate' } },
            series: [
                { name: 'Đăng ký', type: 'bar', stack: 'total', data: sorted.map(m => m.total_applicants || 0).reverse(), itemStyle: { color: '#3b82f6' } },
                { name: 'Trúng tuyển', type: 'bar', stack: 'total', data: sorted.map(m => m.admitted_applicants || 0).reverse(), itemStyle: { color: '#10b981' } },
                { name: 'Nhập học', type: 'bar', stack: 'total', data: sorted.map(m => m.enrolled_applicants || 0).reverse(), itemStyle: { color: '#8b5cf6' } }
            ]
        };
    };

    const getMethodsDonutOption = () => {
        if (!data.methods || !data.methods.length) return {};
        return {
            ...chartTheme,
            tooltip: { trigger: 'item' },
            legend: { orient: 'vertical', left: 'left' },
            series: [{
                name: 'Phương thức', type: 'pie', radius: ['40%', '70%'],
                itemStyle: { borderRadius: 10, borderColor: '#1e293b', borderWidth: 2 },
                label: { show: false },
                emphasis: { label: { show: true, fontSize: 18, fontWeight: 'bold', color: '#fff' } },
                data: data.methods.map(m => ({ value: m.total_applicants || 0, name: m.method_name || 'Chưa rõ' }))
            }]
        };
    };

    // Thay thế hàm getRegionsBarOption hiện tại trong Dashboard.jsx bằng đoạn này:
    const getRegionsBarOption = () => {
        // 1. Kiểm tra an toàn dữ liệu
        if (!data.regions || !data.regions.length) return {};
        
        // 2. Làm sạch tên và đồng bộ key dữ liệu
        const cleanData = data.regions.map(r => ({
            ...r,
            // Hỗ trợ cả r.region hoặc r.province phòng trường hợp API đổi tên key
            regionName: (r.region || r.province || 'Chưa rõ').replace(/^\d+[\s.]*/, '').trim(),
            // Đồng bộ giá trị để dễ tính toán
            applicantCount: r.total_applicants || r.value || 0
        }));

        // 3. Sắp xếp giảm dần (cao nhất đứng trước) và cắt lấy đúng 10 phần tử
        const sorted = [...cleanData]
            .sort((a, b) => b.applicantCount - a.applicantCount)
            .slice(0, 10);

        // 4. Trả về cấu hình ECharts
        return {
            ...chartTheme, // Giữ nguyên theme gốc của bạn
            tooltip: { 
                trigger: 'axis', 
                axisPointer: { type: 'shadow' } 
            },
            grid: { 
                left: '3%', 
                right: '4%', 
                bottom: '15%', 
                containLabel: true 
            },
            xAxis: { 
                type: 'category', 
                data: sorted.map(r => r.regionName), // Top 10 tên địa phương
                axisLabel: { 
                    interval: 0, 
                    rotate: 45, 
                    width: 100, 
                    overflow: 'truncate' 
                } 
            },
            yAxis: { 
                type: 'value', 
                splitLine: { 
                    lineStyle: { color: 'rgba(255,255,255,0.05)' } 
                } 
            },
            series: [{
                name: 'Ứng viên', 
                type: 'bar', 
                barWidth: '50%',
                itemStyle: {
                    color: { 
                        type: 'linear', 
                        x: 0, y: 0, x2: 0, y2: 1, 
                        colorStops: [
                            { offset: 0, color: '#60a5fa' }, 
                            { offset: 1, color: '#3b82f6' }
                        ] 
                    },
                    borderRadius: [4, 4, 0, 0] // Bo tròn 2 góc trên của cột
                },
                data: sorted.map(r => r.applicantCount) // Top 10 số lượng tương ứng
            }]
        };
    };

    const getMotivationOption = () => {
        if (!data.motivation || !data.motivation.high_motivation) return {};
        return {
            ...chartTheme,
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            legend: { data: ['Ứng viên', 'Trúng tuyển'] },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: { type: 'category', data: ['Động lực cao (NV1-3)', 'Dự phòng (NV>3)'] },
            yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
            series: [
                { name: 'Ứng viên', type: 'bar', data: [data.motivation.high_motivation.applicants || 0, data.motivation.low_motivation?.applicants || 0], itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] } },
                { name: 'Trúng tuyển', type: 'bar', data: [data.motivation.high_motivation.admitted || 0, data.motivation.low_motivation?.admitted || 0], itemStyle: { color: '#10b981', borderRadius: [4, 4, 0, 0] } }
            ]
        };
    };

    const getClusteringGraphOption = () => {
        if (!data.clustering || !data.clustering.length) return {};
        const nodesMap = new Map();
        const links = [];
        
        data.clustering.forEach(c => {
            const { nganh_1, nganh_2, frequency } = c;
            if (nganh_1 && nganh_2) {
                nodesMap.set(nganh_1, (nodesMap.get(nganh_1) || 0) + (frequency || 0));
                nodesMap.set(nganh_2, (nodesMap.get(nganh_2) || 0) + (frequency || 0));
                links.push({ source: nganh_1, target: nganh_2, value: frequency || 0 });
            }
        });
        
        if (nodesMap.size === 0) return {};
        
        const nodes = Array.from(nodesMap.keys()).map(name => ({
            name, 
            value: nodesMap.get(name),
            // Điều chỉnh lại symbolSize vừa phải (từ 12px đến 35px) để nhường chỗ cho nhãn chữ
            symbolSize: Math.max(12, Math.min(35, 10 + (nodesMap.get(name) / 15))),
            itemStyle: { color: '#8b5cf6' }
        }));
        
        return {
            ...chartTheme,
            tooltip: { 
                trigger: 'item',
                formatter: function (params) {
                    if (params.dataType === 'node') {
                        return `<strong>Ngành:</strong> ${params.name}<br/>Tần suất xuất hiện: ${params.value}`;
                    }
                    return `<strong>Mối liên hệ:</strong><br/>${params.data.source} ↔ ${params.data.target}<br/>Số lần đăng ký chung: ${params.data.value}`;
                }
            },
            series: [{
                type: 'graph', 
                layout: 'force', 
                roam: true, // Giữ nguyên cho phép cuộn chuột phóng to/thu nhỏ để nhìn rõ hơn
                
                // --- CẤU HÌNH NHÃN CHỮ CHỐNG ĐÈ ---
                label: { 
                    show: true, 
                    position: 'right', 
                    color: '#cbd5e1',
                    fontSize: 12,
                    distance: 6,           // Khoảng cách từ dấu chấm đến chữ
                    overflow: 'break',     // Tự động xuống dòng nếu tên ngành quá dài
                    hideOverlap: true      // Tự động ẩn các nhãn bị đè nhau khi thu nhỏ biểu đồ
                },
                
                // --- TĂNG MẠNH LỰC ĐẨY VẬT LÝ VÀ ĐỘ DÀI LIÊN KẾT ---
                force: { 
                    repulsion: 800,        // Tăng từ 200 lên 800 để các chữ đẩy xa nhau hẳn ra ngoài biên
                    edgeLength: [100, 180], // Thay vì cố định 100, cho phép dao động đến 180px giúp biểu đồ bung rộng tự nhiên
                    gravity: 0.08          // Giảm nhẹ lực hút tâm để các nhóm ngành dạt xa nhau hơn
                },
                
                data: nodes,
                links: links.map(l => ({ 
                    ...l, 
                    lineStyle: { 
                        // Độ dày đường nối dựa trên tần suất cặp ngành xuất hiện cùng nhau
                        width: Math.max(1.5, Math.min(6, l.value / 10)), 
                        color: 'rgba(255,255,255,0.15)',
                        curveness: 0.15 // Bo cong nhẹ đường nối giúp tổng thể mượt mà, dễ nhìn hơn
                    } 
                })),
                
                // Thêm hiệu ứng nổi bật khi di chuột vào 1 ngành
                emphasis: {
                    focus: 'adjacency', // Làm sáng ngành đang chọn và các ngành liên kết trực tiếp, làm mờ các ngành khác
                    lineStyle: {
                        width: 4,
                        color: '#a78bfa'
                    }
                }
            }]
        };
    };

    if (loading) return <div className="dashboard-loading">Đang tải dữ liệu Phân tích Tuyển sinh...</div>;

    return (
        <div className="dashboard-page-container">
            
            {/* CẢNH BÁO NĂM DỮ LIỆU */}
            {year && parseInt(year) !== 2024 && (
                <div className="flex items-center gap-2 bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 p-3 mb-6 rounded-lg text-sm">
                    <AlertTriangle size={18} />
                    <span>Lưu ý: Script giả lập dữ liệu (DataGenerate.py) hiện đang hardcode cho năm 2024. Các biểu đồ dưới đây có thể không có dữ liệu cho năm {year}.</span>
                </div>
            )}

            {/* TẦNG 1: CHIA GRID CHÍNH */}
            <div className="dashboard-top-section-grid">
                
                {/* KHỐI TRÁI */}
                <div className="kpi-left-column">
                    <div className="kpi-card-wrapper">
                        <div className="kpi-card-header">
                            <span className="kpi-card-title">Tổng Ứng Viên</span>
                        </div>
                        <div className="kpi-card-icon-container">
                            <Users className="kpi-icon icon-blue" size={24} />
                        </div>
                        <div className="kpi-card-value">
                            {formatNumber(data.overview?.total_applicants)}
                        </div>
                        <div className="kpi-card-subtext">Hồ sơ đăng ký hợp lệ</div>
                    </div>

                    <div className="kpi-card-wrapper">
                        <div className="kpi-card-header">
                            <span className="kpi-card-title">Nhập Học</span>
                        </div>
                        <div className="kpi-card-icon-container">
                            <GraduationCap className="kpi-icon icon-purple" size={24} />
                        </div>
                        <div className="kpi-card-value">
                            {formatNumber(data.overview?.enrolled_applicants)}
                        </div>
                        <div className="kpi-card-subtext">
                            <span className="kpi-trend trend-green">
                                <TrendingUp size={14} /> {data.overview?.enrollment_rate_percent || 0}%
                            </span> Tỉ lệ nhập học
                        </div>
                    </div>
                </div>

                {/* KHỐI PHẢI */}
                <div className="kpi-right-column">
                    <div className="kpi-card-wrapper">
                        <div className="kpi-card-header">
                            <span className="kpi-card-title">Trúng Tuyển</span>
                        </div>
                        <div className="kpi-card-icon-container">
                            <UserCheck className="kpi-icon icon-green" size={24} />
                        </div>
                        <div className="kpi-card-value">
                            {formatNumber(data.overview?.admitted_applicants)}
                        </div>
                        <div className="kpi-card-subtext">
                            <span className="kpi-trend trend-green">
                                <TrendingUp size={14} /> {data.overview?.admission_rate_percent || 0}%
                            </span> Tỉ lệ đỗ
                        </div>
                    </div>

                    <div className="kpi-card-placeholder"></div>
                </div>
            </div>

            {/* TẦNG 2 */}
            {/* Thêm style minHeight vào div container này */}
            <div className="dashboard-chart-fullwidth-box glass-panel">
                <div className="chart-box-header">
                    <h3 className="chart-box-title">Phân Tích Giới Tính Thí Sinh</h3>
                    <p className="chart-box-subtitle">Cơ cấu phân bổ nam/nữ theo dữ liệu tuyển sinh</p>
                </div>
                {/* Đảm bảo chart-box-body chiếm trọn chiều cao */}
                <div className="chart-box-body" style={{ height: '1200px' }}>
                    {data.gender.length > 0 ? (
                        <GenderAnalyticsChart data={data.gender} theme={chartTheme} />
                    ) : (
                        <div className="chart-empty-state">Đang chờ dữ liệu phân tích giới tính...</div>
                    )}
                </div>
            </div>

            {/* TẦNG 3 */}
            <div className="dashboard-bottom-grid">
                <div className="glass-panel chart-container-item item-span-4">
                    <div className="chart-box-header">
                        <h3 className="chart-box-title">Phễu Chuyển Đổi Tuyển Sinh</h3>
                        <p className="chart-box-subtitle">Từ ứng viên đến sinh viên chính thức</p>
                    </div>
                    <div className="chart-box-body">
                        <ReactECharts option={getFunnelOption()} style={{ height: '100%', width: '100%' }} />
                    </div>
                </div>

                <div className="glass-panel chart-container-item item-span-8">
                    <div className="chart-box-header">
                        <h3 className="chart-box-title">Top 15 Ngành Học Hot Nhất</h3>
                        <p className="chart-box-subtitle">So sánh Đăng ký, Trúng tuyển và Nhập học</p>
                    </div>
                    <div className="chart-box-body">
                        {data.majors.length > 0 ? <ReactECharts option={getMajorsBarOption()} style={{ height: '100%', width: '100%' }} /> : <div className="chart-empty-state">Không có dữ liệu ngành học</div>}
                    </div>
                </div>

                <div className="glass-panel chart-container-item item-span-4">
                    <div className="chart-box-header">
                        <h3 className="chart-box-title">Cơ Cấu Phương Thức Xét Tuyển</h3>
                        <p className="chart-box-subtitle">Phân bổ hồ sơ theo phương thức</p>
                    </div>
                    <div className="chart-box-body">
                        {data.methods.length > 0 ? <ReactECharts option={getMethodsDonutOption()} style={{ height: '100%', width: '100%' }} /> : <div className="chart-empty-state">Không có dữ liệu phương thức</div>}
                    </div>
                </div>

                <div className="glass-panel chart-container-item item-span-8">
                    <div className="chart-box-header">
                        <h3 className="chart-box-title">Phân Tích Động Lực Ứng Viên</h3>
                        <p className="chart-box-subtitle">NV1-3 (Ưu tiên) vs NV&gt;3 (Dự phòng)</p>
                    </div>
                    <div className="chart-box-body">
                        <ReactECharts option={getMotivationOption()} style={{ height: '100%', width: '100%' }} />
                    </div>
                </div>

                <div className="glass-panel chart-container-item item-span-6">
                    <div className="chart-box-header">
                        <h3 className="chart-box-title">Top 10 Địa Phương</h3>
                        <p className="chart-box-subtitle">Khu vực có lượng ứng viên đông đảo nhất</p>
                    </div>
                    <div className="chart-box-body">
                        {data.regions.length > 0 ? <ReactECharts option={getRegionsBarOption()} style={{ height: '100%', width: '100%' }} /> : <div className="chart-empty-state">Không có dữ liệu vùng miền</div>}
                    </div>
                </div>

                <div className="glass-panel chart-container-item item-span-6">
                    <div className="chart-box-header">
                        <h3 className="chart-box-title">Mạng Lưới Nhóm Ngành</h3>
                        <p className="chart-box-subtitle">Các cặp ngành thường được đăng ký cùng nhau</p>
                    </div>
                    <div className="chart-box-body">
                        {data.clustering.length > 0 ? <ReactECharts option={getClusteringGraphOption()} style={{ height: '100%', width: '100%' }} /> : <div className="chart-empty-state">Không có dữ liệu mạng lưới</div>}
                    </div>
                </div>

                <div className="glass-panel chart-container-item item-span-12" style={{ minHeight: '500px' }}>
                    {/* BỔ SUNG PHẦN TIÊU ĐỀ BIỂU ĐỒ */}
                    <div className="chart-box-header">
                        <h3 className="chart-box-title">Bản Đồ Nhiệt Địa Lý</h3>
                        <p className="chart-box-subtitle">Phân bổ thí sinh nhập học theo từng tỉnh thành</p>
                    </div>

                    {/* PHẦN BODY CHỨA BIỂU ĐỒ */}
                    <div className="chart-box-body">
                        {data.geo.length > 0 ? (
                            <GeoHeatmapChart data={data.geo} theme={chartTheme} />
                        ) : (
                            <div className="chart-empty-state">Đang chờ bản đồ nhiệt địa lý...</div>
                        )}
                    </div>
                </div>

                <div className="glass-panel chart-container-item item-span-12" style={{ minHeight: '400px' }}>
                    <div className="chart-box-body">
                        {data.scores.length > 0 ? <ScoreBoxplotChart data={data.scores} theme={chartTheme} /> : <div className="chart-empty-state">Đang chờ số liệu phân tích điểm số THPT...</div>}
                    </div>
                </div>
            </div>

        </div>
    );
};

export default Dashboard;