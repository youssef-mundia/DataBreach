import React from 'react';
import { useQuery } from 'react-query';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { breachesService, healthService } from '../services/api';

const Dashboard = () => {
  const { isAuthenticated, loading } = useAuth();

  // Health check query
  const { data: healthData, isLoading: healthLoading } = useQuery(
    'health',
    () => healthService.getStatus(),
    {
      refetchInterval: 30000, // Refetch every 30 seconds
      retry: 2,
    }
  );

  // Breach stats query
  const { data: statsData, isLoading: statsLoading } = useQuery(
    'breach-stats',
    () => breachesService.getStats(),
    {
      refetchInterval: 10000, // Refetch every 10 seconds
      retry: 2,
    }
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const stats = statsData?.data || {};
  const health = healthData?.data || {};

  const statCards = [
    {
      title: 'Total Breaches',
      value: stats.total_breaches || 0,
      icon: '🚨',
      color: 'blue',
    },
    {
      title: 'Breaches Today',
      value: stats.breaches_today || 0,
      icon: '📅',
      color: 'green',
    },
    {
      title: 'Critical Breaches',
      value: stats.critical_breaches || 0,
      icon: '🔴',
      color: 'red',
    },
    {
      title: 'High Priority',
      value: stats.high_breaches || 0,
      icon: '🟠',
      color: 'orange',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex items-center space-x-2">
          <div
            className={`h-2 w-2 rounded-full ${
              health.status === 'healthy' ? 'bg-green-400' : 'bg-red-400'
            }`}
          ></div>
          <span className="text-sm text-gray-600">
            System {health.status === 'healthy' ? 'Healthy' : 'Issues Detected'}
          </span>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div key={index} className="card">
            <div className="card-content">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {statsLoading ? (
                      <div className="animate-pulse bg-gray-200 h-8 w-16 rounded"></div>
                    ) : (
                      stat.value.toLocaleString()
                    )}
                  </p>
                </div>
                <div className="text-3xl">{stat.icon}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Database Status */}
        <div className="card">
          <div className="card-header">
            <h2 className="text-lg font-semibold text-gray-900">Database Status</h2>
          </div>
          <div className="card-content">
            {healthLoading ? (
              <div className="animate-pulse space-y-2">
                <div className="bg-gray-200 h-4 w-3/4 rounded"></div>
                <div className="bg-gray-200 h-4 w-1/2 rounded"></div>
              </div>
            ) : (
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">PostgreSQL</span>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      health.database?.connectivity?.postgres === 'healthy'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {health.database?.connectivity?.postgres || 'Unknown'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Redis</span>
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      health.database?.connectivity?.redis === 'healthy'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {health.database?.connectivity?.redis || 'Unknown'}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* System Resources */}
        <div className="card">
          <div className="card-header">
            <h2 className="text-lg font-semibold text-gray-900">System Resources</h2>
          </div>
          <div className="card-content">
            {healthLoading ? (
              <div className="animate-pulse space-y-2">
                <div className="bg-gray-200 h-4 w-3/4 rounded"></div>
                <div className="bg-gray-200 h-4 w-1/2 rounded"></div>
              </div>
            ) : (
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">CPU Usage</span>
                    <span className="font-medium">
                      {health.system?.cpu_percent?.toFixed(1) || 0}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${health.system?.cpu_percent || 0}%` }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Memory Usage</span>
                    <span className="font-medium">
                      {health.system?.memory_percent?.toFixed(1) || 0}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                    <div
                      className="bg-green-600 h-2 rounded-full"
                      style={{ width: `${health.system?.memory_percent || 0}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Activity Placeholder */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
        </div>
        <div className="card-content">
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-2">🔍</div>
            <p>Monitoring system is active</p>
            <p className="text-sm">Recent breach data will appear here</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;