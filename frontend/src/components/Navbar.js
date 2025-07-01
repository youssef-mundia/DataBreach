import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated && location.pathname !== '/login') {
    return null;
  }

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/sources', label: 'Sources', icon: '🔍' },
    { path: '/breaches', label: 'Breaches', icon: '🚨' },
    { path: '/alerts', label: 'Alerts', icon: '⚠️' },
  ];

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <span className="text-2xl">🛡️</span>
              <span className="text-xl font-bold text-gray-900">DataBreach Monitor</span>
            </Link>
          </div>

          {/* Navigation Links */}
          {isAuthenticated && (
            <div className="flex items-center space-x-8">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive(item.path)
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          )}

          {/* User Menu */}
          {isAuthenticated && (
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Welcome,</span>
                <span className="text-sm font-medium text-gray-900">
                  {user?.username || 'User'}
                </span>
              </div>
              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700 transition-colors"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;