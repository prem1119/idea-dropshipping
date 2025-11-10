import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { RefreshCw, Package } from 'lucide-react'
import './Orders.css'

function Orders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchOrders()
    const interval = setInterval(fetchOrders, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchOrders = async () => {
    try {
      const response = await axios.get('/api/v1/orders/pending')
      setOrders(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching orders:', error)
      setLoading(false)
    }
  }

  const fulfillOrder = async (orderId) => {
    try {
      await axios.post(`/api/v1/orders/${orderId}/fulfill`)
      alert('Order fulfillment initiated!')
      fetchOrders()
    } catch (error) {
      console.error('Error fulfilling order:', error)
      alert('Failed to fulfill order')
    }
  }

  if (loading) {
    return <div className="orders-loading">Loading orders...</div>
  }

  return (
    <div className="orders">
      <div className="orders-header">
        <div>
          <h1>Orders</h1>
          <p>Manage and fulfill customer orders</p>
        </div>
        <button className="refresh-btn" onClick={fetchOrders}>
          <RefreshCw size={20} />
          Refresh
        </button>
      </div>

      <div className="orders-table-container">
        <table className="orders-table">
          <thead>
            <tr>
              <th>Order #</th>
              <th>Customer</th>
              <th>Items</th>
              <th>Total</th>
              <th>Status</th>
              <th>Fulfillment</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.length === 0 ? (
              <tr>
                <td colSpan="8" className="empty-state">
                  <Package size={48} />
                  <p>No pending orders</p>
                </td>
              </tr>
            ) : (
              orders.map((order) => (
                <tr key={order.id}>
                  <td className="order-number">#{order.order_number}</td>
                  <td>
                    <div>
                      <strong>{order.customer_name}</strong>
                      <p className="customer-email">{order.customer_email}</p>
                    </div>
                  </td>
                  <td>
                    <div className="order-items">
                      {order.items.map((item, idx) => (
                        <div key={idx} className="order-item">
                          {item.quantity}x {item.title}
                        </div>
                      ))}
                    </div>
                  </td>
                  <td>
                    <strong>${order.total.toFixed(2)}</strong>
                  </td>
                  <td>
                    <span className={`status-badge status-${order.status}`}>
                      {order.status}
                    </span>
                  </td>
                  <td>
                    {order.tracking_number ? (
                      <div>
                        <strong>Tracking: {order.tracking_number}</strong>
                      </div>
                    ) : (
                      <span className="status-badge status-unfulfilled">
                        {order.fulfillment_status}
                      </span>
                    )}
                  </td>
                  <td>{new Date(order.created_at).toLocaleDateString()}</td>
                  <td>
                    {order.fulfillment_status === 'unfulfilled' && (
                      <button
                        className="fulfill-btn"
                        onClick={() => fulfillOrder(order.id)}
                      >
                        Fulfill
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Orders

