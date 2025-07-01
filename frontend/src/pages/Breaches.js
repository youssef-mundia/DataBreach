import React from 'react';
import { useQuery } from 'react-query';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { breachesService } from '../services/api';

const Breaches = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Query for breaches
  const { data: breaches, isLoading, error } = useQuery(
    'breaches',
    () => breachesService.getAll(),
    {
      refetchInterval: 30000,
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
      case 'critical': return '🔴';
      case 'high': return '🟠';
      case 'medium': return '🟡';
      case 'low': return '🟢';
      default: return '⚪';
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
        <h1 className="text-3xl font-bold text-gray-900">Data Breaches</h1>
        <div className="flex items-center space-x-4">
          <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
            <option value="">All Threats</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
            <option value="">All Sources</option>
            <option value="verified">Verified Only</option>
            <option value="unverified">Unverified</option>
          </select>
        </div>
      </div>

      {/* Breaches List */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-lg font-semibold text-gray-900">
            Recent Breaches ({breaches?.data?.length || 0})
          </h2>
        </div>
        <div className="card-content">
          {error ? (
            <div className="text-center py-8 text-red-600">
              Error loading breaches: {error.response?.data?.detail || error.message}
            </div>
          ) : breaches?.data?.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl mb-2">🔍</div>
              <p>No breaches detected yet</p>
              <p className="text-sm">Monitor sources will be checked automatically</p>
            </div>
          ) : (
            <div className="space-y-4">
              {breaches?.data?.map((breach) => (
                <div
                  key={breach.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {breach.title}
                        </h3>
                        {breach.threat_level && (
                          <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getThreatLevelColor(breach.threat_level)}`}>
                            {getThreatIcon(breach.threat_level)} {breach.threat_level.toUpperCase()}
                          </span>
                        )}
                        {breach.is_verified && (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            ✓ Verified
                          </span>
                        )}
                        {breach.is_false_positive && (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            False Positive
                          </span>
                        )}
                      </div>
                      
                      <p className="text-gray-600 mb-3 line-clamp-3">
                        {breach.content}
                      </p>
                      
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>Source ID: {breach.source_id}</span>
                        <span>•</span>
                        <span>
                          Discovered: {new Date(breach.discovered_at).toLocaleString()}
                        </span>
                        {breach.url && (
                          <>
                            <span>•</span>
                            <a
                              href={breach.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:text-blue-800"
                            >
                              View Source
                            </a>
                          </>
                        )}
                      </div>
                      
                      {breach.keywords_matched && breach.keywords_matched.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          <span className="text-sm text-gray-600">Keywords:</span>
                          {breach.keywords_matched.map((keyword, idx) => (
                            <span
                              key={idx}
                              className="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded"
                            >
                              {keyword}
                            </span>
                          ))}
                        </div>
                      )}
                      
                      {breach.categories && breach.categories.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          <span className="text-sm text-gray-600">Categories:</span>
                          {breach.categories.map((category, idx) => (
                            <span
                              key={idx}
                              className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
                            >
                              {category}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex flex-col space-y-2 ml-4">
                      {!breach.is_verified && !breach.is_false_positive && (
                        <>
                          <button className="btn-primary text-sm py-1 px-3">
                            Verify
                          </button>
                          <button className="btn-secondary text-sm py-1 px-3">
                            False Positive
                          </button>
                        </>
                      )}
                      {breach.confidence_score && (
                        <div className="text-xs text-gray-500 text-center">
                          Confidence: {(breach.confidence_score * 100).toFixed(1)}%
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Breaches;