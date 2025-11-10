import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  Megaphone, 
  MessageSquare 
} from 'lucide-react'
import './Sidebar.css'

function Sidebar() {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/products', label: 'Products', icon: Package },
    { path: '/orders', label: 'Orders', icon: ShoppingCart },
    { path: '/ads', label: 'Ads', icon: Megaphone },
    { path: '/customer-service', label: 'Customer Service', icon: MessageSquare }
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>Auto Dropship</h1>
        <p className="subtitle">Fully Automated</p>
      </div>
      <nav className="sidebar-nav">
        {navItems.map(item => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>
      <div className="sidebar-footer">
        <div className="status-indicator">
          <div className="status-dot active"></div>
          <span>System Active</span>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar

