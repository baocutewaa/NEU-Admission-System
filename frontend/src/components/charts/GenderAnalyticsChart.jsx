import ReactECharts from 'echarts-for-react';
import { reverseDataArray } from '../../utils/chartHelpers';

const GenderAnalyticsChart = ({ data, theme }) => {
    if (!data || data.length === 0) {
        return <div style={{ color: 'var(--text-muted)' }}>Không có dữ liệu phân bổ giới tính</div>;
    }

    const majors = reverseDataArray(data, 'major_name');
    const maleApplied = reverseDataArray(data, 'male_applied');
    const femaleApplied = reverseDataArray(data, 'female_applied');
    
    // Tính % cơ cấu Nam / Nữ dựa trên tổng số đăng ký của ngành
    const maleYield = data.map(d => {
        const total = (d.male_applied ?? 0) + (d.female_applied ?? 0);
        return total > 0 ? Math.round((d.male_applied / total) * 100) : 0;
    }).reverse();

    const femaleYield = data.map(d => {
        const total = (d.male_applied ?? 0) + (d.female_applied ?? 0);
        return total > 0 ? Math.round((d.female_applied / total) * 100) : 0;
    }).reverse();

    const option = {
        ...theme,
        tooltip: { 
            trigger: 'axis', 
            axisPointer: { type: 'shadow' },
            formatter: function (params) {
                let majorName = params[0].name;
                let res = `<div style="font-weight:bold;margin-bottom:5px;">${majorName}</div>`;
                params.forEach(p => {
                    const isRatio = p.seriesName.includes('%');
                    const valueStr = isRatio ? `${p.value}%` : p.value.toLocaleString();
                    res += `${p.marker} ${p.seriesName}: <strong>${valueStr}</strong><br/>`;
                });
                return res;
            }
        },
        axisPointer: { link: [{ xAxisIndex: 'all' }] },
        legend: {
            data: ['Nam (Đăng ký)', 'Nữ (Đăng ký)', 'Nam (Tỉ lệ %)', 'Nữ (Tỉ lệ %)'],
            bottom: 0,
            itemGap: 20
        },
        grid: [
            { left: '16%', width: '8%', bottom: '10%', top: '5%' },   // Grid Line Nam
            { left: '28%', width: '54%', bottom: '10%', top: '5%' },  // Grid Bar Trung tâm
            { right: '10%', width: '8%', bottom: '10%', top: '5%' }   // Grid Line Nữ
        ],
        xAxis: [
            // Trục X bên trái (Nam %): Ẩn hoàn toàn chữ số đè nhau, chỉ giữ lại lưới dọc
            { 
                gridIndex: 0, 
                type: 'value', 
                min: 0, 
                max: 100, 
                splitLine: { show: true }, 
                axisLabel: { show: false }, 
                axisTick: { show: false },
                axisLine: { show: false }
            },
            // Trục X chính giữa (Số lượng tuyển sinh)
            { 
                gridIndex: 1, 
                type: 'value', 
                name: 'Số lượng',
                nameLocation: 'end',
                nameGap: 10
            }, 
            // Trục X bên phải (Nữ %): Ẩn hoàn toàn chữ số đè nhau
            { 
                gridIndex: 2, 
                type: 'value', 
                min: 0, 
                max: 100, 
                splitLine: { show: true }, 
                axisLabel: { show: false }, 
                axisTick: { show: false },
                axisLine: { show: false }
            }
        ],
        yAxis: [
            { gridIndex: 0, type: 'category', data: majors, axisLabel: { width: 140, overflow: 'truncate' } },
            { gridIndex: 1, type: 'category', data: majors, show: false },
            { gridIndex: 2, type: 'category', data: majors, show: false }
        ],
        series: [
            {
                name: 'Nam (Tỉ lệ %)', type: 'line', xAxisIndex: 0, yAxisIndex: 0,
                itemStyle: { color: '#3b82f6' }, lineStyle: { width: 2, type: 'dashed' },
                symbol: 'circle', symbolSize: 8, data: maleYield
            },
            {
                name: 'Nam (Đăng ký)', type: 'bar', stack: 'total', xAxisIndex: 1, yAxisIndex: 1,
                itemStyle: { color: '#60a5fa' }, data: maleApplied
            },
            {
                name: 'Nữ (Đăng ký)', type: 'bar', stack: 'total', xAxisIndex: 1, yAxisIndex: 1,
                itemStyle: { color: '#f472b6' }, data: femaleApplied
            },
            {
                name: 'Nữ (Tỉ lệ %)', type: 'line', xAxisIndex: 2, yAxisIndex: 2,
                itemStyle: { color: '#ec4899' }, lineStyle: { width: 2, type: 'dashed' },
                symbol: 'circle', symbolSize: 8, z: 10, data: femaleYield
            }
        ]
    };

    return <ReactECharts option={option} style={{ height: '100%', minHeight: '1200px', width: '100%' }} />;
};

export default GenderAnalyticsChart;