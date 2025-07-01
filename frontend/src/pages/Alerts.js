import React from 'react';
import { useQuery } from 'react-query';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { alertsService } from '../services/api';

const Alerts = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Query for alerts
  const { data: alerts, isLoading, error } = useQuery(
    'alerts',
    () => alertsService.getAll(),
    {
      refetchInterval: 15000, // Refetch every 15 seconds for alerts
    }
  );

  const getThreatLevelColor = (level) => {
    switch (level) {
      case 'critical': return 'threat-critical';
      case 'high': return 'threat-high';
      case 'medium': return 'threat-medium';
      case 'low': return 'threat-low';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getThreatIcon = (level) => {
    switch (level) {
      case 'critical': return '🚨';
      case 'high': return '⚠️';
      case 'medium': return '⚡';
      case 'low': return 'ℹ️';
      default: return '📢';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Alerts</h1>
        <div className="flex items-center space-x-4">
          <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
            <option value="">All Alerts</option>
            <option value="sent">Sent</option>
            <option value="pending">Pending</option>
          </select>
          <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
            <option value="">All Priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>

      {/* Alerts List */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-lg font-semibold text-gray-900">
            Recent Alerts ({alerts?.data?.length || 0})
          </h2>
        </div>
        <div className="card-content">
          {error ? (
            <div className="text-center py-8 text-red-600">
              Error loading alerts: {error.response?.data?.detail || error.message}
            </div>
          ) : alerts?.data?.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl mb-2">🔔</div>
              <p>No alerts generated yet</p>
              <p className="text-sm">Alerts will appear here when breaches are detected</p>
            </div>
          ) : (
            <div className="space-y-4">
              {alerts?.data?.map((alert) => (
                <div
                  key={alert.id}
                  className={`border rounded-lg p-4 ${
                    alert.is_sent
                      ? 'border-gray-200 bg-gray-50'
                      : 'border-yellow-300 bg-yellow-50'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="text-2xl">
                          {getThreatIcon(alert.threat_level)}
                        </span>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {alert.title}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getThreatLevelColor(alert.threat_level)}`}>
                          {alert.threat_level.toUpperCase()}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          alert.is_sent
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {alert.is_sent ? 'Sent' : 'Pending'}
                        </span>
                      </div>
                      
                      <p className="text-gray-700 mb-3">
                        {alert.message}
                      </p>
                      
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>
                          Created: {new Date(alert.created_at).toLocaleString()}
                        </span>
                        {alert.sent_at && (
                          <>
                            <span>•</span>
                            <span>
                              Sent: {new Date(alert.sent_at).toLocaleString()}
                            </span>
                          </>
                        )}
                        <span>•</span>
                        <span>Breach ID: {alert.breach_data_id}</span>
                      </div>
                      
                      {alert.sent_channels && alert.sent_channels.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          <span className="text-sm text-gray-600">Sent via:</span>
                          {alert.sent_channels.map((channel, idx) => (
                            <span
                              key={idx}
                              className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
                            >
                              {channel}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex flex-col space-y-2 ml-4">
                      {!alert.is_sent && (
                        <button className="btn-primary text-sm py-1 px-3">
                          Send Now
                        </button>
                      )}
                      <button className="btn-secondary text-sm py-1 px-3">
                        View Breach
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Alert Configuration */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">
            <h2 className="text-lg font-semibold text-gray-900">Alert Channels</h2>
          </div>
          <div className="card-content">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">📧</span>
                  <span>Email Notifications</span>
                </div>
                <button className="text-sm text-blue-600 hover:text-blue-800">
                  Configure
                </button>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">📱</span>
                  <span>SMS Alerts</span>
                </div>
                <button className="text-sm text-blue-600 hover:text-blue-800">
                  Configure
                </button>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">💬</span>
                  <span>Slack Integration</span>
                </div>
                <button className="text-sm text-blue-600 hover:text-blue-800">
                  Configure
                </button>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">📞</span>
                  <span>Webhook Notifications</span>
                </div>
                <button className="text-sm text-blue-600 hover:text-blue-800">
                  Configure
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2 className="text-lg font-semibold text-gray-900">Alert Rules</h2>
          </div>
          <div className="card-content">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span>Critical threats</span>
                <span className="text-sm text-green-600">Immediate</span>
              </div>
              <div className="flex items-center justify-between">
                <span>High priority threats</span>
                <span className="text-sm text-yellow-600">Within 15 min</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Medium priority threats</span>
                <span className="text-sm text-blue-600">Within 1 hour</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Low priority threats</span>
                <span className="text-sm text-gray-600">Daily digest</span>
              </div>
              <div className="pt-2 border-t">
                <button className="btn-primary text-sm w-full">
                  Customize Rules
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Alerts;