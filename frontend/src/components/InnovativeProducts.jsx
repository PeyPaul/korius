import React, { useState, useEffect } from 'react';
import { getInnovativeProducts } from '../services/api';
import './InnovativeProducts.css';

function InnovativeProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [minSuppliers, setMinSuppliers] = useState(1);
  const [sortBy, setSortBy] = useState('suppliers');
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    loadProducts();
  }, [minSuppliers, sortBy]);

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getInnovativeProducts(minSuppliers, sortBy);
      setProducts(data.products);
      setTotalCount(data.total_count);
    } catch (err) {
      setError(err.message || 'Failed to load innovative products');
      console.error('Error loading products:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOrderProduct = (product, supplier = null) => {
    // TODO: Implement order logic
    if (supplier) {
      alert(`Order "${product.product_name}" from "${supplier.name}"?\n\nPrice: €${product.min_price.toFixed(2)} - €${product.max_price.toFixed(2)}\nDelivery: ${product.min_delivery_time} days`);
    } else {
      alert(`Order "${product.product_name}"?\n\nAvailable from ${product.supplier_count} supplier(s)\nPrice range: €${product.min_price.toFixed(2)} - €${product.max_price.toFixed(2)}\nDelivery: ${product.min_delivery_time} days`);
    }
  };

  if (loading) {
    return <div className="loading">Loading innovative products...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="innovative-products">
      <div className="controls">
        <label>
          Minimum Suppliers:
          <input
            type="number"
            min="1"
            value={minSuppliers}
            onChange={(e) => setMinSuppliers(parseInt(e.target.value) || 1)}
          />
        </label>
        <label>
          Sort By:
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="suppliers">Number of Suppliers</option>
            <option value="price">Average Price</option>
            <option value="delivery_time">Delivery Time</option>
          </select>
        </label>
        <button onClick={loadProducts}>Refresh</button>
      </div>

      <div className="summary">
        <p>Found <strong>{totalCount}</strong> innovative products</p>
      </div>

      {products.length === 0 ? (
        <div className="no-results">
          No innovative products found with the current criteria.
        </div>
      ) : (
        <div className="products-grid">
          {products.map((product, index) => (
            <div key={`${product.product_name}-${index}`} className="product-card">
              <h3>{product.product_name}</h3>
              <div className="product-info">
                <div className="info-item">
                  <span className="label">Suppliers:</span>
                  <span className="value">{product.supplier_count}</span>
                </div>
                <div className="info-item">
                  <span className="label">Avg Price:</span>
                  <span className="value">€{product.avg_price.toFixed(2)}</span>
                </div>
                <div className="info-item">
                  <span className="label">Price Range:</span>
                  <span className="value">
                    €{product.min_price.toFixed(2)} - €{product.max_price.toFixed(2)}
                  </span>
                </div>
                <div className="info-item">
                  <span className="label">Min Delivery:</span>
                  <span className="value">{product.min_delivery_time} days</span>
                </div>
                <div className="info-item">
                  <span className="label">Avg Delivery:</span>
                  <span className="value">{product.avg_delivery_time.toFixed(1)} days</span>
                </div>
              </div>
              <div className="suppliers-list">
                <strong>Available Suppliers ({product.supplier_count}):</strong>
                <ul>
                  {product.suppliers.map((supplier) => (
                    <li key={supplier.id}>
                      <div className="supplier-item">
                        <div className="supplier-details">
                          <span className="supplier-name">{supplier.name}</span>
                          <a href={`tel:${supplier.phone}`} className="supplier-phone">
                            {supplier.phone}
                          </a>
                        </div>
                        <button 
                          className="btn btn-sm btn-primary"
                          onClick={() => handleOrderProduct(product, supplier)}
                          title={`Order from ${supplier.name}`}
                        >
                          Order
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="product-actions">
                <button 
                  className="btn btn-primary btn-block"
                  onClick={() => handleOrderProduct(product)}
                  title="Order this product"
                >
                  Order This Product
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default InnovativeProducts;

