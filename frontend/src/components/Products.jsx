import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, Plus, Package } from 'lucide-react'
import './Products.css'

function Products() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const response = await axios.get('/api/v1/products/discover?limit=20')
      setProducts(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching products:', error)
      setLoading(false)
    }
  }

  const addProduct = async (product) => {
    try {
      await axios.post('/api/v1/products/add', product)
      alert('Product added to store!')
    } catch (error) {
      console.error('Error adding product:', error)
      alert('Failed to add product')
    }
  }

  const filteredProducts = products.filter(product =>
    product.title.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return <div className="products-loading">Loading products...</div>
  }

  return (
    <div className="products">
      <div className="products-header">
        <div>
          <h1>Products</h1>
          <p>Discover and add trending products</p>
        </div>
        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="products-grid">
        {filteredProducts.map((product) => (
          <div key={product.id} className="product-card">
            <div className="product-image">
              {product.images && product.images[0] ? (
                <img src={product.images[0]} alt={product.title} />
              ) : (
                <div className="product-image-placeholder">
                  <Package size={48} />
                </div>
              )}
              <div className="product-badge">
                {product.margin > 0.5 ? 'High Margin' : 'Good Margin'}
              </div>
            </div>
            <div className="product-info">
              <h3>{product.title}</h3>
              <p className="product-description">{product.description}</p>
              <div className="product-metrics">
                <div className="metric">
                  <span>Price</span>
                  <strong>${product.price.toFixed(2)}</strong>
                </div>
                <div className="metric">
                  <span>Cost</span>
                  <strong>${product.cost.toFixed(2)}</strong>
                </div>
                <div className="metric">
                  <span>Margin</span>
                  <strong className="margin-high">{(product.margin * 100).toFixed(1)}%</strong>
                </div>
                <div className="metric">
                  <span>Profit</span>
                  <strong className="profit">${product.profit.toFixed(2)}</strong>
                </div>
              </div>
              <button
                className="add-product-btn"
                onClick={() => addProduct(product)}
              >
                <Plus size={20} />
                Add to Store
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Products

