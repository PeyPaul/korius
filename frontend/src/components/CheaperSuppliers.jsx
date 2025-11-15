import React, { useState, useEffect } from 'react';
import { getCheaperAlternatives } from '../services/api';
import './CheaperSuppliers.css';

function CheaperSuppliers() {
  const [alternatives, setAlternatives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [minSavingsPercent, setMinSavingsPercent] = useState(5.0);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    loadAlternatives();
  }, [minSavingsPercent]);

  const loadAlternatives = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getCheaperAlternatives(minSavingsPercent);
      setAlternatives(data.alternatives);
      setTotalCount(data.total_count);
    } catch (err) {
      setError(err.message || 'Failed to load cheaper alternatives');
      console.error('Error loading alternatives:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChangeSupplier = (alternative) => {
    // TODO: Implement supplier change logic
    alert(`Change supplier for "${alternative.product_name}" to "${alternative.alternative_supplier_name}"?\n\nThis will update the product's supplier.`);
  };

  const handleOrderProduct = (alternative) => {
    // TODO: Implement order logic
    alert(`Order "${alternative.product_name}" from "${alternative.alternative_supplier_name}"?\n\nPrice: €${alternative.alternative_price.toFixed(2)}\nDelivery: ${alternative.delivery_time} days`);
  };

  if (loading) {
    return <div className="loading">Loading cheaper alternatives...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="cheaper-suppliers">
      <div className="controls">
        <label>
          Minimum Savings Percentage:
          <input
            type="number"
            min="0"
            max="100"
            step="0.1"
            value={minSavingsPercent}
            onChange={(e) => setMinSavingsPercent(parseFloat(e.target.value) || 0)}
          />
          %
        </label>
        <button onClick={loadAlternatives}>Refresh</button>
      </div>

      <div className="summary">
        <p>Found <strong>{totalCount}</strong> cheaper alternatives</p>
      </div>

      {alternatives.length === 0 ? (
        <div className="no-results">
          No cheaper alternatives found with the current criteria.
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Current Supplier</th>
                <th>Current Price</th>
                <th>Alternative Supplier</th>
                <th>Alternative Price</th>
                <th>Savings</th>
                <th>Delivery</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {alternatives.map((alt, index) => (
                <tr key={`${alt.product_id}-${alt.alternative_supplier_id}-${index}`}>
                  <td>
                    <div className="product-name">{alt.product_name}</div>
                    <div className="product-meta">Stock: {alt.current_stock}</div>
                  </td>
                  <td>{alt.current_supplier_name || alt.current_supplier_id}</td>
                  <td>€{alt.current_price.toFixed(2)}</td>
                  <td>
                    <div className="supplier-info">
                      <strong>{alt.alternative_supplier_name}</strong>
                      <a href={`tel:${alt.alternative_supplier_phone}`} className="supplier-phone">
                        {alt.alternative_supplier_phone}
                      </a>
                    </div>
                  </td>
                  <td className="price">€{alt.alternative_price.toFixed(2)}</td>
                  <td>
                    <div className="savings positive">
                      <strong>€{alt.savings_amount.toFixed(2)}</strong>
                      <span className="savings-percent">{alt.savings_percent.toFixed(1)}%</span>
                    </div>
                  </td>
                  <td>{alt.delivery_time} days</td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        className="btn btn-primary"
                        onClick={() => handleChangeSupplier(alt)}
                        title="Change supplier for this product"
                      >
                        Change Supplier
                      </button>
                      <button 
                        className="btn btn-secondary"
                        onClick={() => handleOrderProduct(alt)}
                        title="Order this product from alternative supplier"
                      >
                        Order Product
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default CheaperSuppliers;

