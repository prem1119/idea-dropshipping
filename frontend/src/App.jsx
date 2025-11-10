import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Products from './components/Products'
import Orders from './components/Orders'
import Ads from './components/Ads'
import CustomerService from './components/CustomerService'
import Sidebar from './components/Sidebar'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/products" element={<Products />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/ads" element={<Ads />} />
            <Route path="/customer-service" element={<CustomerService />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

