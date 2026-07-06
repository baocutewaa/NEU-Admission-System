import { useState, useRef, useEffect } from 'react';
import { askChatbotApi } from '../services/api'; 

const ChatBot = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Xin chào! Tôi có thể giúp gì cho bạn về thông tin tuyển sinh năm nay?' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Tự động cuộn xuống tin nhắn mới nhất
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSendMessage = async (e) => {
        if (e) e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput(''); // Xóa trống thanh nhập liệu
        setMessages(prev => [...prev, { sender: 'user', text: userMessage }]);
        setLoading(true);

        try {
            // Gọi API thật đến FastAPI
            const data = await askChatbotApi(userMessage);
            
            setMessages(prev => [...prev, { 
                sender: 'bot', 
                text: data.answer,
                debug: {
                    sql: data.sql,
                    tables: data.tables_used,
                    rowCount: data.row_count
                }
            }]);

        } catch (error) {
            console.error("Lỗi kết nối Chatbot:", error);
            setMessages(prev => [...prev, { sender: 'bot', text: 'Đã xảy ra lỗi hệ thống hoặc AI Agent không phản hồi. Vui lòng thử lại sau!' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chatbot-container">
            <h2 className="chatbot-title">Chatbot AI Hỗ trợ Tuyển sinh</h2>
            <p className="chatbot-subtitle">
                Hệ thống tư vấn tự động kết nối trực tiếp với Cơ sở dữ liệu.
            </p>
            
            <div className="chatbot-window">
                <div className="chatbot-messages">
                    {messages.map((msg, index) => (
                        <div key={index} className={msg.sender === 'bot' ? 'message-bot' : 'message-user'}>
                            <p>{msg.text}</p>
                            
                            {/* KHU VỰC HIỂN THỊ DEBUG SQL NẾU CÓ */}
                            {msg.debug && msg.debug.sql && (
                                <details className="chatbot-debug-details">
                                    <summary className="chatbot-debug-summary">Xem câu lệnh truy vấn nội bộ (T-SQL)</summary>
                                    <pre className="chatbot-debug-pre">
                                        {msg.debug.sql}
                                    </pre>
                                    <div className="chatbot-debug-meta">
                                        <span className="chatbot-debug-badge-blue">Số dòng kết quả: {msg.debug.rowCount}</span>
                                        {msg.debug.tables && msg.debug.tables.length > 0 && (
                                            <span className="chatbot-debug-badge-purple">Bảng: {msg.debug.tables.join(', ')}</span>
                                        )}
                                    </div>
                                </details>
                            )}
                        </div>
                    ))}
                    {loading && <div className="message-bot loading">Bot đang phân tích dữ liệu...</div>}
                    <div ref={messagesEndRef} />
                </div>
                
                <form onSubmit={handleSendMessage} className="chatbot-input-area">
                    <input 
                        type="text" 
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={loading ? "Vui lòng đợi..." : "Nhập câu hỏi (Ví dụ: Thống kê phổ điểm khối A00)..."} 
                        className="chatbot-input"
                        disabled={loading}
                    />
                    <button type="submit" className="chatbot-send-btn" disabled={loading}>
                        {loading ? '...' : 'Gửi'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatBot;