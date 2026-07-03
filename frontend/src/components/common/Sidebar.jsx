
import { LayoutDashboard, MessageSquare, Search } from 'lucide-react';

const Sidebar = ({ currentPage, setCurrentPage }) => {
    const menuItems = [
        { id: 'dashboard', name: 'Dashboard', icon: <LayoutDashboard size={18} /> },
        { id: 'chatbot', name: 'Chatbot AI', icon: <MessageSquare size={18} /> },
        { id: 'search', name: 'Tra cứu Học sinh', icon: <Search size={18} /> }
    ];

    return (
        <aside className="neu-sidebar" style={{ height: 'calc(100vh - 70px)' }}>
            <nav className="neu-sidebar-nav">
                {menuItems.map((item) => {
                    const isActive = currentPage === item.id;

                    return (
                        <div
                            key={item.id}
                            onClick={() => setCurrentPage(item.id)}
                            className={`neu-sidebar-item ${isActive ? 'active' : ''}`}
                        >
                            <span className="neu-sidebar-icon">
                                {item.icon}
                            </span>
                            <span>{item.name}</span>
                        </div>
                    );
                })}
            </nav>
        </aside>
    );
};

export default Sidebar;