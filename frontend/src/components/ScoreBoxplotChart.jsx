import React from 'react';
import ReactECharts from 'echarts-for-react';

const ScoreBoxplotChart = ({ data, theme }) => {
    if (!data || data.length === 0) return <div style={{ color: 'var(--text-muted)' }}>Không có dữ liệu điểm thi</div>;

    const subjects = data.map(d => d.subject_name);
    
    // We have 5 brackets: "<5", "5-7", "7-8", "8-9", "9-10"
    const bracketKeys = ["<5", "5-7", "7-8", "8-9", "9-10"];
    const seriesData = bracketKeys.map(bk => ({
        name: bk,
        type: 'bar',
        stack: 'total',
        data: data.map(d => {
            const bracketObj = d.brackets.find(b => b.bracket === bk);
            return bracketObj ? bracketObj.count : 0;
        })
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
                    res += `Điểm trung bình: <strong style="color:#60a5fa">${subjData.avg_score}</strong><br/>`;
                    res += `Trung vị (Median): <strong style="color:#34d399">${subjData.median_score}</strong><br/>`;
                    res += `Min/Max: ${subjData.min_score} - ${subjData.max_score}`;
                }
                return res;
            }
        },
        legend: {
            data: bracketKeys,
            textStyle: { color: '#94a3b8' }
        },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: subjects },
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
