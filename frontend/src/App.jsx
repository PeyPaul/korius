import React, { useState } from 'react';
import CheaperSuppliers from './components/CheaperSuppliers';
import InnovativeProducts from './components/InnovativeProducts';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('cheaper');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Supplier Optimization Dashboard</h1>
        <nav className="tabs">
          <button
            className={activeTab === 'cheaper' ? 'active' : ''}
            onClick={() => setActiveTab('cheaper')}
          >
            Cheaper Suppliers
          </button>
          <button
            className={activeTab === 'innovative' ? 'active' : ''}
            onClick={() => setActiveTab('innovative')}
          >
            Innovative Products
          </button>
        </nav>
      </header>
      <main className="App-main">
        {activeTab === 'cheaper' && <CheaperSuppliers />}
        {activeTab === 'innovative' && <InnovativeProducts />}
      </main>
    </div>
  );
}

export default App;

