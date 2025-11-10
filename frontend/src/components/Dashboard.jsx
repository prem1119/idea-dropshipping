import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { 
  DollarSign, 
  TrendingUp, 
  ShoppingCart, 
  Target,
  ArrowUp,
  ArrowDown
} from 'lucide-react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
import './Dashboard.css'

function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 60000) // Refresh every minute
    return () => clearInterval(interval)
  }, [])

  const fetchMetrics = async () => {
    try {
      const response = await axios.get('/api/v1/dashboard/metrics')
      setMetrics(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching metrics:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>
  }

  if (!metrics) {
    return <div className="dashboard-error">Failed to load metrics</div>
  }

  const statCards = [
    {
      title: 'Total Sales',
      value: `$${metrics.total_sales.toFixed(2)}`,
      icon: DollarSign,
      change: '+12.5%',
      positive: true
    },
    {
      title: 'Total Profit',
      value: `$${metrics.total_profit.toFixed(2)}`,
      icon: TrendingUp,
      change: '+8.3%',
      positive: true
    },
    {
      title: 'Total Orders',
      value: metrics.total_orders.toString(),
      icon: ShoppingCart,
      change: '+15.2%',
      positive: true
    },
    {
      title: 'ROI',
      value: `${metrics.roi.toFixed(1)}%`,
      icon: Target,
      change: `+${(metrics.roi / 10).toFixed(1)}%`,
      positive: true
    }
  ]

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Real-time metrics and analytics</p>
      </div>

      <div className="stats-grid">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div key={index} className="stat-card">
              <div className="stat-header">
                <div className="stat-icon">
                  <Icon size={24} />
                </div>
                <span className={`stat-change ${stat.positive ? 'positive' : 'negative'}`}>
                  {stat.positive ? <ArrowUp size={16} /> : <ArrowDown size={16} />}
                  {stat.change}
                </span>
              </div>
              <h3>{stat.value}</h3>
              <p>{stat.title}</p>
            </div>
          )
        })}
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h2>Sales Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics.sales_by_date}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="sales" 
                stroke="#3b82f6" 
                strokeWidth={2}
                name="Sales ($)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h2>Profit Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics.profit_by_date}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="profit" 
                stroke="#10b981" 
                strokeWidth={2}
                name="Profit ($)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="tables-grid">
        <div className="table-card">
          <h2>Top Products</h2>
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Revenue</th>
                <th>Quantity</th>
              </tr>
            </thead>
            <tbody>
              {metrics.top_products.slice(0, 5).map((product, index) => (
                <tr key={index}>
                  <td>{product.name || product.title}</td>
                  <td>${product.revenue?.toFixed(2) || product.sales?.toFixed(2)}</td>
                  <td>{product.quantity || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="table-card">
          <h2>Ad Performance</h2>
          <table>
            <thead>
              <tr>
                <th>Platform</th>
                <th>Spend</th>
                <th>ROAS</th>
                <th>Conversions</th>
              </tr>
            </thead>
            <tbody>
              {metrics.ad_performance.map((ad, index) => (
                <tr key={index}>
                  <td>{ad.platform}</td>
                  <td>${ad.spend.toFixed(2)}</td>
                  <td>{ad.roas.toFixed(2)}x</td>
                  <td>{ad.conversions}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="metrics-summary">
        <div className="metric-item">
          <span>Ad Spend:</span>
          <strong>${metrics.total_ad_spend.toFixed(2)}</strong>
        </div>
        <div className="metric-item">
          <span>Conversion Rate:</span>
          <strong>{metrics.conversion_rate.toFixed(2)}%</strong>
        </div>
        <div className="metric-item">
          <span>Avg Order Value:</span>
          <strong>${metrics.average_order_value.toFixed(2)}</strong>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

