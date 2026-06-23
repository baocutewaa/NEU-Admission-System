import ReactECharts from 'echarts-for-react';
import { getCountByBracket } from '../../utils/chartHelpers';

const ScoreBoxplotChart = ({ data, theme }) => {
    if (!data || data.length === 0) return <div style={{ color: 'var(--text-muted)' }}>Không có dữ liệu điểm thi</div>;

    const subjects = data.map(d => d.subject_name);
    
    const bracketKeys = ["<5", "5-7", "7-8", "8-9", "9-10"];
    const seriesData = bracketKeys.map(bk => ({
        name: bk,
        type: 'bar',
        stack: 'total',
        data: data.map(d => getCountByBracket(d.brackets, bk))
    }));

    const option = {
        ...theme,
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            formatter: function (params) {
                let res = `<div style="font-weight:bold">${params[0].axisValue}</div>`;
                params.forEach(p => {
                    if (p.seriesType === 'bar') {
                        res += `${p.marker} ${p.seriesName}: ${p.value}<br/>`;
                    }
                });
                const subjData = data.find(d => d.subject_name === params[0].axisValue);
                if (subjData) {
                    res += `<hr style="margin:5px 0; border:0; border-top:1px solid rgba(255,255,255,0.2)"/>`;
                    res += `Điểm trung bình: <strong style="color:#60a5fa">${subjData.avg_score ?? 0}</strong><br/>`;
                    res += `Trung vị (Median): <strong style="color:#34d399">${subjData.median_score ?? 0}</strong><br/>`;
                    res += `Min/Max: ${subjData.min_score ?? 0} - ${subjData.max_score ?? 0}`;
                }
                return res;
            }
        },
        legend: {
            data: bracketKeys,
            textStyle: { color: '#94a3b8' }
        },
        // Tăng bottom từ 3% lên 15% để tạo không gian chứa các nhãn xoay nghiêng
        grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
        xAxis: { 
            type: 'category', 
            data: subjects,
            axisLabel: {
                interval: 0,       // Hiển thị đầy đủ tất cả các môn, không ẩn bớt
                rotate: 30,        // Xoay chữ nghiêng 30 độ chống đè dính nhau
                width: 90,         // Giới hạn độ rộng tối đa của chữ môn học
                overflow: 'truncate' // Tự động cắt ngắn thêm dấu "..." nếu tên môn quá dài
            }
        },
        yAxis: { type: 'value', name: 'Số lượng TS', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
        series: [
            ...seriesData.map((s, i) => ({
                ...s,
                itemStyle: {
                    color: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'][i],
                    borderRadius: i === 4 ? [4, 4, 0, 0] : 0
                }
            }))
        ]
    };

    return <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />;
};

export default ScoreBoxplotChart;