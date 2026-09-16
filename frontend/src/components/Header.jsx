import React from 'react';

const Header = () => {
  return (
    <header className="bmw-header">
      <div className="bmw-header-container">
        <div className="bmw-logo-group">
          <div className="bmw-roundel">
            <div className="roundel-quad q1"></div>
            <div className="roundel-quad q2"></div>
            <div className="roundel-quad q3"></div>
            <div className="roundel-quad q4"></div>
          </div>
          <div>
            <h1 className="bmw-title">BMW Service Knowledge Assistant</h1>
            <p className="bmw-subtitle">
              AI-powered service documentation assistant for technicians
            </p>
          </div>
        </div>
        <div className="bmw-badge-pill">
          <span className="pill-dot"></span>
          ISTAGuided RAG v1.0
        </div>
      </div>
    </header>
  );
};

export default Header;
