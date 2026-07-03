import { useEffect, useState, useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
import { formatNumber } from '../../utils/format';

const GeoHeatmapChart = ({ data, theme }) => {
    const [mapLoaded, setMapLoaded] = useState(false);

    // Hàm chuẩn hóa: Viết hoa chữ cái đầu và KHÔNG DẤU để khớp 100% với file JSON của bạn
    const normalizeName = (name) => {
        if (!name) return "";
        
        let cleanName = name.toString().trim();
        
        // 1. Loại bỏ các tiền tố Tiếng Việt phổ biến (bất kể hoa thường)
        cleanName = cleanName.replace(/^(Thành phố|Thanh pho|Tỉnh|Tinh|TP\.)\s+/i, "");

        // 2. Tiến hành xóa dấu, đưa về chữ thường và viết hoa lại chữ cái đầu từng từ
        return cleanName
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "") // Xóa toàn bộ dấu tổ hợp
            .replace(/đ/g, "d").replace(/Đ/g, "D")
            .toLowerCase()
            .split(' ')
            .filter(word => word.trim() !== "") // Loại bỏ khoảng trắng thừa
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ')
            // Dự phòng một số trường hợp đặc biệt sau khi chuyển đổi dấu
            .replace(/^(Thanh Pho|Tinh)\s+/i, ""); 
    };

    useEffect(() => {
        fetch('/vietnam.json')
            .then(res => res.json())
            .then(mapJson => {
                echarts.registerMap('VN', mapJson);
                setMapLoaded(true);
            })
            .catch(err => console.error("Error loading Vietnam GeoJSON:", err));
    }, []);

    const mapData = useMemo(() => {
        if (!data) return [];
        
        // 1. Chuẩn hóa dữ liệu tỉnh thành từ Backend về dạng chữ đầu, không dấu (ví dụ: "Can Tho")
        const processedData = data.map(d => ({
            name: normalizeName(d.province),
            value: d.yield_rate ?? 0,
            total_applicants: d.total_applicants ?? 0,
            admitted: d.admitted_applicants ?? 0,
            enrolled: d.enrolled_applicants ?? 0
        }));

        // 2. Cấu hình cho Hoàng Sa và Trường Sa gốc trong file JSON thành màu đen/tối của bản đồ
        // để chúng không bị tô màu xanh dương ở sai vị trí nữa
        const requiredRegions = ["Hoang Sa", "Truong Sa"];
        requiredRegions.forEach(region => {
            if (!processedData.find(d => d.name === region)) {
                processedData.push({ 
                    name: region, 
                    value: NaN, // Dùng NaN để loại bỏ khỏi thang màu Heatmap
                    itemStyle: {
                        areaColor: '#1e293b', // Ép về màu tối mặc định của bản đồ
                        borderColor: '#475569'
                    },
                    total_applicants: 0, 
                    admitted: 0, 
                    enrolled: 0 
                });
            }
        });

        return processedData;
    }, [data]);

    if (!mapLoaded) return <div style={{ color: 'var(--text-muted)' }}>Đang tải bản đồ...</div>;

    const option = {
        ...theme,
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                const item = mapData.find(d => d.name === params.name);
                
                // Tooltip cho vùng hoặc đảo chưa có số liệu tuyển sinh
                if (!item || item.total_applicants === 0) {
                    return `<div style="font-weight:bold;">${params.name}</div><div>Không có dữ liệu tuyển sinh</div>`;
                }
                
                return `
                    <div style="font-weight:bold;margin-bottom:5px;">${params.name}</div>
                    Đăng ký: ${formatNumber(item.total_applicants)}<br/>
                    Trúng tuyển: ${formatNumber(item.admitted)}<br/>
                    Nhập học: ${formatNumber(item.enrolled)}<br/>
                    <div style="margin-top:5px;padding-top:5px;border-top:1px solid rgba(255,255,255,0.2)">
                        Tỉ lệ nhập học: <strong style="color:#10b981">${item.value}%</strong>
                    </div>
                `;
            }
        },
        series: [
            {
                name: 'Tỉ lệ nhập học',
                type: 'map',
                map: 'VN',
                roam: false,
                data: mapData,
                itemStyle: { areaColor: '#1e293b', borderColor: '#475569' },
                emphasis: {
                    label: { show: true, color: '#fff' },
                    itemStyle: { areaColor: '#f59e0b' }
                }
            }
        ],
        graphic: [
            // CỤM HOÀNG SA: Đã dịch xuống dưới một chút (top: 32% -> 35%) và đổi màu chấm thành màu tối giống đất liền (#1e293b)
            {
                type: 'group',
                left: '65%', 
                top: '44%',  // ĐÃ SỬA: Tăng tỉ lệ % để đẩy cả cụm dịch xuống dưới
                children: [
                    {
                        type: 'text',
                        style: {
                            
                            fill: '#94a3b8',
                            fontSize: 11,
                            fontWeight: 'bold'
                        }
                    },
                    // ĐÃ SỬA: Chuyển màu fill về #1e293b giống màu đất liền mặc định của bạn
                    { type: 'circle', shape: { cx: 15, cy: 30, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 35, cy: 28, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 55, cy: 32, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 30, cy: 40, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 48, cy: 42, r: 2 }, style: { fill: '#1e293b' } }
                ]
            },
            // CỤM TRƯỜNG SA: Đã dịch xuống dưới một chút (top: 58% -> 61%) và đổi màu chấm thành màu tối giống đất liền (#1e293b)
            {
                type: 'group',
                left: '70%', 
                top: '70%',  // ĐÃ SỬA: Tăng tỉ lệ % để đẩy cả cụm dịch xuống dưới
                children: [
                    {
                        type: 'text',
                        style: {
                        
                            fill: '#94a3b8',
                            fontSize: 11,
                            fontWeight: 'bold'
                        }
                    },
                    // ĐÃ SỬA: Chuyển toàn bộ màu fill về #1e293b giống màu đất liền mặc định của bạn
                    { type: 'circle', shape: { cx: -20, cy: 35, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: -10, cy: 45, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 5, cy: 30, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 15, cy: 25, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 20, cy: 50, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 35, cy: 40, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 40, cy: 60, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 55, cy: 45, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 80, cy: 35, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 100, cy: 30, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 90, cy: 20, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 100, cy: 20, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 115, cy: 5, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 100, cy: 1, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 70, cy: 15, r: 2 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 60, cy: 20, r: 2.5 }, style: { fill: '#1e293b' } },
                    { type: 'circle', shape: { cx: 50, cy: 25, r: 2.5 }, style: { fill: '#1e293b' } }
                ]
            }
        ]
    };

    return <ReactECharts option={option} style={{ height: '100%', width: '100%' }} />;
};

export default GeoHeatmapChart;