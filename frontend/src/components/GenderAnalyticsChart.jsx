import React from 'react';
import ReactECharts from 'echarts-for-react';

const GenderAnalyticsChart = ({ data, theme }) => {
    if (!data || data.length === 0) {
        return <div style={{ color: 'var(--text-muted)' }}>Không có dữ liệu phân bổ giới tính</div>;
    }

    const majors = data.map(d => d.major_name).reverse();
    const maleApplied = data.map(d => d.male_applied).reverse();
    const femaleApplied = data.map(d => d.female_applied).reverse();
    
    // Yield rate (Enrolled / Admitted) for lines
    const maleYield = data.map(d => d.male_admitted > 0 ? (d.male_enrolled / d.male_admitted * 100).toFixed(1) : 0).reverse();
    const femaleYield = data.map(d => d.female_admitted > 0 ? (d.female_enrolled / d.female_admitted * 100).toFixed(1) : 0).reverse();

    const option = {
        ...theme,
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' }
        },
        legend: {
            data: ['Nam (Đăng ký)', 'Nữ (Đăng ký)', 'Nam (Tỉ lệ nhập học %)', 'Nữ (Tỉ lệ nhập học %)'],
            textStyle: { color: '#94a3b8' }
        },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: [
            { type: 'value', name: 'Số lượng', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
            { type: 'value', name: 'Tỉ lệ (%)', min: 0, max: 100, splitLine: { show: false }, position: 'top' }
        ],
        yAxis: { type: 'category', data: majors, axisLabel: { width: 150, overflow: 'truncate' } },
        series: [
            {
                name: 'Nam (Đăng ký)', type: 'bar', stack: 'total',
                itemStyle: { color: '#3b82f6' }, data: maleApplied
            },
            {
                name: 'Nữ (Đăng ký)', type: 'bar', stack: 'total',
                itemStyle: { color: '#ec4899' }, data: femaleApplied
            },
            {
                name: 'Nam (Tỉ lệ nhập học %)', type: 'line', xAxisIndex: 1,
                itemStyle: { color: '#60a5fa' }, lineStyle: { width: 3, type: 'dashed' }, data: maleYield
            },
            {
                name: 'Nữ (Tỉ lệ nhập học %)', type: 'line', xAxisIndex: 1,
                itemStyle: { color: '#f472b6' }, lineStyle: { width: 3, type: 'dashed' }, data: femaleYield
            }
        ]
    };

    return <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />;
};

export default GenderAnalyticsChart;
