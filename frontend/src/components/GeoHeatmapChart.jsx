import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';

const GeoHeatmapChart = ({ data, theme }) => {
    const [mapLoaded, setMapLoaded] = useState(false);

    useEffect(() => {
        fetch('/vietnam.json')
            .then(res => res.json())
            .then(mapJson => {
                echarts.registerMap('VN', mapJson);
                setMapLoaded(true);
            })
            .catch(err => console.error("Error loading Vietnam GeoJSON:", err));
    }, []);

    if (!mapLoaded) return <div style={{ color: 'var(--text-muted)' }}>Đang tải bản đồ...</div>;
    if (!data || data.length === 0) return <div style={{ color: 'var(--text-muted)' }}>Không có dữ liệu địa lý</div>;

    const mapData = data.map(d => ({
        name: d.province,
        value: d.yield_rate,
        total_applicants: d.total_applicants,
        admitted: d.admitted_applicants,
        enrolled: d.enrolled_applicants
    }));

    const maxYield = Math.max(...mapData.map(d => d.value), 100);

    const option = {
        ...theme,
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                const data = params.data;
                if (!data) return params.name;
                return `
                    <div style="font-weight:bold;margin-bottom:5px;">${params.name}</div>
                    Đăng ký: ${data.total_applicants}<br/>
                    Trúng tuyển: ${data.admitted}<br/>
                    Nhập học: ${data.enrolled}<br/>
                    <div style="margin-top:5px;padding-top:5px;border-top:1px solid rgba(255,255,255,0.2)">
                        Tỉ lệ nhập học: <strong style="color:#10b981">${data.value}%</strong>
                    </div>
                `;
            }
        },
        visualMap: {
            min: 0,
            max: maxYield,
            text: ['Cao', 'Thấp'],
            realtime: false,
            calculable: true,
            inRange: {
                color: ['#0f172a', '#1e3a8a', '#3b82f6', '#93c5fd', '#10b981']
            },
            textStyle: { color: '#94a3b8' }
        },
        series: [
            {
                name: 'Tỉ lệ nhập học',
                type: 'map',
                map: 'VN',
                roam: true,
                itemStyle: {
                    areaColor: '#1e293b',
                    borderColor: '#475569'
                },
                emphasis: {
                    label: { show: true, color: '#fff' },
                    itemStyle: { areaColor: '#f59e0b' }
                },
                data: mapData
            }
        ]
    };

    return <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />;
};

export default GeoHeatmapChart;
